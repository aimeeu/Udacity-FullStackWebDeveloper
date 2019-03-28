# udacity-fsnd-proj06
project 6 - final project

create lighsail instance with my own public key
aimeeu-udacity-fsnd-p6

create a static IP and attach to instance
public IP: 34.193.161.246

ssh ubuntu@34.193.161.246



update firewall
https://lightsail.aws.amazon.com/ls/docs/en/articles/understanding-firewall-and-port-mappings-in-amazon-lightsail

use http://xip.io/ to set up DNS



Your README.md file should include all of the following:
i. The IP address and SSH port so your server can be accessed by the reviewer.
ii. The complete URL to your hosted web application.
iii. A summary of software you installed and configuration changes made.
iv. A list of any third-party resources you made use of to complete this project.

Locate the SSH key you created for the grader user.

During the submission process, paste the contents of the grader user's SSH key into the "Notes to Reviewer" field.


How will I complete this project?

This project is linked to the Configuring Linux Web Servers course, which teaches you to secure and set up a Linux server. By the end of this project, you will have one of your web applications running live on a secure web server.

To complete this project, you'll need a Linux server instance. We recommend using Amazon Lightsail for this. If you don't already have an Amazon Web Services account, you'll need to set one up. Once you've done that, here are the steps to complete this project.
Get your server.

1. Start a new Ubuntu Linux server instance on Amazon Lightsail. There are full details on setting up your Lightsail instance on the next page.
2. Follow the instructions provided to SSH into your server.
Secure your server.

3. Update all currently installed packages.
4. Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.
5. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

    Warning: When changing the SSH port, make sure that the firewall is open for port 2200 first, so that you don't lock yourself out of the server. When you change the SSH port, the Lightsail instance will no longer be accessible through the web app 'Connect using SSH' button. The button assumes the default port is being used. There are instructions on the same page for connecting from your terminal to the instance. Connect using those instructions and then follow the rest of the steps.

Give grader access.

In order for your project to be reviewed, the grader needs to be able to log in to your server.

6. Create a new user account named grader.
7. Give grader the permission to sudo.
8. Create an SSH key pair for grader using the ssh-keygen tool.
Prepare to deploy your project.

9. Configure the local timezone to UTC.
10. Install and configure Apache to serve a Python mod_wsgi application.

    If you built your project with Python 3, you will need to install the Python 3 mod_wsgi package on your server: sudo apt-get install libapache2-mod-wsgi-py3.

11. Install and configure PostgreSQL:

    Do not allow remote connections
    Create a new database user named catalog that has limited permissions to your catalog application database.

12. Install git.
Deploy the Item Catalog project.

13. Clone and setup your Item Catalog project from the Github repository you created earlier in this Nanodegree program.
14. Set it up in your server so that it functions correctly when visiting your server’s IP address in a browser. Make sure that your .git directory is not publicly accessible via a browser!


