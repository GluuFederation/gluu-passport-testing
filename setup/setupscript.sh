### Inside chroot

### check for flag file
if [ -f /root/fresh ]
then
    cd /install/community-edition-setup
    python setup.py -c -n
    cd /root
    bash certbot.sh
    rm -f /root/fresh
fi
