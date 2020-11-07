import os
import shutil
import configparser
import subprocess
import click
import sys
from tempfile import mkstemp

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

@click.group()
def cli():
    install_config()

@cli.command()
@click.option('--setup', '-s')
def run(setup):
    """ Runs either the setup designated in the main config or -s """
    if setup == None:
        setup = get_current_setup()
    os.system(run_wm_custom_config(setup))

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
        copy_current(wm, setupName)
    else:
        setup_base(wm, setupName)

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
    username = 'lukew3'
    repository = setup
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    script = get_upload_script(setup_dir, username, repository)
    os.system(script)

@cli.command()
def list():
    """ Lists all setups in easyrice config """
    pass

def copy_current(wm, setupName):
    """ Copies your current setup into easyrice """
    config_dir = os.path.expanduser("~") + "/.config"

    setup_base(wm, setupName)

    this_setup_dir = config_dir + "/easyrice/setups/" + setupName
    base = ''
    if wm == 'bspwm':
        # add sxhkd dependency
        sxhkdrc_head = config_dir + "/sxhkd/sxhkdrc"
        sxhkdrc_base = this_setup_dir + "/app_configs/sxhkd/sxhkdrc"
        shutil.copyfile(sxhkdrc_head, sxhkdrc_base)
        # add bspwm config titled bspwmrc
        bspwmrc_head = config_dir + "/bspwm/bspwmrc"
        bspwmrc_base = this_setup_dir + "/app_configs/bspwm/bspwmrc"
        shutil.copyfile(bspwmrc_head, bspwmrc_base)
        # add sxhkd command to bspwmrc
        sxhkd_command = 'sxhkd -c ' + sxhkdrc_base + " &"
        replace(bspwmrc_base, 'sxhkd &', sxhkd_command)
        base = bspwmrc_base
    else:
        head = config_dir + "/" + wm + "/config"
        base = this_setup_dir + "/app_configs/" + wm + "/config"
        shutil.copyfile(head, base)

    print("Window manager config created")

    # print("What requirements are necessary? Seperate names of packages with a space. ")
    # arguments = input("Requirements: ")

    # Detect and move wallpapers
    wallpaper_head = ''
    wallpaper_base = ''
    f = open(base, "r")
    for line in f:
        if 'feh' in line:
            wallpaper_head = line.rsplit(None, 1)[-1]
            wallpaper_name = wallpaper_head.rsplit('/', 1)[1]
            wallpaper_base = config_dir + "/easyrice/setups/" + setupName + "/assets/" + wallpaper_name
            # Changes reference in wm config to new wallpaper location in assets folder
            replace(base, wallpaper_head, wallpaper_base)
            break
    f.close()
    if wallpaper_head != '':
        if wallpaper_head[0] == '~':
            wallpaper_head = os.path.expanduser("~") + wallpaper_head[1:]
        shutil.copyfile(wallpaper_head, wallpaper_base)
        print("Wallpaper copied")

    # it's not a good idea to search for each package individually but polybar
    # is so common that it works for now.
    # check for polybar
    polybar_config_head = config_dir + "/polybar"
    if os.path.exists(polybar_config_head):
        polybar_config_base = this_setup_dir + "/app_configs/polybar"
        shutil.copytree(polybar_config_head, polybar_config_base)
        print("Polybar config copied")
    # fix polybar references in window manager config
    original_polybar_call = ".config/polybar/launch.sh"
    new_polybar_call = ".config/easyrice/setups/" + setupName + "/app_configs/polybar/launch.sh"
    replace(base, original_polybar_call, new_polybar_call)

    # Set easyrice to run this setup on startup
    set_current_setup(setupName)
    # It would help if you could run your wm like you usually would and easyrice
    # would detect which apps started up before you started using the environment
    # Then those apps would be added to requirements.txt and their configs added to app_config folder

def set_current_setup(setupName):
    easyrice_path = os.path.expanduser("~") + "/.config/easyrice"
    config = configparser.ConfigParser()
    config.read(easyrice_path + "/config")
    config['main']['current_setup'] = setupName
    with open(easyrice_path + '/config', 'w') as configfile:
        config.write(configfile)

def get_current_setup():
    easyrice_path = os.path.expanduser("~") + "/.config/easyrice"
    config = configparser.ConfigParser()
    config.read(easyrice_path + "/config")
    return config['main']['current_setup']

def setup_base(wm, setupName):
    parent_dir = os.path.expanduser("~") + "/.config/easyrice/setups"
    setup_dir = parent_dir + "/" + setupName
    os.makedirs(setup_dir + "/assets")
    os.makedirs(setup_dir + "/app_configs")
    wm_dir = setup_dir + "/app_configs/" + wm
    if wm == 'bspwm':
        os.makedirs(setup_dir + "/app_configs/sxhkd")
    os.makedirs(wm_dir)

    # Write setup config file including wm name and runwm command
    wm_config_filename = ''
    if wm == 'bspwm':
        wm_config_filename = 'bspwmrc'
    else:
        wm_config_filename = 'config'
    run_wm_command = wm + " -c " + \
        os.path.expanduser("~") + "/.config/easyrice/setups/" + \
        setupName + "/app_configs/" + wm + "/" + wm_config_filename
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'window_manager': wm,
                         'run_wm_command': run_wm_command}
    with open(setup_dir + "/config", 'w') as configfile:
        config.write(configfile)
    print("Base directory created")


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


def run_wm_custom_config(setup_name):
    """ Gets the path of the window manager config """
    easyrice_path = os.path.expanduser("~") + "/.config/easyrice"
    config = configparser.ConfigParser()
    config.read(easyrice_path + "/config")

    if setup_name == None:
        setup = config['main']['current_setup']
    else:
        setup = setup_name

    if os.path.isfile(easyrice_path + "/setups/" + setup + "/config"):
        config.read(easyrice_path + "/setups/" + setup + "/config")
        # start_wm command should be added to config file so that the calculations below don't have to be run at every startup
        wm = config['DEFAULT']['window_manager']
        run_command = config['DEFAULT']['run_wm_command']
    else:
        run_command = ''
    return run_command

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

def get_upload_script(path, user, repo):
    script = []
    script.append(f'cd {path}')
    script.append('git init')
    script.append('git add .')
    script.append('git commit -m "Easyrice upload"')
    # It would be preferable if I could use f string for this next one but I don't think you can
    script.append('curl -u \'' + user + '\' https://api.github.com/user/repos -d \'{\"name\":\"' + repo + '\"}\'')
    script.append(f'git remote add origin https://github.com/{user}/{repo}.git')
    script.append('git branch -M main')
    script.append('git push -u origin main')
    output = '\n'.join(script)
    return output
if __name__ == "__main__":
    main()
