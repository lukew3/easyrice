import shutil
import os
import platform
import distro
import configparser
from .mod_pkg_install import get_install_script

def get_current_setup():
    easyrice_path = os.path.expanduser("~") + "/.config/easyrice"
    config = configparser.ConfigParser()
    config.read(easyrice_path + "/config")
    return config['main']['current_setup']


def setup_requirements():
    setup = get_current_setup()
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    requirements_file = setup_dir + "/requirements.txt"
    f = open(requirements_file, 'r')
    requirements = f.readlines()
    for i in range(0, len(requirements) - 1):
        requirements[i] = requirements[i].strip()
    # Removes extra newline character in last line of requirements
    if requirements[-1][-1:] == "\n":
        requirements[-1] = requirements[-1][:-1]
    # Check that the packages are valid and install
    install_requirements(requirements)
    # Copy .config files
    copy_configs(requirements, setup_dir)


def install_requirements(requirements):
    distro_name = distro.linux_distribution(full_distribution_name=False)[0]
    for req in requirements:
        print("-------------------------")
        print("Installing " + req + "...")
        os.system(get_install_script(req, distro_name))


def copy_configs(requirements, setup_dir):
    for req in requirements:
        old_dir = os.path.expanduser("~") + ".config/" + req
        # If a config file exists, copy it to the setup's dotfiles folder
        if os.path.isdir(old_dir):
            new_dir = setup_dir + "/dotfiles/" + req
            shutil.copyfile(old_dir, new_dir)
