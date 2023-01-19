#!/usr/bin/env python3

# use of https://python-jenkins.readthedocs.io/en/latest/index.html

import sys
import requests
import jenkins
import time
import json
import os
from github_utils import write_to_github_env_file

def mandatory_arg(argv):
    if argv == "":
        raise ValueError("Only job_params can be empty. Required fields: url, token, user and path")
    return argv

# mandatory
JENKINS_URL = mandatory_arg(sys.argv[1])
JENKINS_TOKEN = mandatory_arg(sys.argv[2])
JENKINS_USER = mandatory_arg(sys.argv[3])
JOB_PATH = mandatory_arg(sys.argv[4])

# not mandatory
JOB_PARAMS = sys.argv[5] or '{}'

# create/connect jenkins server
server = jenkins.Jenkins(f"http://{JENKINS_URL}", username=JENKINS_USER, password=JENKINS_TOKEN)
user = server.get_whoami()
version = server.get_version()

# build job
split = JOB_PATH.split("job/")
job_name = "".join(split)
server.build_job(job_name, parameters=json.loads(JOB_PARAMS), token=JENKINS_TOKEN)
queue_info = server.get_queue_info()
queue_id = queue_info[0].get('id')

def get_trigger_info(url: str):
    trigger_info = requests.get(url).json()
    return trigger_info

# define url to request build_number
url = f"http://{JENKINS_USER}:{JENKINS_TOKEN}@{JENKINS_URL}/queue/item/{queue_id}/api/json?pretty=true"
while "executable" not in (info := get_trigger_info(url)):
    time.sleep(3)

# Write status to comms file for GitHub Action
build_number = info["executable"]["number"]
build_url = info["executable"]["url"]
write_to_github_env_file("BUILD_NUMBER",build_number)
write_to_github_env_file("BUILD_URL",build_url)
