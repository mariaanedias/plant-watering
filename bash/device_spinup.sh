#!/bin/sh

#Once connected to your Amazon EC2 instance through SSH, run the following commands to create user ggc_user and group ggc_group
adduser --system ggc_user
groupadd --system ggc_group

#Extract and run the following script to mount Linux control groups (cgroups). This is an AWS Greengrass dependency:
curl https://raw.githubusercontent.com/tianon/cgroupfs-mount/951c38ee8d802330454bdede20d85ec1c0f8d312/cgroupfs-mount > cgroupfs-mount.sh
chmod +x cgroupfs-mount.sh 
sudo bash ./cgroupfs-mount.sh

#sudo yum install git -y
git clone https://github.com/aws-samples/aws-greengrass-samples.git
cd aws-greengrass-samples
cd greengrass-dependency-checker-GGCv1.6.0
sudo ./check_ggc_dependencies

aws s3 cp s3://gg-project-files-bf/greengrass-linux-armv7l-1.6.0.tar.gz /tmp/greengrass-linux-armv7l-1.6.0.tar.gz
tar -xzvf /tmp/greengrass-linux-armv7l-1.6.0.tar.gz -C /

aws s3 cp --recursive s3://gg-project-files-bf/certs/ /greengrass/certs/
aws s3 cp --recursive s3://gg-project-files-bf/config/ /greengrass/config/

cd /greengrass/certs/
sudo wget -O root.ca.pem http://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem

cd /greengrass/ggc/core/
sudo ./greengrassd start

# aws s3 sync config/ s3://gg-project-files-bf/config/
# aws s3 sync certs/ s3://gg-project-files-bf/certs/