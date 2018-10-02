# Breeze Project Definition



This is a directory containing a breeze.toml configutation file.

    # This is a breeze Project Definition file.

    # Project Name is required, it must observer the same rules as CF stack names
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-parameters.html
    project_name="abc-website"

    # Generator Cmd is required. This is the command line that will be executed when generating a new infrastructure definition version. 
    # Breeze will replace <version_lable> and <output_directory> with appropriate values.
    generator_cmd="python generate.py <version_label> <output_directory>"


