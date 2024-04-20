#!/usr/bin/python3
"""
Deletes outdated archives based on user input
"""

import os
from fabric.api import *

env.hosts = ['18.207.2.191', '3.90.83.114']

def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number (int): user input of number of archives to keep.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    if len(archives) > number:
        with lcd("versions"):
            [local("rm ./{}".format(a)) for a in archives[:-number]]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        if len(archives) > number:
            [run("rm -rf ./{}".format(a)) for a in archives[:-number]]
