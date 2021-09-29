### This setup just install the fresh gluu server

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
cp /test-install-data/setup.properties /opt/gluu-server/install/community-edition-setup

### Setup Gluu Server
gluu-serverd login << EOF
cd /install/community-edition-setup/
./setup.py -n -c
EOF
