"""
This code commits any uncommitted changes within any of the directories
listed below, and in an automated fashion.
"""

# Standard imports.
import os
import pathlib
import subprocess
from datetime import datetime

# Local constants.
DIRECTORIES = ["chancery", "chancery-b", "hgmj", "hoskers-almanack",
               "kingdom-of-cyprus"]
PATH_TO_HOME = str(pathlib.Path.home())
DEFAULT_PATH_TO_LOG = os.path.join(PATH_TO_HOME, "auto_commit.log")
PATH_TO_GIT_CREDENTIALS = os.path.join(PATH_TO_HOME, ".git-credentials")

#############
# FUNCTIONS #
#############

def append_to_log(string_to_write, path_to=DEFAULT_PATH_TO_LOG):
    """ Append a given string, with a time, to the log. """
    string_to_write = str(datetime.now())+" | "+string_to_write+"\n"
    with open(path_to, "a") as log_file:
        log_file.write(string_to_write)

def check_for_git_credentials():
    """ Check that the file holding the Git credentials exists. """
    if not os.path.exists(PATH_TO_GIT_CREDENTIALS):
        append_to_log("No Git credentials found.")
        return False
    return True

def commit_uncommitted_in_directory(name, super_path=PATH_TO_HOME,
                                    branch="master"):
    """ Commit any uncommitted material in the directory specified. """
    absolute_path = os.path.join(super_path, name)
    os.chdir(absolute_path)
    return_code = os.system("git add -A")
    if return_code != 0:
        append_to_log("Repo "+name+": Calling `git add` returns code "+
                      str(return_code)+".")
        return
    return_code = os.system("git commit -m \"HMSS auto commit.\"")
    return_code = os.system("git push origin "+branch)
    if return_code != 0:
        append_to_log("Repo "+name+": Calling `git push` returns code "+
                      str(return_code)+".")
        append_to_log("uid="+str(os.getuid()))

def commit_uncommitted_in_directories(directories_list=DIRECTORIES):
    """ As above, but for several directories. """
    if not check_for_git_credentials():
        return
    for directory in directories_list:
        commit_uncommitted_in_directory(directory)
    append_to_log("Iterated over all directories without throwing an "+
                  "exception.")

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    commit_uncommitted_in_directories()

if __name__ == "__main__":
    run()
