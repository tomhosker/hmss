"""
This file lists some configurations for the project as a whole.
"""

# Standard imports.
import os
import pathlib

##################
# CONFIGURATIONS #
##################

# Headliners.
PROGRAM_DESCRIPTION = "His Majesty's Software Suite"

# Components.
PATH_TO_HOME = str(pathlib.Path.home())

# Defaults.
DEFAULT_EMAIL_ADDRESS = "tomdothosker@gmail.com"
DEFAULT_ENCODING = "utf-8"
DEFAULT_GIT_USERNAME = "tomhosker"
DEFAULT_OS = "ubuntu"
DEFAULT_PATH_TO_GIT_CREDENTIALS = \
    os.path.join(PATH_TO_HOME, ".git-credentials")
DEFAULT_PATH_TO_PAT = \
    os.path.join(PATH_TO_HOME, "personal_access_token.txt")
DEFAULT_PATH_TO_WALLPAPER_DIR = \
    os.path.join(PATH_TO_HOME, "hmss/wallpaper/")
DEFAULT_PYTHON_VERSION = 3
DEFAULT_TARGET_DIR = PATH_TO_HOME
