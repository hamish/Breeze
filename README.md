# Breeze System

Breeze is a system for building cloudformation templates, and maintaining cloudformation stacks.

# Breeze Project Definition

This is a directory containing a breeze.toml configutation file, and other files supporting the generation of cloudformation templates, policy files and other artifacts.

    # This is a breeze Project Definition file.

    # Project Name is required, it must observer the same rules as CF stack names
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-parameters.html
    project_name="abc-website"

    # Generator Cmd is required. This is the command line that will be executed when generating a new infrastructure definition version. 
    # Breeze will replace <version_lable>, <output_directory> and <bucket_url> with appropriate values.
    generator_cmd="python generate.py <version_label> <output_directory> <bucket_url>"

    # Infrastructure Definition Bucket Name
    # The name of the bucket that will store the completed infrastructure definition. This bucket shoud be writable to by the AWS account configured.
    id_bucket_name="breeze-bucket"

    # Infrastructure Definition Prefix
    # The prefix used to create all infrastructure definitions. Note that <project_name> will be replaced with the name defined above. 
    # The version label will be used to further seperate the infrastructure definitions.
    id_prefix="infrstructure-definitions/<project_name>/"

    # The default template name. 
    template_name="main"

    # Parameters to be used when launching a stack
    [Parameters]
    # Webserver Instance Size
    webserver_instance_size="t3.micro"

    [Parameters.by_account_id.359123456789]
    # A route 53 domain that has already been configured to exist in the account
    domain_name="testing.breeze.org.au"

    [Parameters.by_account_id.953123456789]
    # A route 53 domain that has already been configured to exist in the account
    domain_name="production.breeze.org.au"

# Breeze Infrastructure Definition

An Infrastructure Definition (ID) is a directory structure of files that make up the templates, policy 
files and other artifacts needed to launch a cloudformation stack. For IDs that create nested stacks, 
the eventual bucket name and prefix must be known at generation time. This is because [the reference to the nested stack must be a fully qualified s3 URL](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl).

The Project Definition generator creaets these files on disk locally, the breeze tool is repsponsible for uploading them to S3.


# Breeze cli

The breeze cli is a tool designed to help create and use Infrastructure Definitions.

## Generate

    breeze generate <project_definition_file> [--version version_label]

### What this does:

1. If Version Label was not specified, generate a new version lable (yyyyMMdd-HHmmss)
1. Read the project definition file and obtain the generator command, the bucket and prefix names.
1. Generate the parameters to the generator:

   bucket_url: https://s3.amazonaws.com/<bucket_name>/bucket_prefix/<version_label>

   output_directory: output/<project_name>/version

1. Run the generator, waiting for completion.
1. If the execution returned an error, print what we can and exit.
1. Optional: Copy the output from the versioned directory to output/<project_name>-latest/
1. Upload the versioned ID directory to s3.
1. Add variables to ssm parameter store to enable the version to be discovered.

   TODO: Determine what SSM Parameters to upload...



## Launch

    breeze launch <project_name> <stack_name> [--version version_label] [--main-template template_name] [--override parameter_name=parameter_value [--override parameter_name=parameter_value]]

### What this does:

1. Check that no stack with the name exists, or if it does and is in a delete in progress state, wait until the delete is complete.
1. If version not specified, retrieve the  /breeze/<project_name>/default-version parameter from SSM. Use this value as version_label
1. Retrieve the /breeze/<project_name>/versions/<version_label>/breeze-project-definition-url parameter from SSM.
1. Download the breeze project definition file from S3.
1. If template_name not specified, obtain the default from the breeze project definition file.
1. Retrieve the main template from S3 and parse the file, noting the parameters.
1. Apply any override parameters if applicable.
1. Identify the matching parameters in the definition file.
1. Launch the new stack with the template, the stack_name and the parameters.



## Update

    breeze update <stack_name> [--version version_label] [--main-template template_name] [--override parameter_name=parameter_value [--override parameter_name=parameter_value]] [--apply-change]

### What this does:

1. Check that the specified stack exists, and that it is in an updatable status, if not, wait until it becomes updatable.
1. If the version is not specified, obtain the version from the currently running stack.
1. If the template name is not specified, obtain the version from the currently running stack.
1. Obtain the parameter values from the currently running stack. (Note that "NoEcho" parameter values are not available from the stack.)
1. Obtain the project definition file and the main templates files from S3.
1. Construct the parameters, using overrides, then current stack values, then values from the project definition file as precidence.
1. Create a change set with the stack_name, template and parameters.
1. Wait until the change set is available, print the change.
1. If the apply-change flag has been set, apply the change.



## Delete 

    breeze delete <stack_name>

### What this does:

1. Check that the specified stack exists and that it is in a deletable status, if not, wait until it becomes deletable.
1. Delete the stack.
1. Watch the progress of the stack deletion, and take restorative measures if failures occur. This could involve re-submitting the delete, resubmitting but passing the option to retain the resources that failed to delete, or using the API to delete the resource in qustion.


TODO:

## Why is this useful

Update this to describe why someone would choose to use this rather than the aws cli, or one of the other tools.

Some Benefits:

* Allows developers to obtain a set of infrastructure with the same (or simmilar) settings to produciton easily.
* Allows developers to reherse the upgrade of a set of infrastructure from one set of templates to another in a controlled way.
* Allows administrators to apply stack policies that protect infrastructure from getting removed or replaced by an error in a template.
* Allows infrastructure that is only intermittently needed (prototype servers for example) to be created when needed in a child template and then destroyed when no longer needed.

## Execute breeze in cloud

All breeze commands (except perhaps generate) should execute in lambda/step functions rather than on a particular computer. This makes the capabilities available to a wider range of users and enables alternative UI's (web, voice, etc) and should improve robustness.

## Additional Commands

There are a number of extra commands to document, including:

    breeze apply_policy <stack_name> <policy_name>
    breeze remove_policy <stack_name>
    breeze launch-child <main_stack_name> <child_template_name> [--override parameter_name=parameter_value [--override parameter_name=parameter_value]] 
    breeze delete-child <main_stack_name> <child_template_name>

## Additional cli options

* The ability to wait for a CF operation to complete.

## Additional parameter options

* allow users to specify queries for ami's at launch/update time. eg latest windows or linux ami.
* there are probably other dimensions that paramters should be configurable along than just accountid.


# Integrating with CI/CD pipelines.

Breeze provides the ability to launch a stack at a particular version and then upgrade the stack to a new version. It is intended that in a CI/CD situation, a stack will be launched at the same version as a target stack (production, UAT, etc), a newer version applied and tests executed to determine if there were problems during stack update. If the tests pass, the version is considered suitable to be installed in the next and the CI/CD pipeling moves on to the next stage.

# Automation

It is intended that launching and deleting stacks can be integrated with a home/office automation system such as Alexia. 

# Automatic Deletion of stacks.

Stacks in development avccounts may be given a time to live, and are subject to deletion after that time.
