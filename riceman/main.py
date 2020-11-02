import os
import shutil
import configparser
import subprocess
import click
import sys


@click.group(invoke_without_command=True)
# @click.option('--s') # select the setup that you want to run without changing the config
def cli():
    """ Runs the setup selected in config or the command passed """

    install_config()

    os.system(get_wm_config_path())
    # install_config()


def get_wm_config_path():
    """ Gets the path of the window manager config """
    riceman_path = os.path.expanduser("~") + "/.config/riceman"
    config = configparser.ConfigParser()

    config.read(riceman_path + "/config")
    setup = config['main']['current_setup']
    if os.path.isfile(riceman_path + "/setups/" + setup + "/config"):
        config.read(riceman_path + "/setups/" + setup + "/config")
        wm = config['main']['window_manager']
        run_command = wm + " -c " + \
            os.path.expanduser("~") + "/.config/riceman/setups/" + \
            setup + "/app_configs/" + wm + "/config"
    else:
        run_command = ''
    return run_command


def install_config():
    # Make base directory and configs for install
    user_config_dir = os.path.expanduser("~") + "/.config/riceman"
    user_config = user_config_dir + "/config"
    user_setups_dir = user_config_dir + "/setups"
    user_launch_sh = user_config_dir + "/launch.sh"

    if not os.path.isfile(user_config):
        # The make config dir is unecessary but I'm not sure if it's best practice to keep it or not
        os.makedirs(user_config_dir, exist_ok=True)
        os.makedirs(user_setups_dir, exist_ok=True)
        shutil.copyfile("riceman/config", user_config)

    # Write xsessions desktop file
    environment_file = "/usr/share/xsessions/riceman.desktop"
# shutil.copyfile("ricemandesktop", environment_file)


@cli.command()
# @click.option('--name', required=False, help='Include the name of your setup')
def copy_current():
    """ Copies your current setup made outside of riceman and adds it to setups """
    # This could be used to copy the users current setup
    # Maybe grab the config in i3 or whatever is specified and then
    # grab dependencies from that
    # Could be called by riceman newsetup
    # Could also pass setupname through this as 'riceman newsetup custom'
    setupName = input("Give your setup a name: ")
    wm = input("Window manager: ")
    setup_base(wm, setupName)
    print("Base directory created")

    config_dir = os.path.expanduser("~") + "/.config"
    # The next line is really messy, maybe I could make it neater by assigning strings
    # to variables and then calling them in shutil copyfile
    head = config_dir + "/" + wm + "/config"
    base = config_dir + "/riceman/setups/" + setupName + "/app_configs/" + wm + "/config"
    shutil.copyfile(head, base)
    print("Window manger config created")

    # Detect apps like polybar and others

    # Detect and move wallpapers


def setup_base(wm, setupName):
    parent_dir = os.path.expanduser("~") + "/.config/riceman/setups"
    setup_dir = parent_dir + "/" + setupName
    os.makedirs(setup_dir)
    os.makedirs(setup_dir + "/assets")
    os.makedirs(setup_dir + "/app_configs")
    wm_dir = setup_dir + "/app_configs/" + wm
    os.makedirs(wm_dir)
    f = open(setup_dir + "/config", "w+")
    f.writelines(['[main]\n', 'window_manager = ' + wm + "\n"])
    f.close()
    f = open(setup_dir + "/requirements.txt", "w+")
    f.close()


@ cli.command('rename_setup', short_help='rename a setup')
# could pass two arguments to change name1 to name2
def renameSetup():
    # Rename a setup
    # This will search through the configs and replace the /<setupname>/ part of the location string of each mentionof the
    # <setupname> folder
    currentName = input("Current name: ")
    newName = input("New name: ")


if __name__ == "__main__":
    main()
