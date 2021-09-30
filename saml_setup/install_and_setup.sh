#!/bin/bash

### This setup just install the fresh gluu server
### Accept two command line argument
### Need two environment PASSPORT_HOST_IP PASSPORT_HOST_GLUU_ADMIN_PASSWORD

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
sed -i "1s/.*/ip=$PASSPORT_HOST_IP/" ~/gluu-passport-testing/setup.properties
sed -i "2s/.*/ldapPass=$PASSPORT_HOST_GLUU_ADMIN_PASSWORD/" ~/gluu-passport-testing/setup.properties
sed -i "3s/.*/oxtrust_admin_password=$PASSPORT_HOST_GLUU_ADMIN_PASSWORD/" ~/gluu-passport-testing/setup.properties

cp ~/gluu-passport-testing/setup.properties /opt/gluu-server/install/community-edition-setup

### Setup Gluu Server
gluu-serverd login << EOF
cd /install/community-edition-setup/
./setup.py -n -c
EOF
