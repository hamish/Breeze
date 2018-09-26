import sys
import os

def generate(version, bucket_name, directory):
    versioned_dir = os.path.join(directory, "versioned", version)
    os.makedirs(versioned_dir)
    from troposphere import Ref, Template
    import troposphere.ec2 as ec2
    t = Template()
    instance = ec2.Instance("myinstance")
    instance.ImageId = "ami-951945d0"
    instance.InstanceType = "t1.micro"
    t.add_resource(instance)
    print(t.to_json())


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ("usage: {} version, bucket_name, directory".format(sys.argv[0]))
        sys.exit()
    version=sys.argv[1]
    bucket_name=sys.argv[2]
    directory=sys.argv[3]
    generate(version, bucket_name, directory)
