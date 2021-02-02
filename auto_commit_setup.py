"""
This code defines a script which ensures that the code in the file
"auto_commit_changes.py" is executed on every start-up.
"""

# Imports.
import os

# Local imports.
from auto_commit_changes import PATH_TO_HOME, PATH_TO_GIT_CREDENTIALS

# Local constants.
PATH_TO_PAT = os.path.join(PATH_TO_HOME, "personal_access_token.txt")
GIT_USERNAME = "tomhosker"
CRONTAB_ADDITION = "@reboot python /bin/auto_commit_changes.py &"

#############
# FUNCTIONS #
#############

def make_github_credential(pat, username=GIT_USERNAME):
    """ Generate a string for a GitHub credential, given a username and a
    personal access token. """
    result = "https://"+username+":"+pat+"@github.com"
    return result

def set_up_git_credentials(path_to_git_credentials=PATH_TO_GIT_CREDENTIALS,
                           path_to_pat=PATH_TO_PAT):
    """ Set up GIT credentials, if necessary and possible. """
    if os.path.exists(path_to_git_credentials):
        return True
    elif os.path.exists(path_to_pat):
        with open(path_to_pat, "r") as pat_file:
            pat = pat_file.read()
            while pat.endswith("\n"):
                pat = pat[:-1]
        credential = make_github_credential(pat)
        with open(path_to_credentials, "w") as credentials_file:
            credentials_file.write(credential)
        return True
    return False

def set_up_crontab(addition=CRONTAB_ADDITION):
    """ Make the required additon to the root's Crontab. """
    os.system("sudo crontab -l > mycron")
    with open("mycron", "r") as mycron_file:
        mycron_readout = mycron_file.read()
    if addition in mycron_readout:
        os.remove("mycron")
        return
    mycron_new = mycron_readout+"\n"+addition+"\n"
    with open("mycron", "w") as mycron_file:
        mycron_file.write(mycron_new)
    os.system("sudo crontab mycron >/dev/null")
    os.remove("mycron")

def set_up_auto_commit():
    """ Wrap the above into one function. """
    set_up_git_credentials()
    os.system("sudo cp -f auto_commit_changes.py /bin")
    set_up_crontab()
    print("Added auto commit script to Crontab.")

###################
# RUN AND WRAP UP #
###################

def run():
    set_up_auto_commit()

if __name__ == "__main__":
    run()
