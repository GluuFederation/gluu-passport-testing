#!/bin/bash

### This setup just install the fresh gluu server
### Accept two command line argument
### Need two environment PASSPORT_HOST PASSPORT_HOST_IP PASSPORT_HOST_GLUU_ADMIN_PASSWORD

### Ads and install latest STABLE package for ubuntu 18
echo "deb https://repo.gluu.org/ubuntu/ focal main" > /etc/apt/sources.list.d/gluu-repo.list
curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
apt update -y
apt install gluu-server -y
apt-mark hold gluu-server -y

gluu-serverd enable
echo "Starting gluu-serverd..."
gluu-serverd start
echo "Loggin in to execute next script..."
gluu-serverd login
echo "All finished!"

### Move preconfigured setup.properties to gluu setup directory
test_data_dir=/root/gluu-passport-testing/install
setup_property_file=$test_data_dir/gluu/templates/setup.properties 
sed -i "1s/.*/ip=$PASSPORT_HOST_IP/" $setup_property_file
sed -i "2s/.*/ldapPass=$PASSPORT_HOST_GLUU_ADMIN_PASSWORD/" $setup_property_file
sed -i "3s/.*/oxtrust_admin_password=$PASSPORT_HOST_GLUU_ADMIN_PASSWORD/" $setup_property_file
sed -i "4s/.*/hostname=$PASSPORT_HOST/" $setup_property_file

cp $setup_property_file /opt/gluu-server/install/community-edition-setup

### Setup Gluu Server
gluu-serverd login << EOF
cd /install/community-edition-setup/
./setup.py -n -c
EOF