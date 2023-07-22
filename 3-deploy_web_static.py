#!/usr/bin/env python3
"""
Fabric script that distributes an archive to your web servers
"""
import os
from fabric.api import env, put, run
from datetime import datetime


env.hosts = ['54.209.118.161', '54.165.214.4']



def do_pack():
    """
    Creates a compressed archive of the web_static folder
    """
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(current_time)
        run("mkdir -p versions")
        run("tar -czvf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(e)
        return None


def deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
         # Use the archive_path argument in your function logic
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension> on the web server
        archive_filename = os.path.basename(archive_path)
        archive_folder = "/data/web_static/releases/" + archive_filename.split(".")[0]
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move files from web_static folder to the current release folder
        run("mv {}/web_static/* {}/".format(archive_folder, archive_folder))

        # Remove the web_static folder
        run("rm -rf {}/web_static".format(archive_folder))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        # linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
        run("ln -s {} /data/web_static/current".format(archive_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
