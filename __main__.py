"""
This code serves as the entry point to this package.
"""

# Standard imports.
import argparse

# Local imports.
from git_credentials import set_up_git_credentials
from hm_software_installer import (
    HMSoftwareInstaller,
    DEFAULT_OS,
    DEFAULT_TARGET_DIR,
    DEFAULT_PATH_TO_WALLPAPER_DIR,
    DEFAULT_PATH_TO_GIT_CREDENTIALS,
    DEFAULT_PATH_TO_PAT,
    DEFAULT_GIT_USERNAME,
    DEFAULT_EMAIL_ADDRESS,
    DEFAULT_PYTHON_VERSION
)

# Constants.
PROGRAM_DESCRIPTION = "His Majesty's Software Suite"
ARGUMENTS = [
    {
        "name": "--os",
        "default": DEFAULT_OS,
        "dest": "this_os",
        "help": "A string giving the OS in use on this system",
        "type": str
    }, {
        "name": "--email-address",
        "default": DEFAULT_EMAIL_ADDRESS,
        "dest": "email_address",
        "help": "Your email address",
        "type": str
    }, {
        "name": "--git-username",
        "default": DEFAULT_GIT_USERNAME,
        "dest": "git_username",
        "help": "Your Git username",
        "type": str
    }, {
        "name": "--path-to-git-credentials",
        "default": DEFAULT_PATH_TO_GIT_CREDENTIALS,
        "dest": "path_to_git_credentials",
        "help": "The path to the Git credentials file",
        "type": str
    }, {
        "name": "--path-to-pat",
        "default": DEFAULT_PATH_TO_PAT,
        "dest": "path_to_pat",
        "help": "The path to the Personal Access Token file",
        "type": str
    }, {
        "name": "--path-to-wallpaper-dir",
        "default": DEFAULT_PATH_TO_WALLPAPER_DIR,
        "dest": "path_to_wallpaper_dir",
        "help": (
            "The path to the directory where the wallpaper images are held"
        ),
        "type": str
    }, {
        "name": "--pip-version",
        "default": DEFAULT_PYTHON_VERSION,
        "dest": "pip_version",
        "help": (
            "The version of PIP you wish to use on this device"
        ),
        "type": int
    }, {
        "name": "--python-version",
        "default": DEFAULT_PYTHON_VERSION,
        "dest": "python_version",
        "help": (
            "The (integer) version of Python you wish to use on this device"
        ),
        "type": int
    }, {
        "name": "--target-dir",
        "default": DEFAULT_TARGET_DIR,
        "dest": "target_dir",
        "help": (
            "The path to the directory into which we're going to install stuff"
        ),
        "type": str
    }, {
        "name": "--thunderbird-num",
        "default": None,
        "dest": "thunderbird_num",
        "help": "The Thunderbird number for this device",
        "type": int
    }, {
        "name": "--reset-git-credentials-only",
        "action": "store_true",
        "default": False,
        "dest": "reset_git_credentials_only",
        "help": "Reset the Git credentials, but perform no installations"
    }, {
        "name": "--show-output",
        "action": "store_true",
        "default": False,
        "dest": "show_output",
        "help": "Show the output from the various commands called"
    }
]

####################
# HELPER FUNCTIONS #
####################

def get_attribute_names():
    """ Get the names of the attributes of the HMSoftwareInstaller that we're
    going to modify via the command line. """
    result = []
    for argument in ARGUMENTS:
        result.append(argument["dest"])
    return result

def make_installer_obj(arguments):
    """ Ronseal. """
    result = HMSoftwareInstaller()
    attribute_names = get_attribute_names()
    for attribute_name in attribute_names:
        attribute_value = getattr(arguments, attribute_name)
        setattr(result, attribute_name, attribute_value)
    return result

def make_parser():
    """ Ronseal. """
    result = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    for argument in ARGUMENTS:
        result.add_argument(argument.pop("name"), **argument)
    return result

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    parser = make_parser()
    arguments = parser.parse_args()
    if arguments.reset_git_credentials_only:
        run_git_credentials_function(arguments)
    else:
        installer = make_installer_obj(arguments)
        installer.run()

if __name__ == "__main__":
    run()
