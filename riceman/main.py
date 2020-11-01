import os
import shutil
import configparser


def main():
    install_config()


def read_config():
    user_config_dir = os.path.expanduser("~") + "/.config/ricemantest"
    user_config = user_config_dir + "/config"

    # if not os.path.isfile(user_config):
    #    os.makedirs(user_config_dir, exist_ok=True)
    #    shutil.copyfile("config", user_config)

    config = configparser.ConfigParser()
    config.read(user_config)

    print(config['section']['setting_1'])
    print(config['section']['setting_2'])


def install_config():
    # Make base directory and configs for install
    user_config_dir = os.path.expanduser("~") + "/.config/ricemantest"
    user_config = user_config_dir + "/config"
    user_setups_dir = user_config_dir + "/setups"

    if not os.path.isfile(user_config):
        # The make config dir is unecessary but I'm not sure if it's best practice to keep it or not
        os.makedirs(user_config_dir, exist_ok=True)
        os.makedirs(user_setups_dir, exist_ok=True)
        shutil.copyfile("config", user_config)

    # Write xsessions desktop file
    environment_file = "/usr/share/xsessions/riceman.desktop"
    shutil.copyfile("riceman.desktop", environment_file)


def copy_current():
    # This could be used to copy the users current setup
    # Maybe grab the config in i3 or whatever is specified and then
    # grab dependencies from that
    pass


if __name__ == "__main__":
    main()
