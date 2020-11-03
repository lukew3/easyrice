# riceman
A tool for sharing unix configurations, also known as ricing. Adds the ability to use different settings for the same window manager. Also allows for setups to be easily shared.

## Install
Right now, this can only be installed from source. To do this, you can run the following commands:
```
git clone https://github.com/lukew3/riceman.git
cd riceman
sudo make install
```

## Usage
Use `riceman copy-current` to copy your current setup and save it as a riceman setup. Once you have tweaked your setup config files to work seperately from any config files on your pc, you are ready to copy and upload your setup folder to share with others.

## .config/riceman structure
```
riceman
├── config
└── setups
    └── first
        ├── app_configs
        │   └── i3
        │       └── config
        ├── assets
        │   └── retrolinuxdark.png
        ├── config
        └── requirements.txt
```

## riceman --help
```
Usage: riceman [OPTIONS] COMMAND [ARGS]...

  Runs the setup selected in config or the command passed

Options:
  -s, --setup-name TEXT  Include the name of the setup you want to use
  --help                 Show this message and exit.

Commands:
  copy-current  Copies your current setup made outside of riceman
  delete-setup  Delete an existing setup
  new-setup     Creates a new setup with empty directories
  rename-setup  Rename an existing setup
```
