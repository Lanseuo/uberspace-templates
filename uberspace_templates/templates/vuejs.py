import os

from uberspace_templates import utils


def create(name):
    git_folder = "/home/{}/projects/git/".format(utils.get_username()) + name + ".git/"
    git_folder = input("Git Folder ({}): ".format(git_folder)) or git_folder

    domain = utils.ask_domain()

    os.system("mkdir /home/{}/tmp".format(utils.get_username()))

    print("\nCreate git folder ({})".format(git_folder))
    os.system("mkdir -p {}".format(git_folder))

    print("\nInitialize git folder")
    os.system("git init --bare {}".format(git_folder))

    print("\nAdd post-receive file to git hooks")
    with open(git_folder + "hooks/post-receive", "w") as f:
        f.write("""#!/bin/sh
set -e

# Use new nodejs version
export PATH=/package/host/localhost/nodejs-9.2.0/bin:$PATH

GIT_PATH=\"""" + git_folder + """\"
TMP_PATH="/home/""" + utils.get_username() + """/tmp/""" + name + """\"
WEB_ROOT_PATH="/var/www/virtual/""" + utils.get_username() + """/""" + domain + """\"

mkdir -p $TMP_PATH

cd $GIT_PATH
if ! [ -t 0 ]; then
    read -a ref
fi
IFS='/' read -ra REF <<< "${ref[2]}"
branch="${REF[2]}"
GIT_WORK_TREE=$TMP_PATH git checkout -f $branch

cd $TMP_PATH
echo ---INSTALL DEPENDENCIES---
npm install
echo ---BUILD FOR PRODUCTION---
npm run build

echo ---DELTE OLD FILES FROM WEBROOT---
cd $WEB_ROOT_PATH
rm -rf *

echo ---COPY DIST FILES TO WEBROOT---
cd ${TMP_PATH}/dist
cp -r * $WEB_ROOT_PATH

echo ---DELETE TEMPORARY NOT BUILT FILES
cd $TMP_PATH
cd ..
rm -r """ + name)
    os.system("chmod +x " + git_folder + "hooks/post-receive")

    utils.add_uberspace_domain(domain)
    utils.add_htaccess(domain)

    print("\nTODO LOCAL")
    print("git remote add live uberspace:" + git_folder[:-1])
