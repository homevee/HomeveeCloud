#Update
sudo apt-get update
sudo apt-get upgrade -y

#Install pip
sudo apt install python3-pip -y
sudo apt-get install libapache2-mod-wsgi python-dev apache2 -y
sudo a2enmod wsgi
sudo service apache2 restart

#Install certbot
sudo apt-get install certbot -y

sudo apt-get install python-certbot-apache -y

#Install cert
certbot certonly --standalone -d cloud.homevee.de
certbot certonly --apache -d cloud.homevee.de

#Insert renewing cronjob
#certbot certonly --force-renew --apache --cert-name smarthome-blogger.de -d smarthome-blogger.de

#Install dependencies
sudo pip3 install mysql-connector
sudo pip3 install pyfcm
sudo pip3 install passlib
sudo pip3 install flask
sudo pip3 install azure-iothub-service-client
sudo pip3 install azure-iothub-device-client

######FLASK APACHE DEPLOYMENT######

 nano /etc/apache2/sites-available/HomeveeCloud.conf

 <VirtualHost *:80>
	ServerName cloud.homevee.de
	ServerAdmin support@homevee.de
	WSGIScriptAlias / /var/www/HomeveeCloud/homevee-cloud.wsgi
	<Directory /var/www/HomeveeCloud/HomeveeCloud/>
		Order allow,deny
		Allow from all
	</Directory>
	#Alias /static /var/www/HomeveeCloud/HomeveeCloud/static
	#<Directory /var/www/HomeveeCloud/HomeveeCloud/static/>
	#	Order allow,deny
	#	Allow from all
	#</Directory>
	ErrorLog ${APACHE_LOG_DIR}/error.log
	LogLevel warn
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

a2ensite HomeveeCloud

nano /var/www/HomeveeCloud/homevee-cloud.wsgi

#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/HomeveeCloud/")

from FlaskApp import app as application
application.secret_key = 'Add your secret key'

#disable apache2 on boot

sudo update-rc.d apache2 disable