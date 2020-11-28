import shutil
import os
import platform
import distro
from .mod_utils import replace, get_current_setup

def check_requirements():
    setup = get_current_setup()
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    requirements_file = setup_dir + "/requirements.txt"
    f = open(requirements_file, 'r')
    requirements = f.readlines()
    for i in range(0, len(requirements)-1):
        requirements[i] = requirements[i].strip()

    print(requirements)
    #Check that the packages are valid and install
    install_requirements(requirements)
    #Copy .config files
    copy_configs(requirements, setup_dir)


def install_requirements(requirements):
    distro_name = distro.linux_distribution(full_distribution_name=False)[0]
    for req in requirements:
        print("Installing " + req + "...")
        os.system(get_install_command(req, distro_name))
    print(distro_name)


def copy_configs(requirements, setup_dir):
    for req in requirements:
        old_dir = os.path.expanduser("~") + ".config/" + req
        # If a config file exists, copy it to the setup's app_configs folder
        if os.path.isdir(old_dir):
            new_dir = setup_dir + "/app_configs/" + req
            shutil.copyfile(old_dir, new_dir)

def get_install_command(req, distro_name):
    # Support is needed for requirements that must be installed from source
    if distro_name == 'ubuntu':
        script = 'sudo apt-get install ' + req
    elif distro_name == 'fedora':
        script = 'sudo dnf install ' + req
    elif distro_name == 'debian':
        script = 'sudo apt install ' + req
    else:
        # There needs to be some way to tell the system how to retrieve the package.
        # Unfortunately, there isn't one universal way to install
        # The variables in here aren't valid yet, they are just pseudocode
        script_list = [
        'git clone ' + git_url,
        'cd ' + package,
        'sudo make install'
        ]
        script = '\n'.join(script)
    return script
