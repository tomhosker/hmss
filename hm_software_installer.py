"""
This code defines a class which installs the various packages and repositories
required on this computer.
"""

# Standard imports.
import os
import pathlib
import shutil
import subprocess
import urllib.parse
from dataclasses import dataclass
from typing import ClassVar

# Local imports.
from git_credentials import set_up_git_credentials, \
    DEFAULT_PATH_TO_GIT_CREDENTIALS, DEFAULT_PATH_TO_PAT, \
    DEFAULT_USERNAME as DEFAULT_GIT_USERNAME, DEFAULT_EMAIL_ADDRESS

# Local constants.
DEFAULT_OS = "ubuntu"
DEFAULT_TARGET_DIR = str(pathlib.Path.home())
DEFAULT_PATH_TO_WALLPAPER_DIR = \
    os.path.join(DEFAULT_TARGET_DIR, "hmss/wallpaper/")
DEFAULT_PYTHON_VERSION = 3

##############
# MAIN CLASS #
##############

@dataclass
class HMSoftwareInstaller:
    """ The class in question. """
    # Fields
    this_os: str = DEFAULT_OS
    target_dir: str = DEFAULT_TARGET_DIR
    thunderbird_num: int = None
    path_to_git_credentials: str = DEFAULT_PATH_TO_GIT_CREDENTIALS
    path_to_pat: str = DEFAULT_PATH_TO_PAT
    git_username: str = DEFAULT_GIT_USERNAME
    email_address: str = DEFAULT_EMAIL_ADDRESS
    path_to_wallpaper_dir: str = DEFAULT_PATH_TO_WALLPAPER_DIR
    python_version: int = DEFAULT_PYTHON_VERSION
    pip_version: int = DEFAULT_PYTHON_VERSION

    # Class attributes.
    CHROME_DEB = "google-chrome-stable_current_amd64.deb"
    CHROME_STEM = "https://dl.google.com/linux/direct/"
    EXPECTED_PATH_TO_GOOGLE_CHROME_COMMAND = "/usr/bin/google-chrome"
    GIT_URL_STEM = "https://github.com/"
    MISSING_FROM_CHROME = ("eog", "nautilus")
    OTHER_THIRD_PARTY = ("gedit-plugins", "inkscape")
    SUPPORTED_OSS = {"ubuntu", "chrome-os", "raspian", "linux-based"}
    WALLPAPER_STEM = "wallpaper_t"
    WALLPAPER_EXT = ".png"
    PIP_PACKAGES = (
        { "name": "pylint", "operator": ">=", "version": "2.12.2" },
        { "name": "pytest", "operator": None, "version": None }
    )

    def make_essentials(self):
        """ Build a tuple of essential processes to run. """
        result = (
            {
                "imperative": "Check OS",
                "gerund": "Checking OS",
                "method": self.check_os
            }, {
                "imperative": "Update and upgrade",
                "gerund": "Updating and upgrading",
                "method": update_and_upgrade
            }, {
                "imperative": "Upgrade Python",
                "gerund": "Upgrading Python",
                "method": self.upgrade_python
            }, {
                "imperative": "Set up Git",
                "gerund": "Setting up Git",
                "method": self.set_up_git
            }
        )
        return result

    def make_non_essentials(self):
        """ Build a tuple of non-essential processes to run. """
        result = (
            {
                "imperative": "Install Google Chrome",
                "gerund": "Installing Google Chrome",
                "method": self.install_google_chrome
            }, {
                "imperative": "Install HMSS",
                "gerund": "Installing HMSS",
                "method": self.install_hmss
            }, {
                "imperative": "Install Kingdom of Cyprus",
                "gerund": "Installing Kingdom of Cyprus",
                "method": self.install_kingdom_of_cyprus
            }, {
                "imperative": "Install Chancery repos",
                "gerund": "Installing Chancery repos",
                "method": self.install_chancery
            }, {
                "imperative": "Install HGMJ",
                "gerund": "Installing HGMJ",
                "method": self.install_hgmj
            }, {
                "imperative": "Install SQLite",
                "gerund": "Installing SQLite",
                "method": install_sqlite
            }, {
                "imperative": "Install other third party",
                "gerund": "Installing other third party",
                "method": self.install_other_third_party
            }
        )
        return result

    def check_os(self):
        """ Test whether the OS we're using is supported. """
        if self.this_os in self.SUPPORTED_OSS:
            return True
        return False

    def move_to_target_dir(self):
        """ Change into the directory where we want to install stuff. """
        os.chdir(self.target_dir)

    def set_up_git(self):
        """ Install Git and set up a personal access token. """
        install_result = install_via_apt("git")
        if not install_result:
            return False
        pat_result = \
            set_up_git_credentials(
                username=self.git_username,
                email_address=self.email_address,
                path_to_git_credentials=self.path_to_git_credentials,
                path_to_pat=self.path_to_pat
            )
        if not pat_result:
            return False
        return True

    def upgrade_python(self):
        """ Install PIP and other useful Python hangers-on. """
        pip_package_name = "python"+str(self.python_version)+"-pip"
        result = True
        if not install_via_apt(pip_package_name):
            result = False
        if not self.install_pip_packages():
            result = False
        return result

    def install_pip_packages(self):
        """ Install the various PIP packages specified in the class
        attribute above. """
        pip_command = "pip"+str(self.pip_version)
        result = True
        for package in self.PIP_PACKAGES:
            id_string = package["name"]
            if package["operator"] and package["version"]:
                id_string = id_string+package["operator"]+package["version"]
            command_to_run = [pip_command, "install", id_string]
            if not run_with_indulgence(command_to_run):
                result = False
        return result

    def install_google_chrome(self):
        """ Ronseal. """
        if (
            check_command_exists("google-chrome") or
            (self.this_os == "chrome-os")
        ):
            return True
        chrome_url = urllib.parse.urljoin(self.CHROME_STEM, self.CHROME_DEB)
        chrome_deb_path = "./"+self.CHROME_DEB
        download_process = subprocess.run(["wget", chrome_url])
        if download_process.returncode != 0:
            return False
        if not install_via_apt(chrome_deb_path):
            return False
        os.remove(chrome_deb_path)
        return True

    def change_wallpaper(self):
        """ Change the wallpaper on the desktop of this computer. """
        if not os.path.exists(self.path_to_wallpaper_dir):
            return False
        if self.thunderbird_num:
            wallpaper_filename = (
                self.WALLPAPER_STEM+
                str(self.thunderbird_num)+
                self.WALLPAPER_EXT
            )
        else:
            wallpaper_filename = "default.jpg"
        wallpaper_path = \
            os.path.join(self.path_to_wallpaper_dir, wallpaper_filename)
        if self.this_os == "ubuntu":
            arguments = [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                "file:///"+wallpaper_path
            ]
        elif self.this_os == "raspbian":
            arguments = ["pcmanfm", "--set-wallpaper", wallpaper_path]
        else:
            return False
        result = run_with_indulgence(arguments)
        return result

    def make_git_url(self, repo_name):
        """ Make the URL pointing to a given repo. """
        suffix = self.git_username+"/"+repo_name+".git"
        result = urllib.parse.urljoin(self.GIT_URL_STEM, suffix)
        return result

    def install_own_repo(
            self,
            repo_name,
            underpinning_packages=None,
            installation_arguments=None
        ):
        """ Install a custom repo. """
        if os.path.exists(repo_name):
            print("Looks like "+repo_name+" already exists...")
            return True
        if underpinning_packages:
            for package_name in underpinning_packages:
                if not install_via_apt(package_name):
                    return False
        arguments = ["git", "clone", self.make_git_url(repo_name)]
        if not run_with_indulgence(arguments):
            return False
        os.chdir(repo_name)
        if installation_arguments:
            if not run_with_indulgence(arguments):
                os.chdir(self.target_dir)
                return False
        os.chdir(self.target_dir)
        return True

    def install_kingdom_of_cyprus(self):
        """ Install the Kingdom of Cyprus repo. """
        result = \
            self.install_own_repo(
                "kingdom-of-cyprus",
                underpinning_packages=("nodejs", "npm")
            )
        return result

    def install_chancery(self):
        """ Install the Chancery repos. """
        if not self.install_own_repo("chancery"):
            return False
        result = \
            self.install_own_repo(
                "chancery-b",
                installation_arguments=("sh", "install_3rd_party")
            )
        return result

    def install_hmss(self):
        """ Install the HMSS repo. """
        result = self.install_own_repo("hmss")
        return result

    def install_hgmj(self):
        """ Install the HGMJ repo. """
        result = \
            self.install_own_repo(
                "hgmj",
                installation_arguments=("sh", "install_3rd_party")
            )
        return result

    def install_other_third_party(self):
        """ Install some other useful packages. """
        result = True
        for package in self.OTHER_THIRD_PARTY:
            if not install_via_apt(package):
                result = False
        if self.this_os == "chrome-os":
            for package in self.MISSING_FROM_CHROME:
                if not install_via_apt(package):
                    result = False
        return result

    def run_essentials(self):
        """ Run those processes which, if they fail, we will have to stop
        the entire program there. """
        for item in self.make_essentials():
            print(item["gerund"]+"...")
            method_to_run = item["method"]
            if not method_to_run():
                self.failure_log.append(item["imperative"])
                return False
        return True

    def run_non_essentials(self):
        """ Run the installation processes. """
        result = True
        for item in self.make_non_essentials():
            print(item["gerund"]+"...")
            method_to_run = item["method"]
            if not method_to_run():
                self.failure_log.append(item["imperative"])
                result = False
        print("Changing wallpaper...")
        if not self.change_wallpaper():
            self.failure_log.append("Change wallpaper")
            # It doesn't matter too much if this fails.
        return result

    def print_outcome(self, passed, with_flying_colours):
        """ Print a list of what failed to the screen. """
        if passed and with_flying_colours:
            print("Installation PASSED with flying colours!")
            return
        if passed:
            print("Installation PASSED but with non-essential failures.")
        else:
            print("Installation FAILED.")
        print("\nThe following items failed:\n")
        for item in self.failure_log:
            print("    * "+item)
        print(" ")

    def run(self):
        """ Run the software installer. """
        print("Running His Majesty's Software Installer...")
        get_sudo()
        self.move_to_target_dir()
        if not self.run_essentials():
            print("\nFinished.\n\n")
            self.print_outcome(False, False)
            return False
        with_flying_colours = self.run_non_essentials()
        print("\nComplete!\n")
        self.print_outcome(True, with_flying_colours)
        return True

####################
# HELPER FUNCTIONS #
####################

def get_sudo():
    """ Get superuser privileges. """
    print("I'm going to need superuser privileges for this...")
    subprocess.run(
        ["sudo", "echo", "Superuser privileges: activate!"],
        check=True
    )

def run_with_indulgence(arguments, show_output=False):
    """ Run a command, and don't panic immediately if we get a non-zero
    return code. """
    if show_output:
        print("Running subprocess.run() with arguments:")
        print(arguments)
        process = subprocess.run(arguments)
    else:
        process = subprocess.run(arguments, stdout=subprocess.DEVNULL)
    if process.returncode == 0:
        return True
    return False

def run_apt_with_argument(argument):
    """ Run APT with an argument, and tell me how it went. """
    arguments = ["sudo", "apt-get", "--yes", argument]
    result = run_with_indulgence(arguments)
    return result

def check_against_dpkg(package_name):
    """ Check whether a given package is on the books with DPKG. """
    result = run_with_indulgence(["dpkg", "--status", package_name])
    return result

def check_command_exists(command):
    """ Check whether a given command exists on this computer. """
    if shutil.which(command):
        return True
    return False

def install_via_apt(package_name, command=None):
    """ Attempt to install a package, and tell me how it went. """
    if not command:
        command = package_name
    if check_command_exists(command):
        return True
    arguments = ["sudo", "apt-get", "--yes", "install", package_name]
    result = run_with_indulgence(arguments)
    return result

def update_and_upgrade():
    """ Update and upgrade the existing software. """
    if not run_apt_with_argument("update"):
        return False
    if not run_apt_with_argument("upgrade"):
        return False
    if not install_via_apt("software-properties-common"):
        return False
    return True

def install_sqlite():
    """ Install both SQLite and a browser for it. """
    if not install_via_apt("sqlite"):
        return False
    if not install_via_apt("sqlitebrowser"):
        return False
    return True
