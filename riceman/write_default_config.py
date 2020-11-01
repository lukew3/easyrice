import configparser

config = configparser.ConfigParser()

config.add_section('section')
config['section']['setting_1'] = "hello"
config['section']['setting_2'] = "goodbye"

with open("config", 'w') as f:
    config.write(f)
