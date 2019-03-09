#
#
#
#

import sys
import subprocess
import os
import getpass
from github import Github
from github import GithubException

# Check if an arg was passed
if not len(sys.argv) > 1:
    print('No file specified.')
    sys.exit(1)

# TODO: Check if git is installed

# Get file name
fileName = sys.argv[1]

# Check if file exists
if not os.path.isfile(fileName):
    print('Could not find file')
    sys.exit(1)

# Get confirmation for the process
answer = input('Would you like to upload ' + fileName + '? (y/n) ')
if answer == 'n':
    print('Exiting...')
    sys.exit(1)

# TODO: extract temprary folder path to variable

# Setup temporary folder
subprocess.run(["mkdir", "/tmp/submit"])

# Get user credentials
username = input('Github username: ')
password = getpass.getpass()

# Authenticate user with github
g = Github(username, password)
user = g.get_user()
org = g.get_organization("tomsk-submit")

repo = None

# TODO: Verify if user is in the org

try:
    repo = org.get_repo(user.login)
    subprocess.run(
        [f"git clone {repo.clone_url} ."], shell=True, cwd="/tmp/submit")
    subprocess.run(["rm -r /tmp/submit/*"], shell=True)
    subprocess.run(["cp", fileName, "/tmp/submit"])
    subprocess.run(["git add --all"], shell=True, cwd="/tmp/submit")
    subprocess.run(["git commit --allow-empty-message -m ''"],
                   shell=True, cwd="/tmp/submit")
except GithubException as e:
    # Github repo creation. Should be done only if it does not exist
    repo = org.create_repo(
        user.login,
        allow_rebase_merge=True,
        auto_init=False,
        description="Automated repo",
        has_issues=True,
        has_projects=False,
        has_wiki=False,
        private=False,
    )
    # Start git on temporary folder
    subprocess.run(["git init"], shell=True, cwd="/tmp/submit")
    subprocess.run(["git add --all"], shell=True, cwd="/tmp/submit")
    subprocess.run(["git commit --allow-empty-message -m ''"],
                   shell=True, cwd="/tmp/submit")

# Push all content to github. Only for freshly created repos
subprocess.run(
    [f"git push -u https://{username}:{password}@github.com/tomsk-submit/{username}.git master"],
    shell=True,
    cwd="/tmp/submit", stdout=subprocess.DEVNULL)

# Clean temporary folder
subprocess.run(["rm", "-rf", "/tmp/submit"])
