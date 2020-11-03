import os
import shutil
import configparser
import subprocess
import click
import sys


@click.group(invoke_without_command=True)
@click.option('-s', '--setup-name', help='Include the name of the setup you want to use')
def cli(setup_name):
    """ Runs the setup selected in config or the command passed """
    print(setup_name)
    install_config()
    os.system(run_wm_custom_config(setup_name))


def run_wm_custom_config(setup_name):
    """ Gets the path of the window manager config """
    riceman_path = os.path.expanduser("~") + "/.config/riceman"
    config = configparser.ConfigParser()
    config.read(riceman_path + "/config")

    if setup_name == None:
        setup = config['main']['current_setup']
    else:
        setup = setup_name

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
    """ Make base directory and configs for install """
    user_config_dir = os.path.expanduser("~") + "/.config/riceman"
    user_config = user_config_dir + "/config"
    user_setups_dir = user_config_dir + "/setups"
    user_launch_sh = user_config_dir + "/launch.sh"

    if not os.path.isfile(user_config):
        # The make config dir is unecessary but I'm not sure if it's best practice to keep it or not
        os.makedirs(user_config_dir, exist_ok=True)
        os.makedirs(user_setups_dir, exist_ok=True)
        shutil.copyfile("riceman/config", user_config)


@cli.command()
def copy_current():
    """ Copies your current setup made outside of riceman """
    setupName = input("Give your setup a name: ")
    wm = input("Window manager: ")
    setup_base(wm, setupName)
    print("Base directory created")

    config_dir = os.path.expanduser("~") + "/.config"
    this_setup_dir = config_dir + "/riceman/setups/" + setupName
    head = config_dir + "/" + wm + "/config"
    base = config_dir + "/riceman/setups/" + setupName + "/app_configs/" + wm + "/config"
    shutil.copyfile(head, base)
    print("Window manager config created")

    # print("What requirements are necessary? Seperate names of packages with a space. ")
    # arguments = input("Requirements: ")

    # Detect and move wallpapers
    f = open(base, "r")
    wallpaper_head = ''
    wallpaper_name = ''
    for line in f:
        if 'feh' in line:
            wallpaper_head = line.rsplit(None, 1)[-1]
            wallpaper_name = wallpaper_head.rsplit('/', 1)[1]
    wallpaper_base = config_dir + "/riceman/setups/" + setupName + "/assets/" + wallpaper_name
    if wallpaper_head[0] == '~':
        wallpaper_head = os.path.expanduser("~") + wallpaper_head[1:]
    shutil.copyfile(wallpaper_head, wallpaper_base)
    print("Wallpaper copied")
    # Fix reference to wallpaper in window manager

    # it's not a good idea to search for each package individually but polybar
    # is so common that it works for now.
    # check for polybar
    polybar_config_head = config_dir + "/polybar"
    if os.path.exists(polybar_config_head):
        polybar_config_base = this_setup_dir + "/app_configs/polybar"
        shutil.copytree(polybar_config_head, polybar_config_base)
        print("Polybar config copied")
    # fix polybar references in window manager config

    # Set riceman to run this setup on startup
    riceman_path = os.path.expanduser("~") + "/.config/riceman"
    config = configparser.ConfigParser()
    config.read(riceman_path + "/config")
    config['main']['current_setup'] = setupName
    with open(riceman_path + '/config', 'w') as configfile:
        config.write(configfile)

    # It would help if you could run your wm like you usually would and riceman
    # would detect which apps started up before you started using the environment
    # Then those apps would be added to requirements.txt and their configs added to app_config folder


@cli.command()
def new_setup():
    """ Creates a new setup with empty directories """
    setupName = input("Give your setup a name: ")
    wm = input("Window manager: ")
    setup_base(wm, setupName)


def setup_base(wm, setupName):
    parent_dir = os.path.expanduser("~") + "/.config/riceman/setups"
    setup_dir = parent_dir + "/" + setupName
    os.makedirs(setup_dir + "/assets")
    os.makedirs(setup_dir + "/app_configs")
    wm_dir = setup_dir + "/app_configs/" + wm
    os.makedirs(wm_dir)
    f = open(setup_dir + "/config", "w+")
    f.writelines(['[main]\n', 'window_manager = ' + wm + "\n"])
    f.close()
    f = open(setup_dir + "/requirements.txt", "w+")
    f.close()


@ cli.command()
# could pass two arguments to change name1 to name2
def rename_setup():
    """ Rename an existing setup """
    # Rename a setup
    # This will search through the configs and replace the /<setupname>/ part of the location string of each mentionof the
    # <setupname> folder
    currentName = input("Current name: ")
    newName = input("New name: ")


@cli.command()
def delete_setup():
    """ Delete an existing setup """
    # Could print a list of setups numbered and then ask for a number or numbers to delete
    name = input("Which setup do you want to delete: ")
    setup_dir = os.path.expanduser("~") + "/.config/riceman/setups/" + name
    os.system('rm -r ' + setup_dir)


if __name__ == "__main__":
    main()
