# FILE: gluu.sh
# Should be placed on /etc/profile.d of gluu w/ passport snapshot

if [ -f /root/freshsnap ]
then
    ### Ads and install package for ubuntu 18
    echo "deb https://repo.gluu.org/ubuntu/ bionic main" > /etc/apt/sources.list.d/gluu-repo.list
    curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
    apt update -y
    apt install gluu-server=4.2.0~bionic -y
    apt-mark hold gluu-server -y
    ### copy setup files to chmod
    cp /test-install-data/setup.properties /opt/gluu-server/install/community-edition-setup/.
    ### In case of 4.2.0 needs setup.py
    cp /test-install-data/setup.py /opt/gluu-server/install/community-edition-setup/.
    ### Templates
    cp /test-install-data/templates/*.* /opt/gluu-server/install/community-edition-setup/templates/.
    ### Certbot to root chmod
    cp /test-install-data/certbot.sh /opt/gluu-server/root/.

    ### create flag file on chroot
    touch /opt/gluu-server/root/fresh

    ### copy install script to profile
    cp /test-install-data/setupscript.sh /opt/gluu-server/etc/profile.d/.

    # Enable, start, login gluu
    gluu-serverd enable
    gluu-serverd start
    gluu-serverd login

    rm -f /root/freshsnap
fi



