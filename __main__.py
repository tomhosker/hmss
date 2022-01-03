"""
This code serves as the entry point to this package.
"""

# Standard imports.
import argparse

# Local imports.
from git_credentials import set_up_git_credentials
from hm_software_installer import HMSoftwareInstaller, \
                                  DEFAULT_OS, \
                                  DEFAULT_TARGET_DIR, \
                                  DEFAULT_PATH_TO_WALLPAPER_DIR, \
                                  DEFAULT_PATH_TO_GIT_CREDENTIALS, \
                                  DEFAULT_PATH_TO_PAT, \
                                  DEFAULT_GIT_USERNAME, \
                                  DEFAULT_EMAIL_ADDRESS

# Constants.
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
    }
]
BOOLEAN_ARGUMENTS = [
    {
        "name": "--reset-git-credentials-only",
        "action": "store_true",
        "default": False,
        "dest": "reset_git_credentials_only",
        "help": "Reset the Git credentials, but perform no installations"
    }
]

####################
# HELPER FUNCTIONS #
####################

def add_boolean_arguments(parser):
    """ Add the Boolean flags to the parser object. """
    for argument in BOOLEAN_ARGUMENTS:
        parser.add_argument(
            argument["name"],
            action=argument["action"],
            default=argument["default"],
            dest=argument["dest"],
            help=argument["help"]
        )

def make_parser():
    """ Ronseal. """
    result = argparse.ArgumentParser(description="Parser for HMSS")
    for argument in ARGUMENTS:
        result.add_argument(
            argument["name"],
            default=argument["default"],
            dest=argument["dest"],
            help=argument["help"],
            type=argument["type"]
        )
    add_boolean_arguments(result)
    return result

def make_installer_obj(arguments):
    """ Ronseal. """
    result = \
        HMSoftwareInstaller(
            this_os=arguments.this_os,
            target_dir=arguments.target_dir,
            thunderbird_num=arguments.thunderbird_num,
            path_to_git_credentials=arguments.path_to_git_credentials,
            path_to_pat=arguments.path_to_pat,
            git_username=arguments.git_username,
            email_address=arguments.email_address,
            path_to_wallpaper_dir=arguments.path_to_wallpaper_dir
        )
    return result

def run_git_credentials_function(arguments):
    set_up_git_credentials(
        username=arguments.git_username,
        email_address=arguments.email_address,
        path_to_git_credentials=arguments.path_to_git_credentials,
        path_to_pat=arguments.path_to_pat
    )

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
