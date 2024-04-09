#!/usr/bin/env bash
# Prepare web servers for deployment of web_static

if ! dpkg -s nginx &> /dev/null; then
    sudo apt update
    sudo apt install nginx -y
fi

mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "<html>
<head>
</head>
<body>
    Welcome to the Matrix!
</body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data
config_path="/etc/nginx/sites-available/default"
sed -i "/listen 80 default_server;/a location /hbnb_static/ {\\n    alias /data/web_static/current/;\\n}" $config_path
service nginx restart

# Python script for creating and deploying the archive
# Define Python script content here
python_script_content='''#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import *
from datetime import datetime
from os.path import exists
import os

env.hosts = ['18.207.2.191']
env.user = 'ubuntu'
env.key_filename = '/Users/Megahed/.ssh/id_rsa''

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder

    Returns:
        str: Archive path if generated successfully, None otherwise
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return os.path.abspath("versions/{}".format(archive_name))

    except Exception as e:
        print("Error:", e)
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers and deploys it
    """
    if not exists(archive_path):
        return False
    
    try:
        put(archive_path, '/tmp')
        archive_name = archive_path.split('/')[-1]
        release_folder = '/data/web_static/releases/' + archive_name[:-4]
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, release_folder))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))
        run('rm -rf {}/web_static'.format(release_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_folder))
        return True
    except Exception as e:
        print("Error:", e)
        return False

def deploy():
    """
    Executes full deployment process
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deplo
