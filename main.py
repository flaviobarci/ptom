import sys
import subprocess
import os

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
subprocess.run(["cp", fileName, "/tmp/submit"])

# Start git on temporary folder
subprocess.run(["git init"], shell=True, cwd="/tmp/submit")
subprocess.run(["git add --all"], shell=True, cwd="/tmp/submit")
subprocess.run(["git commit --allow-empty-message -m ''"],
               shell=True, cwd="/tmp/submit")

subprocess.run(["git push origin master"])

# Clean temporary folder
subprocess.run(["rm", "-rf", "/tmp/submit"])
