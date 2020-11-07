import os
import shutil
import configparser
import subprocess
import click
import sys
from tempfile import mkstemp

from .commands import mod_new, mod_run, mod_upload, mod_utils
from .commands.mod_utils import set_current_setup, get_current_setup, replace

@click.group()
def cli():
    install_config()

@cli.command()
@click.option('--setup', '-s')
def run(setup):
    """ Runs either the setup designated in the main config or -s """
    if setup == None:
        setup = mod_utils.get_current_setup()
    mod_run.main(setup)

@cli.command()
@click.option('--copy', '-c', is_flag=True)
def new(copy):
    """ Creates a new setup directory. Empty unless passed -c, which copies local setup """
    config_dir = os.path.expanduser("~") + "/.config"
    setupName = input("Give your setup a name: ")
    while os.path.exists(config_dir + "/easyrice/setups/" + setupName):
        print("A setup with that name already exists")
        setupName = input("Give your setup a different name: ")
    wm = input("Window manager: ")

    if copy:
        mod_new.copy(wm, setupName)
    else:
        mod_new.make_base(wm, setupName)

@cli.command()
@click.argument('repo')
def clone(repo):
    """ Clones a setup from a passed git remote repository """
    setups_dir = os.path.expanduser("~") + '/.config/easyrice/setups'
    clone_script = 'cd ' + setups_dir + '\ngit clone ' + repo
    os.system(clone_script)
    setup_name = repo.split('/')[-1].split('.')[0]
    set_current_setup(setup_name)
    # Might want to add a way to check if the git repo has an extra folder in it.
    # If the user uploaded the whole folder instead of the insides of the folder, this script wont work
    # Or you could make a way to automatically upload a setup to github

@cli.command()
@click.option('--from', '-f', 'from_', required=False)
@click.option('--to', '-t', required=False)
def rename(from_, to):
    """ Rename an existing setup"""
    current_name = from_
    new_name = to
    if current_name == None:
        current_name = input("Enter the setup you want to rename: ")
    if new_name == None:
        new_name = input("Enter the new name for the setup: ")
    current_folder = os.path.expanduser("~") + "/.config/easyrice/setups/" + current_name
    new_folder = os.path.expanduser("~") + "/.config/easyrice/setups/" + new_name
    os.rename(current_folder, new_folder)

    # Replace name of setup in config run_wm_command
    # This is incomplete because name needs to be changed in each config file as well
    # probably could do some recursive search through files for \setups\<current_name>\
    setup_config = new_folder + "/config"
    pattern = '/setups/' + current_name + '/app_configs'
    subst = '/setups/' + new_name + '/app_configs'
    replace(setup_config, pattern, subst)
    print("Setup \'" + current_name + "\' renamed to \'" + new_name + "\'")


@cli.command()
@click.argument('setup')
def remove(setup):
    """ Delete an existing setup """
    # Could print a list of setups numbered and then ask for a number or numbers to delete
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    os.system('rm -rf ' + setup_dir)
    # Could add a message that tells if the setup doesn't exist and can't be removed

@cli.command()
@click.argument('setup')
def upload(setup):
    """ Uploads passed setup to your github """
    username = input("Github username: ")
    mod_upload.main(username, setup)

"""
@cli.command()
def list():
    """ Lists all setups in easyrice config """
    pass
"""

def install_config():
    """ Make base directory and configs for install """
    user_config_dir = os.path.expanduser("~") + "/.config/easyrice"
    user_config = user_config_dir + "/config"
    user_setups_dir = user_config_dir + "/setups"

    if not os.path.isfile(user_config):
        # The make config dir is unecessary but I'm not sure if it's best practice to keep it or not
        os.makedirs(user_config_dir, exist_ok=True)
        os.makedirs(user_setups_dir, exist_ok=True)
        shutil.copyfile("easyrice/config", user_config)

if __name__ == "__main__":
    main()
