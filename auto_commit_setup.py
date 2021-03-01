"""
This code defines a script which ensures that the code in the file
"auto_commit_changes.py" is executed on every start-up.

Run me with `python3 auto_commit_setup.py`, or with `python3
auto_commit_setup.py --undo` to undo the former.
"""

# Imports.
import os
import sys

# Local imports.
from auto_commit_changes import PATH_TO_HOME, PATH_TO_GIT_CREDENTIALS

# Local constants.
DEFAULT_PATH_TO_PAT = os.path.join(PATH_TO_HOME,
                                   "personal_access_token.txt")
GIT_USERNAME = "tomhosker"
CRONTAB_ADDITION = "@reboot python3 /bin/auto_commit_changes.py &"

#############
# FUNCTIONS #
#############

def make_github_credential(pat, username=GIT_USERNAME):
    """ Generate a string for a GitHub credential, given a username and a
    personal access token. """
    result = "https://"+username+":"+pat+"@github.com"
    return result

def set_up_git_credentials(path_to_git_credentials=PATH_TO_GIT_CREDENTIALS,
                           path_to_pat=DEFAULT_PATH_TO_PAT):
    """ Set up GIT credentials, if necessary and possible. """
    if os.path.exists(path_to_git_credentials):
        pass
    elif os.path.exists(path_to_pat):
        with open(path_to_pat, "r") as pat_file:
            pat = pat_file.read()
            while pat.endswith("\n"):
                pat = pat[:-1]
        credential = make_github_credential(pat)
        with open(path_to_git_credentials, "w") as credentials_file:
            credentials_file.write(credential)
    else:
        return False
    os.system("git config --global credential.helper \"store --file "+
              PATH_TO_GIT_CREDENTIALS+"\"")
    return True

def set_up_crontab(addition=CRONTAB_ADDITION):
    """ Make the required additon to the root's Crontab. """
    os.system("crontab -l > mycron")
    with open("mycron", "r") as mycron_file:
        mycron_readout = mycron_file.read()
    if addition in mycron_readout:
        os.remove("mycron")
        return
    mycron_new = mycron_readout+"\n"+addition+"\n"
    with open("mycron", "w") as mycron_file:
        mycron_file.write(mycron_new)
    os.system("crontab mycron >/dev/null")
    os.remove("mycron")

def set_up_auto_commit(path_to_pat=DEFAULT_PATH_TO_PAT):
    """ Wrap the above into one function. """
    if not set_up_git_credentials():
        print("No personal access token found, and therefore no auto-"+
              "commits could be set up.")
        return False
    os.system("sudo cp -f auto_commit_changes.py /bin")
    set_up_crontab()
    print("Added auto commit script to Crontab.")
    return True

def remove_from_crontab(item=CRONTAB_ADDITION):
    """ Remove a given item from Crontab. """
    os.system("crontab -l > mycron")
    with open("mycron", "r") as mycron_file:
        mycron_readout = mycron_file.read()
    mycron_new = mycron_readout.replace(item, "")
    with open("mycron", "w") as mycron_file:
        mycron_file.write(mycron_new)
    os.system("crontab mycron >/dev/null")
    os.remove("mycron")

def remove_auto_commit():
    """ Undo the above setup function. """
    remove_from_crontab()
    print("Item removed from Crontab. GitHub credentials unchanged.")

###################
# RUN AND WRAP UP #
###################

def run():
    if "--undo" in sys.argv:
        remove_auto_commit()
    else:
        set_up_auto_commit()

if __name__ == "__main__":
    run()
