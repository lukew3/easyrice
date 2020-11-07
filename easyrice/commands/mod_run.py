import os
import configparser

def main(setup):
    os.system(get_run_command(setup))

def get_run_command(setup_name):
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
