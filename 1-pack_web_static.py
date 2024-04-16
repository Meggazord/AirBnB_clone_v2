#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os

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

if __name__ == "__main__":
    do_pack()
    