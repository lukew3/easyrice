import os
import shutil
import configparser
import subprocess
import click
import sys
from tempfile import mkstemp

from .commands import mod_new, mod_run, mod_transfer, mod_utils, mod_req
from .commands.mod_utils import set_current_setup, get_current_setup, replace


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    install_config()
    setup_name = mod_utils.get_current_setup()
    if ctx.invoked_subcommand is None:
        mod_run.main(setup_name)


@cli.command()
@click.option('--requirements', '-r', required=False)
def new(requirements):
    """ Creates a new setup directory. Empty unless passed -c, which copies local setup """
    config_dir = os.path.expanduser("~") + "/.config"
    # TODO: create a generated name with the lorem package if the user doesn't want to include a name https://pypi.org/project/lorem/
    setupName = input("Give your setup a name: ")
    while os.path.exists(config_dir + "/easyrice/setups/" + setupName):
        print("A setup with that name already exists")
        setupName = input("Give your setup a different name: ")
    if requirements != None:
        requirements_file = os.getcwd() + "/" + requirements
    else:
        requirements_file = ''
    mod_new.make_base(setupName, requirements_file)


@cli.command()
@click.argument('repo')
def clone(repo):
    """ Clones a setup from a passed git remote repository """
    mod_transfer.git_clone(repo)


@cli.command()
@click.argument('old_name')
@click.argument('new_name')
def rename(old_name, new_name):
    """ Rename an existing setup"""
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
    pattern = '/setups/' + old_name + '/dotfiles'
    subst = '/setups/' + new_name + '/dotfiles'
    replace(setup_config, pattern, subst)
    print("Setup \'" + old_name + "\' renamed to \'" + new_name + "\'")
    if old_name == get_current_setup():
        set_current_setup(new_name)


@cli.command()
@click.argument('setup')
def remove(setup):
    """ Delete an existing setup """
    # Could print a list of setups numbered and then ask for a number or numbers to delete
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    os.system('rm -rf ' + setup_dir)
    # Could add a message that tells if the setup doesn't exist and can't be removed


# This method of upload was deprecated by github.
# This can still work if you add tokens
@cli.command()
@click.argument('setup')
def upload(setup):
    """ Uploads passed setup to your github """
    username = input("Github username: ")
    mod_transfer.upload(username, setup)


@cli.command()
def list():
    """ Lists all setups in easyrice config """
    # Maybe you could include the window manager used in each setup
    # Even better you could add an option that allows the user to see all installed packages or config folder names
    setups_dir = os.path.expanduser("~") + "/.config/easyrice/setups/"
    setups_list = os.listdir(setups_dir)
    active = get_current_setup()
    for setup in setups_list:
        if setup == active:
            print(setup + " (active)")
        else:
            print(setup)


@cli.command()
@click.argument('setup')
def set_active(setup):
    """ Sets the passed setup as active setup """
    set_current_setup(setup)


@cli.command()
def revert():
    """ Reverts configs to what they were before the current setup """
    mod_utils.revert()


@cli.command()
@click.argument('setup')
def export(setup):
    """ Export given setup to home directory """
    # Could add option to change output location
    mod_transfer.local_export(setup)


@cli.command()
@click.argument('setup_dir')
def add(setup_dir):
    """ Imports a setup folder into easyrice """
    mod_transfer.local_import(setup_dir)


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
