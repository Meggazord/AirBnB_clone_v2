#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists
import os

env.hosts = ['18.207.2.191', '3.90.83.114']
env.user = 'ubuntu'
env.key_filename = '/Users/Megahed/.ssh/id_rsa'

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
    Distributes an archive to the web servers and deploys it

    Args:
        archive_path (str): Path to the archive to deploy

    Returns:
        bool: True if all operations were done correctly, False otherwise
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_name_no_ext = os.path.splitext(archive_name)[0]
        remote_tmp = '/tmp/'
        put(archive_path, remote_tmp)
        run('mkdir -p /data/web_static/releases/{}/'
            .format(archive_name_no_ext))
        run('tar -xzf {}{} -C /data/web_static/releases/{}/'
            .format(remote_tmp, archive_name, archive_name_no_ext))
        run('rm {}{}'.format(remote_tmp, archive_name))
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'
            .format(archive_name_no_ext, archive_name_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_name_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_name_no_ext))
        print("New version deployed!")
        return True

    except Exception as e:
        print("Error: {}".format(e))
        return False

def deploy():
    """
    Executes full deployment process
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

if __name__ == "__main__":
    deploy()
