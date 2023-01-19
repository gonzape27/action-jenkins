"""
Script to check the status of a Jenkins job
Sets JOB_STATUS in the GITHUB_ENV
"""
#!/usr/bin/env python3
# use of https://python-jenkins.readthedocs.io/en/latest/index.html

from jenkins import Jenkins
from time import sleep
from sys import argv
from os import getenv
from github_utils import write_to_github_env_file

def mandatory_arg(argv):
    if argv == "":
        raise ValueError("Only job_params can be empty. Required fields: url, token, user and path")
    return argv

# mandatory
JENKINS_URL = mandatory_arg(argv[1])
JENKINS_TOKEN = mandatory_arg(argv[2])
JENKINS_USER = mandatory_arg(argv[3])
JOB_PATH = mandatory_arg(argv[4])
BUILD_NUMBER = mandatory_arg(argv[5])

# not mandatory
JOB_PARAMS = argv[6] or '{}'

# create/connect jenkins server
server = Jenkins(f"http://{JENKINS_URL}", username=JENKINS_USER, password=JENKINS_TOKEN)
user = server.get_whoami()
version = server.get_version()

# build job
split = JOB_PATH.split("job/")
job_name = "".join(split)
queue_info = server.get_queue_info()
queue_id = queue_info[0].get('id')

def get_status(name: str, number: int) -> str:
    build_info = server.get_build_info(name=name, number=number)
    job_status = build_info["result"]
    return job_status

while not (status := get_status(job_name, int(BUILD_NUMBER))):
    sleep(1)

# Write status to comms file for GitHub Action
write_to_github_env_file("JOB_STATUS",status)

if status != 'SUCCESS':
    exit(1)
