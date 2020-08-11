# File /opt/gluu-server/root/certbot.sh
# Works on ubuntu 18
# To be runned on chmod after fresh install
apt-get update -y
apt-get install software-properties-common -y
add-apt-repository universe -y
add-apt-repository ppa:certbot/certbot -y
apt-get update -y
apt-get install certbot python3-certbot-apache -y
# certbot --apache --agree-tos --force-renewal -m chris@gluu.org -n -d t1.techno24x7.com
certbot renew -n
