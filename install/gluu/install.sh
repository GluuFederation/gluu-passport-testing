#!/bin/bash

### This setup just install the fresh gluu server
### Accept two command line argument
### Need two environment GLUU_VERSION PASSPORT_HOST PASSPORT_HOST_IP PASSPORT_HOST_GLUU_ADMIN_PASSWORD

### Ads and install latest STABLE package for ubuntu 20
echo "Installing Gluu..."
if [ $GLUU_VERSION == "LATEST" ]
then
  echo "deb https://repo.gluu.org/ubuntu/ focal-devel main" > /etc/apt/sources.list.d/gluu-repo.list
else
  echo "deb https://repo.gluu.org/ubuntu/ focal main" > /etc/apt/sources.list.d/gluu-repo.list
fi

curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
apt update -y
apt install gluu-server -y
apt-mark hold gluu-server -y

gluu-serverd enable
echo "Starting Gluu..."
gluu-serverd start

### Move preconfigured setup.properties to gluu setup directory
echo "Making Config File..."
export TEST_DIR=/root/gluu-passport-testing
install_dir=$TEST_DIR/install
setup_property_file=$install_dir/gluu/templates/setup.properties 
sed -i "1s/.*/ip=$PASSPORT_HOST_IP/" $setup_property_file
sed -i "2s/.*/ldapPass=$PASSPORT_HOST_GLUU_ADMIN_PASSWORD/" $setup_property_file
sed -i "3s/.*/oxtrust_admin_password=$PASSPORT_HOST_GLUU_ADMIN_PASSWORD/" $setup_property_file
sed -i "4s/.*/hostname=$PASSPORT_HOST/" $setup_property_file

cp $setup_property_file /opt/gluu-server/install/community-edition-setup

### Setup Gluu Server
echo "Setuping Gluu..."
gluu-serverd login << EOF
cd /install/community-edition-setup/
./setup.py -n -c
EOF
