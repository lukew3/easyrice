import os
import shutil
import configparser
from .mod_utils import replace, set_current_setup

def make_base(wm, setupName):
    parent_dir = os.path.expanduser("~") + "/.config/easyrice/setups"
    setup_dir = parent_dir + "/" + setupName
    os.makedirs(setup_dir + "/assets")
    os.makedirs(setup_dir + "/app_configs")
    open(setup_dir + "/requirements.txt", 'a').close()
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


def copy(wm, setupName):
    config_dir = os.path.expanduser("~") + "/.config"

    make_base(wm, setupName)

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
