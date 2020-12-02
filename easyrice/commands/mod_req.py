import shutil
import os
import platform
import distro
import configparser


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
        os.system(get_install_command(req, distro_name))


def copy_configs(requirements, setup_dir):
    for req in requirements:
        old_dir = os.path.expanduser("~") + ".config/" + req
        # If a config file exists, copy it to the setup's dotfiles folder
        if os.path.isdir(old_dir):
            new_dir = setup_dir + "/dotfiles/" + req
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
        script = get_install_from_source_script(req, distro_name)
    return script


def get_install_from_source_script(req, distro_name):
    # There needs to be some way to tell the system how to retrieve the package.
    # Unfortunately, there isn't one universal way to install
    # The variables in here aren't valid yet, they are just pseudocode
    git_url = "github.com/" + req + "/" + req
    script_list = [
        'git clone ' + git_url,
        'cd ' + req, 'sudo make install',
        'cd ..',
        'rm -rf ' + req
    ]
    script = '\n'.join(script_list)
    return script
