import os
import shutil
from tempfile import mkstemp
import configparser
from .mod_req import setup_requirements


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
