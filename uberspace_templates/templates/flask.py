import os
import subprocess

from uberspace_templates import utils


def create(name):
    project_folder = "/home/{}/projects/".format(utils.get_username()) + name + "/"
    project_folder = input("Project Folder ({}): ".format(project_folder)) or project_folder

    git_folder = "/home/{}/projects/git/".format(utils.get_username()) + name + ".git/"
    git_folder = input("Git Folder ({}): ".format(git_folder)) or git_folder

    log_folder = input("Log Folder (/home/{}/projects/data/".format(utils.get_username()) + name +
                       "/logs/): ") or "/home/{}/projects/data/".format(utils.get_username()) + name + "/logs/"

    domain = utils.ask_domain()

    print("\nCreate project folder ({})".format(project_folder))
    os.system("mkdir -p {}".format(project_folder))

    print("\nCreate git folder ({})".format(git_folder))
    os.system("mkdir -p {}".format(git_folder))

    print("\nCreate log folder ({})".format(log_folder))
    os.system("mkdir -p {}".format(log_folder))

    print("\nInitialize git folder ({})".format(git_folder))
    os.system("git init --bare {}".format(git_folder))

    print("\nAdd post-receive file to git hooks")
    with open(git_folder + "hooks/post-receive", "w") as f:
        f.write("""#!/bin/sh
set -e

PROJECT_PATH=\"""" + project_folder + """\"
GIT_PATH=\"""" + git_folder + """\"

cd $PROJECT_PATH

echo ---DELETE OLD FILES---
rm -rf *

cd $GIT_PATH
if ! [ -t 0 ]; then
    read -a ref
fi
IFS='/' read -ra REF <<< "${ref[2]}"
branch="${REF[2]}"
GIT_WORK_TREE=$TMP_PATH git checkout -f $branch

cd $PROJECT_PATH

echo ---CREATE VIRTUALENV---
virtualenv venv -p python3

echo ---INSTALL REQUIREMENTS---
venv/bin/pip3 install -r requirements.txt
venv/bin/pip3 install gunicorn

echo ---CREATE config.py AND COPY CONTENT---
cp ${GIT_PATH}/config.py ${PROJECT_PATH}/config.py
""")
    os.system("chmod +x " + git_folder + "hooks/post-receive")
    os.system("touch " + git_folder + "config.py")

    port = utils.ask_and_find_port()

    package_function = input("\nPackage and Function (app:app): ") or "app:app"

    print("\nCreate daemon")
    os.system("mkdir -p ~/etc/run-{}".format(name))
    print("~/etc/run-" + name + "/run")
    with open("/home/{}/etc/run-".format(utils.get_username()) + name + "/run", "w") as f:
        f.write("""#!/bin/sh
{project_folder}venv/bin/gunicorn --reload --access-logfile {log_folder}gunicorn_access.log --error-logfile {log_folder}gunicorn.log --log-file {log_folder}gunicorn.log --chdir {project_folder} --bind 127.0.0.1:{port} {package_function}
""".format(project_folder=project_folder, log_folder=log_folder, port=port, package_function=package_function))
    os.system("chmod +x /home/{}/etc/run-".format(utils.get_username()) + name + "/run")
    os.system("mkdir -p /home/{}/etc/run-".format(utils.get_username()) + name + "/log")
    with open("/home/{}/etc/run-".format(utils.get_username()) + name + "/log/run", "w") as f:
        f.write("""#!/bin/sh
exec multilog t ./main""")
    os.system("chmod +x /home/{}/etc/run-".format(utils.get_username()) + name + "/log/run")
    os.system("ln -s /home/{}/etc/run-".format(utils.get_username()) +
              name + " /home/{}/service/".format(utils.get_username()) + name)

    utils.add_uberspace_domain(domain)
    utils.add_htaccess(domain, reverse_proxy_port=port)

    print("\nTODO ON SERVER")
    print("nano " + git_folder + "config.py")

    print("\nTODO LOCAL")
    print("git remote add live uberspace:" + git_folder[:-1])
