#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists
import os

env.hosts = ['18.207.2.191', '3.90.83.114']
env.user = 'ubuntu'
env.key_filename = '/Users/Megahed/.ssh/id_rsa'

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
        run('tar -xzf {}{}/ -C /data/web_static/releases/{}/'
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
        print(e)
        return False

if __name__ == "__main__":
    do_deploy()


"""
#def do_deploy(archive_path):
"""    """
    Distributes an archive to your web servers

    Args:
        archive_path (str): Path to the archive file

    Returns:
        bool: True if all operations were successful, False otherwise
    """
"""
    if not exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp')
        archive_name = archive_path.split('/')[-1]
        release_folder = '/data/web_static/releases/' + archive_name [:-4]
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, release_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_folder))
        print("Successful deployment!")
        return True
    
    except Exception as e:
        print("Error:", e)
        return False

if __name__ == "__main__":
    do_deploy("<path_to_archive>")
"""