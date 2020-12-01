# easyrice
A tool for sharing unix configurations, also known as ricing. Adds the ability to use different settings for the same window manager. Also allows for setups to be easily shared.

## Install
Right now, this can only be installed from source. To do this, you can run the following commands:
```
git clone https://github.com/lukew3/easyrice.git
cd easyrice
sudo make install
```

## Usage
Use `easyrice copy-current` to copy your current setup and save it as a easyrice setup. Once you have tweaked your setup config files to work seperately from any config files on your pc, you are ready to copy and upload your setup folder to share with others.

## .config/easyrice structure
```
easyrice
├── config
└── setups
    └── first
        ├── dotfiles
        │   └── i3
        │       └── config
        ├── assets
        │   └── wallpaper.png
        ├── config
        └── requirements.txt
```

## easyrice --help
```
Usage: easyrice [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add         Imports a setup folder into easyrice
  clone       Clones a setup from a passed git remote repository
  export      Export given setup to home directory
  list        Lists all setups in easyrice config
  new         Creates a new setup directory.
  remove      Delete an existing setup
  rename      Rename an existing setup
  revert      Reverts configs to what they were before the current setup
  set-active  Sets the passed setup as active setup
  upload      Uploads passed setup to your github
```
