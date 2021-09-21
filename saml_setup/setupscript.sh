### FILE: /opt/gluu-server/root/setupscript.sh
### Inside chroot, run setup and take care of letsencrypt certs

### check for flag file
if [ -f /root/fresh ]
then
    cd /install/community-edition-setup
    ./setup.py -c -n
    cd /root
    bash certbot.sh
    rm -f /root/fresh
    logout
fi
