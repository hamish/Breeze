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



## Launch

    breeze launch <project_name> <stack_name>

### Waht this does

1. 




    usage: breeze command [options] 

    verge generate -v version_label output_directory -d breeze_project_directory
    breeze launch stack_name -p project_name -l version_label [-o parameter_name=value [-o parameter_name=value]
    breeze update_version stack_name -l version_label
    breeze launch_child_stack parent_stack_name -t template_name
    breeze delete_child_stack parent_stack_name -t template_name
    breeze apply_policy stack_name policy_name
    breeze remove_policy stack_name




