# Breeze

Breeze is a system for building cloudformation templates, and maintaining cloudformation stacks.

# Breeze Project Definition

This is a directory containing a breeze.toml configutation file, and other files supporting the generation of cloudformation templates, policy files and other artifacts.

    # This is a breeze Project Definition file.

    # Project Name is required, it must observer the same rules as CF stack names
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-parameters.html
    project_name="abc-website"

    # Generator Cmd is required. This is the command line that will be executed when generating a new infrastructure definition version. 
    # Breeze will replace <version_lable> and <output_directory> with appropriate values.
    generator_cmd="python generate.py <version_label> <output_directory> <bucket_name> <bucket_prefix>"

# Breeze Infrastructure Definition

An Infrastructure Definition (ID) is a directory structure of files that make up the templates, policy 
files and other artifacts needed to launch a cloudformation stack. For IDs that create nested stacks, 
the eventual bucket name and prefix must be known at generation time. This is because [the reference to the nested stack must be a fully qualified s3 URL(https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl).

The Project Definition generator creaets these files on disk locally, the breeze tool is repsponsible for uploading them to S3.










    usage: breeze command [options] 

    verge generate -v version_label output_directory -d breeze_project_directory
    breeze launch stack_name -p project_name -l version_label [-o parameter_name=value [-o parameter_name=value]
    breeze update_version stack_name -l version_label
    breeze launch_child_stack parent_stack_name -t template_name
    breeze delete_child_stack parent_stack_name -t template_name
    breeze apply_policy stack_name policy_name
    breeze remove_policy stack_name




