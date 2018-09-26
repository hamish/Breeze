import sys
import os
import json
import shutil

def write_file(file_path, file_body):
    with open(file_path, 'w') as f:
        f.write(file_body)

def generate(version, bucket_name, directory):
    base_dir = os.path.join(directory, "versioned", version)
    templates_dir = os.path.join(base_dir, "templates" )
    policies_dir = os.path.join(base_dir, "policies" )
    os.makedirs(base_dir)
    os.makedirs(templates_dir)
    os.makedirs(policies_dir)

    from troposphere import Ref, Template
    import troposphere.ec2 as ec2
    t = Template()
    instance = ec2.Instance("myinstance")
    instance.ImageId = "ami-951945d0"
    instance.InstanceType = "t1.micro"
    t.add_resource(instance)
    # print(t.to_json())

    template_file_path=os.path.join(templates_dir, "template.json")
    template_file_body=t.to_json()
    write_file(template_file_path, template_file_body)

    policy_file_path=os.path.join(policies_dir, "template-restricted.json")
    policy_file_body=json.dumps({
        "Statement" : [
            {
                "Effect" : "Allow",
                "Action" : "Update:*",
                "Principal": "*",
                "Resource" : "*"
            },
            {
                "Effect" : "Deny",
                "Action" : "Update:*",
                "Principal": "*",
                "Resource" : "LogicalResourceId/ProductionDatabase"
            }
        ]
    })
    write_file(policy_file_path, policy_file_body)

    config_path=os.path.join(base_dir, "breeze.json")
    config_body=json.dumps({
        "DefaultPolicy":"permisive",
        "Policies" : [ "restricted", "permisive"]
    }, sort_keys=True, indent=4)
    write_file(config_path, config_body)

    latest_dir = os.path.join(directory, "latest")

    if os.path.exists(latest_dir):
        shutil.rmtree(latest_dir)
    shutil.copytree(base_dir, latest_dir)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ("usage: {} version, bucket_name, directory".format(sys.argv[0]))
        sys.exit()
    version=sys.argv[1]
    bucket_name=sys.argv[2]
    directory=sys.argv[3]
    generate(version, bucket_name, directory)
