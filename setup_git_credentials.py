"""
This code sets up the GIT credentials for this computer.
"""

# Imports.
import os
import pathlib

# Local constants.
PATH_TO_HOME = str(pathlib.Path.home())
DEFAULT_PATH_TO_LOG = os.path.join(PATH_TO_HOME, "auto_commit.log")
DEFAULT_PATH_TO_GIT_CREDENTIALS = os.path.join(
                                      PATH_TO_HOME, ".git-credentials")
DEFAULT_PATH_TO_PAT = os.path.join(
                          PATH_TO_HOME, "personal_access_token.txt")
DEFAULT_USERNAME = "tomhosker"

#############
# FUNCTIONS #
#############

def make_github_credential(pat, username=DEFAULT_USERNAME):
    """ Generate a string for a GitHub credential, given a username and a
    personal access token. """
    result = "https://"+username+":"+pat+"@github.com"
    return result

def set_up_git_credentials(
        path_to_git_credentials=DEFAULT_PATH_TO_GIT_CREDENTIALS,
        path_to_pat=DEFAULT_PATH_TO_PAT):
    """ Set up GIT credentials, if necessary and possible. """
    if os.path.exists(path_to_pat):
        with open(path_to_pat, "r") as pat_file:
            pat = pat_file.read()
            while pat.endswith("\n"):
                pat = pat[:-1]
        credential = make_github_credential(pat)
        with open(path_to_git_credentials, "w") as credentials_file:
            credentials_file.write(credential)
    elif not os.path.exists(path_to_git_credentials):
        print("Error setting up GIT credentials: could not find PAT at "+
              path_to_pat+" or GIT credentials at "+path_to_git_credentials)
        return False
    os.system("git config --global credential.helper \"store --file "+
              path_to_git_credentials+"\"")
    print("GIT credentials set up!")
    return True

###################
# RUN AND WRAP UP #
###################

def run():
    set_up_git_credentials()

if __name__ == "__main__":
    run()
