# FILE: /test-install-data/gluu.sh
# File called by init.d on start. To be started, needs to have flag file /root/freshsnap
# Can be created, for testing pruposes, w/ touch /root/freshsnap

if [ -f /root/freshsnap ]
then
    ### Ads and install latest STABLE package for ubuntu 18
    # echo "deb https://repo.gluu.org/ubuntu/ bionic main" > /etc/apt/sources.list.d/gluu-repo.list

    ### Ads and install latest DEV package for ubuntu 18
    echo "deb https://repo.gluu.org/ubuntu/ bionic-devel main" > /etc/apt/sources.list.d/gluu-repo.list
    curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
    apt update -y
    apt install gluu-server -y
    apt-mark hold gluu-server -y
    ### copy setup files to chmod
    echo "Copying setup files to chmod..."
    cp /test-install-data/setup.properties /opt/gluu-server/install/community-edition-setup/.
    ### In case of 4.2.0 needs to overwrite setup.py
    cp /test-install-data/setup.py /opt/gluu-server/install/community-edition-setup/.
    echo "Copying templates files to chmod..."
    ### Templates
    cp /test-install-data/templates/*.* /opt/gluu-server/install/community-edition-setup/templates/.
    echo "Copying certbot script to chmod..."
    ### Certbot to root chmod
    cp /test-install-data/certbot.sh /opt/gluu-server/root/.

    echo "Creating flag file on chroot to initiate script on first login to chroot..."
    ### create flag file on chroot
    touch /opt/gluu-server/root/fresh

    echo "Copying script to setup gluu-server on first login to chroot..."
    ### copy install script to profile
    cp /test-install-data/setupscript.sh /opt/gluu-server/etc/profile.d/.

    echo "Extracting letsencrypt files to chmod..."
    ## extract certificates to fresh install
    tar -zxvf /test-install-data/etcletsencrypt.tar -C /opt/gluu-server

    # Enable, start, login gluu
    gluu-serverd enable
    echo "Starting gluu-serverd..."
    gluu-serverd start
    echo "Loggin in to execute next script..."
    gluu-serverd login

    echo "Deleting flag file /root/freshsnap"
    rm -f /root/freshsnap
fi