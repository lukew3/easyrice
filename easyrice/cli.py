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
@click.option('--name', '-n', required=False)
def new(requirements, name):
    """ Creates a new setup directory. Empty unless passed -c, which copies local setup """
    config_dir = os.path.expanduser("~") + "/.config"
    # TODO: create a generated name with the lorem package if the user doesn't want to include a name https://pypi.org/project/lorem/
    if name == None:
        setupName = input("Give your setup a name: ")
    else:
        setupName = name
    while os.path.exists(config_dir + "/easyrice/setups/" + setupName):
        print("A setup with that name already exists")
        setupName = input("Give your setup a different name: ")
    if requirements != None:
        requirements_file = os.getcwd() + "/" + requirements
    else:
        requirements_file = ''
    mod_new.make_setup(setupName, requirements_file)


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
    mod_utils.rename_setup(old_name, new_name)


@cli.command()
@click.argument('setup')
def remove(setup):
    """ Delete an existing setup """
    # Could print a list of setups numbered and then ask for a number or numbers to delete
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    # Warns if setup is current setup
    if get_current_setup() == setup:
        choice = input("This is your active setup, are you sure you want to remove it? (y/n)")
        if choice == 'n' or choice == 'N':
            return 0
    # Check that setup existss
    if os.path.exists(setup_dir):
        os.system('rm -rf ' + setup_dir)
    else:
        print("Setup \"" + setup + "\" doesn't exist")


@cli.command()
@click.argument('setup')
def upload(setup):
    """ Uploads passed setup to easyrice-setups github """
    mod_transfer.upload(setup)


@cli.command()
def list():
    """ Lists all setups in easyrice config """
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
@click.option('-t', '--to-dir', required=False)
def export(setup, to_dir):
    """ Export given setup to home directory """
    # Could add option to change output location
    mod_transfer.local_export(setup, to_dir)


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
        os.makedirs(user_setups_dir, exist_ok=True)
        shutil.copyfile("easyrice/config", user_config)
