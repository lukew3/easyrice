import os
import shutil
from tempfile import mkstemp
import configparser
from .mod_req import setup_requirements

def remove_setup(setup_name, warning_off):
    # Could print a list of setups numbered and then ask for a number or numbers to delete
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup_name
    # Warns if setup is current setup
    if (get_current_setup() == setup_name) and warning_off == False:
        choice = input("This is your active setup, are you sure you want to remove it? (y/n)")
        if choice == 'n' or choice == 'N':
            return 0
    # Check that setup existss
    if os.path.exists(setup_dir):
        os.system('rm -rf ' + setup_dir)
    else:
        print("Setup \"" + setup_name + "\" doesn't exist")

def copy_setup(old_name, new_name):
    current_folder = os.path.expanduser("~") + "/.config/easyrice/setups/" + old_name
    current_placeholder = current_folder + "(1)"
    new_folder = os.path.expanduser("~") + "/.config/easyrice/setups/" + new_name

    # Add (1) to the end of current_folder to differentiate
    os.rename(current_folder, current_placeholder)

    shutil.copytree(current_placeholder, current_folder)

    rename_setup(old_name, new_name)
    os.rename(current_placeholder, current_folder)

def rename_setup(old_name, new_name):
    if old_name == None:
        old_name = input("Enter the setup you want to rename: ")
    if new_name == None:
        new_name = input("Enter the new name for the setup: ")
    current_folder = os.path.expanduser("~") + "/.config/easyrice/setups/" + old_name
    new_folder = os.path.expanduser("~") + "/.config/easyrice/setups/" + new_name
    os.rename(current_folder, new_folder)

    # Replace name of setup in config run_wm_command
    # This is incomplete because name needs to be changed in each config file as well
    # probably could do some recursive search through files for \setups\<old_name>\
    setup_config = new_folder + "/config"
    pattern = '/easyrice/setups/' + old_name
    subst = 'easyrice/setups/' + new_name
    replace(setup_config, pattern, subst)
    readme_location = os.path.expanduser("~") + "/.config/easyrice/setups/" + new_name + "/README.md"
    replace(readme_location, old_name, new_name)
    print("Setup \'" + old_name + "\' renamed to \'" + new_name + "\'")
    if old_name == get_current_setup():
        set_current_setup(new_name)


def set_current_setup(setup_name):
    easyrice_path = os.path.expanduser("~") + "/.config/easyrice"
    config = configparser.ConfigParser()
    config.read(easyrice_path + "/config")
    config['main']['current_setup'] = setup_name
    with open(easyrice_path + '/config', 'w') as configfile:
        config.write(configfile)
    # Install requirements
    setup_requirements()
    # Write config files to user .config
    localize_dotfiles(setup_name)


def localize_dotfiles(setup_name):
    setup_dotfiles = os.path.expanduser(
        "~") + "/.config/easyrice/setups/" + setup_name + "/dotfiles"
    local_dotfiles = os.path.expanduser("~") + "/.config"
    # local_backup = easyrice_path + "/setups/" + ".backup" + "/dotfiles"
    shutil.copytree(setup_dotfiles, local_dotfiles, dirs_exist_ok=True)

    # Creates a backup of .config files before they were changed
    # Only stores files from the last change, better for storage but could be bad if user tries out multiple setups and realizes they liked their first one the best
    # It might be possible to use git to save different versions while keeping storage in mind, leaning towards not though
    revert_path = os.path.expanduser("~") + "/.config/easyrice/revert"
    if not os.path.isdir(revert_path):
        os.makedirs(revert_path)
    folders = os.listdir(setup_dotfiles)
    for folder in folders:
        shutil.copytree(local_dotfiles + '/' + folder, revert_path +
                        '/' + folder, dirs_exist_ok=True)


def revert():
    revert_path = os.path.expanduser("~") + "/.config/easyrice/revert"
    local_dotfiles = os.path.expanduser("~") + "/.config"
    shutil.copytree(revert_path, local_dotfiles, dirs_exist_ok=True)


def get_current_setup():
    easyrice_path = os.path.expanduser("~") + "/.config/easyrice"
    config = configparser.ConfigParser()
    config.read(easyrice_path + "/config")
    return config['main']['current_setup']


def replace(file_path, pattern, subst):
    """ Replaces the given pattern with subst in the file at file_path"""
    # Create temp file
    fh, abs_path = mkstemp()
    with os.fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    # Copy the file permissions from the old file to the new file
    shutil.copymode(file_path, abs_path)
    # Remove original file
    os.remove(file_path)
    # Move new file
    shutil.move(abs_path, file_path)


def expand_dir(og_dir):
    if og_dir[0] == "/":
        return og_dir
    elif og_dir[0] == "~":
        full_dir = os.path.expanduser("~") + og_dir[1:]
        return full_dir
    else:
        full_dir = os.getcwd() + '/' + og_dir
        return full_dir
