# FILE /test-install-data/prepare.sh
#
# Dev propused file
# Put every file in the right folder b4 boot script and other stuff
apt install moreutils -y
mv 9gluu /etc/init.d/.
update-rc.d 9gluu defaults
touch /root/freshsnap