import os
import shutil
import configparser
from .mod_utils import replace, set_current_setup


def make_setup(setup_name, requirements_file=''):
    # Write base directory
    parent_dir = os.path.expanduser("~") + "/.config/easyrice/setups"
    setup_dir = parent_dir + "/" + setup_name
    os.makedirs(setup_dir + "/assets")
    os.makedirs(setup_dir + "/dotfiles")
    open(setup_dir + "/requirements.txt", 'a').close()

    # If requirements file is not passed, collect requirements
    if requirements_file == '':
        req = 'not empty'
        f = open(setup_dir + "/requirements.txt", 'a')
        print("Please add each requirement one at a time. Start with the window manager and then other packages necessary for your setup.")
        print("Once you have added all necessary requirements, press enter without typing any input")
        while req != '':
            req = input("> ")
            # TODO: ideally, req should be checked to see if it is a valid package
            if req != '':
                f.write(req + "\n")
        f.close()
    elif requirements_file != '':
        print(requirements_file)
        setup_requirements_file = setup_dir + "/requirements.txt"
        shutil.copyfile(requirements_file, setup_requirements_file)

    # Transfer all .config files of required packages to setup dotfiles folder
    requirements = open(setup_dir + "/requirements.txt", 'r').read().splitlines()
    for req in requirements:
        # If folder exists in .config, copy that folder to setup's dotfile
        local_req_config_dir = os.path.expanduser("~") + "/.config/" + req
        setup_req_config_dir = setup_dir + "/dotfiles/" + req
        if os.path.isdir(local_req_config_dir):
            shutil.copytree(local_req_config_dir, setup_req_config_dir)
            print("Requirement " + req + " config copied successfully")
        else:
            print("Requirement " + req + " config not found")

    # Gets window manager, checks requirements for commonly used wm and uses first requirement if not found in common_wms
    common_wms = ['i3', 'i3-gaps', 'bspwm', 'awesome', 'openbox']
    wm = ""
    for item in requirements:
        if item in common_wms:
            wm = item
            break
    if wm == "":
        wm = requirements[0]

    config = configparser.ConfigParser()
    # Not sure if run_wm_command should be removed or not
    config['DEFAULT'] = {'window_manager': wm,
                         'run_wm_command': wm}
    with open(setup_dir + "/config", 'w') as configfile:
        config.write(configfile)
    print("Base directory created")
    set_current_setup(setup_name)
    # Get name of wm config file and move wallpaper to setup assets
    wm_config_folder = setup_dir + "/dotfiles/" + wm
    # The listdir[0] way of doing this might not work in wm's with lots of config files, but it works for the top 3 at least
    wm_config_file = wm_config_folder + '/' + os.listdir(wm_config_folder)[0]
    if os.path.exists(wm_config_file):
        get_wallpaper(wm_config_file, setup_name)
    # Create README
    readme_location = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup_name + "/README.md"
    f = open(readme_location, 'a')
    f.write("# " + setup_name + "\n")
    f.close()
    print("README.md created")
    print("New setup created successfully")


def get_wallpaper(wm_config_file, setup_name):
    wallpaper_head = ''
    wallpaper_base = ''
    f = open(wm_config_file, "r")
    for line in f:
        if 'feh' in line:
            wallpaper_head = line.rsplit(None, 1)[-1]
            wallpaper_name = wallpaper_head.rsplit('/', 1)[1]
            wallpaper_base = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup_name + "/assets/" + wallpaper_name
            # Changes reference in wm config to new wallpaper location in assets folder
            replace(wm_config_file, wallpaper_head, wallpaper_base)
            break
    f.close()
    if wallpaper_head != '':
        if wallpaper_head[0] == '~':
            wallpaper_head = os.path.expanduser("~") + wallpaper_head[1:]
        shutil.copyfile(wallpaper_head, wallpaper_base)
        print("Wallpaper copied")
