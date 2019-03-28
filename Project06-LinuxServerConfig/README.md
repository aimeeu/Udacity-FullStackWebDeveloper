# Udacity Full Stack Web Developer Project 6 - Linux Server Configuration
## Udacity Reviewer

SSH Address: 18.211.87.104

SSH Port: 2200

Account: grader

URL of Hosted Web Application: http://18.211.87.104 (uses Github authorization)

## Cloud Server

- Amazon Lightsail server 512 MB RAM, 1 vCPU, 20 GB SSD
- Ubuntu 18.04 LTS

## Summary of Configuration

### Lightsail Configuration

![lightsail-main](/docs/lightsail-main.png)

1. Create/attach static IP

2. Configure Lightsail firewall; note: I enabled https in case I want to install an SSL certificate in the future.

	![project6-networking](/docs/project6-networking.png)

## Summary of Software Installed
- aptitude
- ufw
- apache2
- libapache2-mod-wsgi-py3
- python3-dev
- python3-pip
- my udacity-fsnd-proj06 Catalog and required packages

### Server Configuration 

#### Update OS

```
ubuntu@ip-172-26-1-224:~$ sudo apt-get update
ubuntu@ip-172-26-1-224:~$ sudo apt-get dist-upgrade
```
#### Set Local Time to UTC

```
ubuntu@ip-172-26-1-224:~$ sudo timedatectl set-timezone UTC
ubuntu@ip-172-26-1-224:~$ timedatectl
                      Local time: Tue 2018-12-11 17:23:42 UTC
                  Universal time: Tue 2018-12-11 17:23:42 UTC
                        RTC time: Tue 2018-12-11 17:23:43
                       Time zone: UTC (UTC, +0000)
       System clock synchronized: yes
systemd-timesyncd.service active: yes
                 RTC in local TZ: no
```

#### Add Grader User

```
ubuntu@ip-172-26-1-224:~$ sudo adduser grader
Adding user `grader' ...
Adding new group `grader' (1001) ...
Adding new user `grader' (1001) with group `grader' ...
Creating home directory `/home/grader' ...
Copying files from `/etc/skel' ...
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
Changing the user information for grader
Enter the new value, or press ENTER for the default
	Full Name []: Udacity Grader
	Room Number []: 
	Work Phone []: 
	Home Phone []: 
	Other []: 
Is the information correct? [Y/n] y
ubuntu@ip-172-26-1-224:~$ sudo usermod -aG sudo grader
```
#### Add SSH Key to Authorized Keys
On my laptop, I generated a new SSH key using the ssh-keygen tool. The I added the new key to the ssh-agent before adding they public key to the grader's authorized_keys file.
```
ubuntu@ip-172-26-1-224:~$ cd /home/grader
ubuntu@ip-172-26-1-224:/home/grader$ sudo mkdir .ssh
ubuntu@ip-172-26-1-224:/home/grader$ cd .ssh
ubuntu@ip-172-26-1-224:/home/grader/.ssh$ sudo nano authorized_keys
```
#### Install, Configure, and Enable the Uncomplicated Firewall (ufw)

```
ubuntu@ip-172-26-1-224:~$ sudo aptitude install ufw
ubuntu@ip-172-26-1-224:/home/grader/.ssh$ sudo ufw allow 2200
Rules updated
Rules updated (v6)
ubuntu@ip-172-26-1-224:/home/grader/.ssh$ sudo ufw allow http
Rules updated
Rules updated (v6)
ubuntu@ip-172-26-1-224:/home/grader/.ssh$ sudo ufw allow https
Rules updated
Rules updated (v6)
ubuntu@ip-172-26-1-224:/home/grader/.ssh$ sudo ufw allow 123
Rules updated
Rules updated (v6)
ubuntu@ip-172-26-1-224:~$ sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
ubuntu@ip-172-26-1-224:~$ sudo ufw status
Status: active
```
Note: I enabled https in case I want to install an SSL certificate in the future.

#### Modify sshd_config

Modify sshd_config to listen on port 2200 and to not allow root access:

- AllowUsers ubuntu grader

- Port 2200
- PermitRootLogin no

```
ubuntu@ip-172-26-1-224:~$ sudo nano /etc/ssh/sshd_config
ubuntu@ip-172-26-1-224:~$ sudo reboot
```
Verify grader ssh access:
```
aimeeu@aimeeu-7520:~$ ssh grader@18.211.87.104 -p 2200
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-1029-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed Dec 12 18:27:45 UTC 2018

  System load:  0.0                Processes:           88
  Usage of /:   10.8% of 19.32GB   Users logged in:     0
  Memory usage: 44%                IP address for eth0: 172.26.1.224
  Swap usage:   0%

 * MicroK8s is Kubernetes in a snap. Made by devs for devs.
   One quick install on a workstation, VM, or appliance.

   - https://bit.ly/microk8s

 * Full K8s GPU support is now available! Get it in MicroK8s, CDK,
   and on GKE with Ubuntu workers.

   - https://blog.ubuntu.com/2018/12/10/using-gpgpus-with-kubernetes


  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

0 packages can be updated.
0 updates are security updates.


Last login: Tue Dec 11 17:20:48 2018 from 99.129.239.198
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.
```

#### Install Apache2, WSGI
```
ubuntu@ip-172-26-1-224:~$ sudo apt-get install apache2
ubuntu@ip-172-26-1-224:~$ apachectl -V
Server version: Apache/2.4.29 (Ubuntu)
Server built:   2018-10-10T18:59:25
Server's Module Magic Number: 20120211:68
Server loaded:  APR 1.6.3, APR-UTIL 1.6.1
Compiled using: APR 1.6.3, APR-UTIL 1.6.1
Architecture:   64-bit
Server MPM:     event
  threaded:     yes (fixed thread count)
    forked:     yes (variable process count)
ubuntu@ip-172-26-1-224:~$ sudo apt-get install libapache2-mod-wsgi-py3 python3-dev
ubuntu@ip-172-26-1-224:~$ sudo a2enmod wsgi
ubuntu@ip-172-26-1-224:~$ sudo apache2ctl restart 
ubuntu@ip-172-26-1-224:~$ sudo apache2ctl -M|grep -i wsgi
 wsgi_module (shared)
ubuntu@ip-172-26-1-224:~$ sudo ufw app list
Available applications:
  Apache
  Apache Full
  Apache Secure
  OpenSSH
ubuntu@ip-172-26-1-224:~$ sudo ufw allow 'Apache Full'
Rules updated
Rules updated (v6)
```

#### Install Pip3
```
ubuntu@ip-172-26-1-224:~$ sudo apt-get install python3-pip
ubuntu@ip-172-26-1-224:~$ which pip3
/usr/bin/pip3
```

#### Clone udacity-fsnd-proj06
On my laptop, I cloned my udacity_fsnd_proj4_item_catalog and modified file paths in application.py to be absolute. Then I created a new repo and pushed the modified code.
On the server, I cloned the new repo, renamed it to catalog  and then copied the directory to the Apache directory  /var/www/catalog.  I removed all files not needed to set up and run the application. I also changed ownership of the /var/www/catalog directory to the ubuntu account to enable writing to the SQLite database. 
```
ubuntu@ip-172-26-1-224:/var/www$ sudo chown -R ubuntu:ubuntu /var/www/catalog
```

#### Create WSGI Conf Files
Create catalog.wsgi file in /var/www/catalog. The OAUTH_INSECURE_TRANSPORT variable is needed by Flask-Dance for authorization without SSL. Note: this is done only for testing; a production application should have a proper SSL certificate installed.
```
# flask-dance 
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# add your python files to the python path; this is needed to find the application.py file (where your flask app is located)
import sys
sys.path.insert(0, '/var/www/catalog')

# tell the application where the root is - required for loading templates.
from application import app as application
application.root_path = '/var/www/catalog'
```

Create a catalog.conf configuration file for WSGI in /etc/apache2/sites-available with content:
```
<VirtualHost *:80>
   ServerName 18.211.87.104
   ServerAdmin aimeeu.opensource@gmail.com
   SetEnv OAUTHLIB_INSECURE_TRANSPORT 1
   WSGIDaemonProcess catalog user=ubuntu group=ubuntu threads=2
   WSGIScriptAlias / /var/www/catalog/catalog.wsgi
   <Directory /var/www/catalog>
     WSGIProcessGroup catalog
     WSGIApplicationGroup %{GLOBAL}
     <IfVersion < 2.4>
        Order allow,deny
        Allow from all
     </IfVersion>
     <IfVersion >= 2.4>
        Require all granted
      </IfVersion>
   </Directory>
   Alias "/static/" "/var/www/catalog/static/"
   <Directory /var/www/catalog/static/>
     <IfVersion < 2.4>
        Order allow,deny
        Allow from all
     </IfVersion>
     <IfVersion >= 2.4>
        Require all granted
      </IfVersion>
   </Directory>
   ErrorLog ${APACHE_LOG_DIR}/error.log
   LogLevel info
   CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Enable the catalog wsgi application:
```
ubuntu@ip-172-26-1-224:/etc/apache2/sites-available# sudo a2ensite catalog
Enabling site catalog.
To activate the new configuration, you need to run:
  systemctl reload apache2
```
####  Install and Populate Catalog Application
From the /var/www/catalog directory, install the required python packages using pip3:
```
ubuntu@ip-172-26-1-224:~/var/www/catalog$ pip3 install --user -r requirements.txt
```
Then create and populate the database:
```
ubuntu@ip-172-26-1-224:/var/www/catalog$ python3 application.py --setup
```
Finally, reload apache2:
```
ubuntu@ip-172-26-1-224:/var/www/catalog$ sudo systemctl reload apache2
```
#### Test the Catalog Application

![app-running](/docs/app-running.png)

## Third-Party Resources Used For This Project

- My own notes from working with Centos and Ubuntu servers
- StackOverflow
- Google search engine
- https://wsgi.readthedocs.io/en/latest/
- https://modwsgi.readthedocs.io/en/develop/
- Flask Dance [docs](https://flask-dance.readthedocs.io/en/latest/)
- Flask mod_wsgi deployment [docs](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/)

## Future Enhancements

- Refactor the application to be scaleable
- Dockerize the application 
- Deploy application and database as separate containers using docker-compose on a single server
- Create a Helm chart and deploy on Kubernetes

