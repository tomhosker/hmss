"""
This code sets up the Git credentials for this computer.
"""

# Imports.
import os
import pathlib
import subprocess

# Local constants.
PATH_TO_HOME = str(pathlib.Path.home())
DEFAULT_PATH_TO_LOG = os.path.join(PATH_TO_HOME, "auto_commit.log")
DEFAULT_PATH_TO_GIT_CREDENTIALS = \
    os.path.join(PATH_TO_HOME, ".git-credentials")
DEFAULT_PATH_TO_PAT = \
    os.path.join(PATH_TO_HOME, "personal_access_token.txt")
DEFAULT_USERNAME = "tomhosker"
DEFAULT_EMAIL_ADDRESS = "tomdothosker@gmail.com"

#############
# FUNCTIONS #
#############

def make_github_credential(pat, username=DEFAULT_USERNAME):
    """ Generate a string for a GitHub credential, given a username and a
    personal access token. """
    result = "https://"+username+":"+pat+"@github.com"
    return result

def set_username_and_email_address(
        username=DEFAULT_USERNAME,
        email_address=DEFAULT_EMAIL_ADDRESS
    ):
    """ Set the global Git ID configurations for this device. """
    subprocess.run(
        ["git", "config", "--global", "user.name", username],
        check=True
    )
    subprocess.run(
        ["git", "config", "--global", "user.email", email_address],
        check=True
    )

def set_up_git_credentials(
        username=DEFAULT_USERNAME,
        email_address=DEFAULT_EMAIL_ADDRESS,
        path_to_git_credentials=DEFAULT_PATH_TO_GIT_CREDENTIALS,
        path_to_pat=DEFAULT_PATH_TO_PAT
    ):
    """ Set up GIT credentials, if necessary and possible. """
    set_username_and_email_address(
        username=username,
        email_address=email_address
    )
    if os.path.exists(path_to_pat):
        with open(path_to_pat, "r") as pat_file:
            pat = pat_file.read()
            while pat.endswith("\n"):
                pat = pat[:-1]
        credential = make_github_credential(pat)
        with open(path_to_git_credentials, "w") as credentials_file:
            credentials_file.write(credential)
    elif not os.path.exists(path_to_git_credentials):
        print(
            "Error setting up GIT credentials: could not find PAT at "+
            path_to_pat+" or GIT credentials at "+path_to_git_credentials
        )
        return False
    config_string = "store --file "+path_to_git_credentials
    subprocess.run(
        ["git", "config", "--global", "credential.helper", config_string],
        check=True
    )
    print("GIT credentials set up!")
    return True
