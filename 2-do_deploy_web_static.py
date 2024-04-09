#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric import *
from os.path import exists

env.hosts = ['18.207.2.191', '3.90.83.114']
env.user = 'ubuntu'
env.key_filename = '/Users/Megahed/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    Args:
        archive_path (str): Path to the archive file
    Returns:
        bool: True if all operations were successful, False otherwise
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


