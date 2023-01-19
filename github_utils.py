"""
GitHub Utility functions
"""

from os import getenv

def write_to_github_comms_file(github_file: str, key: str, value: str) -> None:
    '''
    GitHub Actions communicate via config files. File paths are stored in the environment
    allowing us to retrieve the file location and write key/value pairs to it. These values can be retrieved
    from within the GitHub Action script.
    '''
    env_file_handle = getenv("GITHUB_ENV")
    with open(env_file_handle, "a") as env_file:
        env_file.write(f"{key}={value}\n")

def write_to_github_env_file(key: str, value: str) -> None:
    '''
    GitHub environment vars are accessible from within the GitHub Action script
    via ${{ env.key }} where key is the value passed in for key
    '''
    write_to_github_comms_file("GITHUB_ENV", key, value)

def write_to_github_output_file(key: str, value: str) -> None:
    '''
    GitHub output vars are accessible from within the GitHub Action script
    via outputs for the step that called
    '''
    write_to_github_comms_file("GITHUB_OUTPUT", key, value)