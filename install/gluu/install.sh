#!/bin/bash

### This setup just install the fresh gluu server
### Accept two command line argument
### Need two environment GLUU_VERSION PASSPORT_HOST PASSPORT_IP PASSPORT_HOST_GLUU_ADMIN_PASSWORD

### Ads and install latest STABLE package for ubuntu 20
echo "Installing Gluu..."
if [ $GLUU_VERSION == "LATEST-DEV" ]
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
community_setup_dir=/opt/gluu-server/install/community-edition-setup
install_dir=$TEST_DIR/install
templates_dir=$install_dir/gluu/templates
setup_property_file=$templates_dir/setup.properties 
sed -i "1s/.*/ip=$PASSPORT_IP/" $setup_property_file
sed -i "2s/.*/ldapPass=$PASSPORT_HOST_GLUU_ADMIN_PASSWORD/" $setup_property_file
sed -i "3s/.*/oxtrust_admin_password=$PASSPORT_HOST_GLUU_ADMIN_PASSWORD/" $setup_property_file
sed -i "4s/.*/hostname=$PASSPORT_HOST/" $setup_property_file

cp $setup_property_file $community_setup_dir

# apache ssl and config setup
apache_dir=$templates_dir/apache
tar -zxvf $apache_dir/etcletsencrypt.tar -C /opt/gluu-server
cp -R $apache_dir/https_gluu.conf $community_setup_dir/templates/apache

### Setup Gluu Server
echo "Setuping Gluu..."
gluu-serverd login << EOF
cd /install/community-edition-setup/
./setup.py -n -c
EOF

### TODO: Setup gluu-passport as per PR

### Wait for services to start
wait_until_port_start () {
	port=$1
	while ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; do
	  echo "waiting for port $port"
	  sleep 5
	done

	echo "Port $port started"
}

wait_until_port_start 8081
wait_until_port_start 8082
wait_until_port_start 8090
