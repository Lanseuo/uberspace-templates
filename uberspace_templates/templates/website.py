import os

from uberspace_templates import utils


def create(name):
    git_folder = "/home/{}/projects/git/".format(utils.get_username()) + name + ".git/"
    git_folder = input("Git Folder ({}): ".format(git_folder)) or git_folder

    domain = utils.ask_domain()

    print("\nCreate git folder ({})".format(git_folder))
    os.system("mkdir -p {}".format(git_folder))

    print("\nInitialize git folder")
    os.system("git init --bare {}".format(git_folder))

    print("\nAdd post-receive file to git hooks")
    with open(git_folder + "hooks/post-receive", "w") as f:
        f.write("""#!/bin/sh
set -e

PROJECT_PATH="/var/www/virtual/""" + utils.get_username() + """/""" + domain + """\"
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
""")
    os.system("chmod +x " + git_folder + "hooks/post-receive")

    utils.add_htaccess(domain)

    utils.add_uberspace_domain(domain)

    print("\nTODO LOCAL")
    print("git remote add live uberspace:" + git_folder[:-1])
