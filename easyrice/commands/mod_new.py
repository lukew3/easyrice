import os
import shutil
import configparser
from .mod_utils import replace, set_current_setup


def make_base(setupName, requirements_file=''):
    # Write base directory
    parent_dir = os.path.expanduser("~") + "/.config/easyrice/setups"
    setup_dir = parent_dir + "/" + setupName
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

    # Write window manager run command
    wm = requirements[0]
    # TODO: Check that the first item in requirements is a wm
    # If it is not, check the list of requirements for a wm
    # The current config file just conveys the same variable twice TODO: either remove run_wm_command or make use of it
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'window_manager': wm,
                         'run_wm_command': wm}
    with open(setup_dir + "/config", 'w') as configfile:
        config.write(configfile)

    """
    # Keeping this run_wm_command for a little bit until I'm sure of the direction I'm going with this
    run_wm_command = wm + " -c " + \
        os.path.expanduser("~") + "/.config/easyrice/setups/" + \
        setupName + "/dotfiles/" + wm + "/" + wm_config_filename
    """

    print("Base directory created")
    set_current_setup(setupName)


def copy(setupName):
    config_dir = os.path.expanduser("~") + "/.config"

    make_base(wm, setupName)

    this_setup_dir = config_dir + "/easyrice/setups/" + setupName
    base = ''
    if wm == 'bspwm':
        # add sxhkd dependency
        sxhkdrc_head = config_dir + "/sxhkd/sxhkdrc"
        sxhkdrc_base = this_setup_dir + "/dotfiles/sxhkd/sxhkdrc"
        shutil.copyfile(sxhkdrc_head, sxhkdrc_base)
        # add bspwm config titled bspwmrc
        bspwmrc_head = config_dir + "/bspwm/bspwmrc"
        bspwmrc_base = this_setup_dir + "/dotfiles/bspwm/bspwmrc"
        shutil.copyfile(bspwmrc_head, bspwmrc_base)
        # add sxhkd command to bspwmrc
        sxhkd_command = 'sxhkd -c ' + sxhkdrc_base + " &"
        replace(bspwmrc_base, 'sxhkd &', sxhkd_command)
        base = bspwmrc_base
    else:
        head = config_dir + "/" + wm + "/config"
        base = this_setup_dir + "/dotfiles/" + wm + "/config"
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
        polybar_config_base = this_setup_dir + "/dotfiles/polybar"
        shutil.copytree(polybar_config_head, polybar_config_base)
        print("Polybar config copied")
    # fix polybar references in window manager config
    original_polybar_call = ".config/polybar/launch.sh"
    new_polybar_call = ".config/easyrice/setups/" + setupName + "/dotfiles/polybar/launch.sh"
    replace(base, original_polybar_call, new_polybar_call)

    # Set easyrice to run this setup on startup
    set_current_setup(setupName)
    # It would help if you could run your wm like you usually would and easyrice
    # would detect which apps started up before you started using the environment
    # Then those apps would be added to requirements.txt and their configs added to app_config folder


def replace_dotfiles():
    pass


def backup_dotfiles():
    pass
