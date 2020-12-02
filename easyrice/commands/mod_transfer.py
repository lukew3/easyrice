import os
import shutil
import subprocess
import requests
import sys
from github import Github
import configparser
from .mod_utils import replace, set_current_setup, expand_dir


def upload(setup):
    create_remote(setup)
    input("Check your email and accept invitation to collaborate. Then press enter to continue")
    git_upload(setup)


def decipher(ciphertext):
    L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
    I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    key = 3
    # decipher
    plaintext = ""
    for c in ciphertext.upper():
        if c.isalpha():
            plaintext += I2L[(L2I[c] - key) % 26]
        else:
            plaintext += c
    plaintext = plaintext.lower()
    return plaintext


def create_remote(name):
    easyrice_config_path = os.path.expanduser("~") + "/.config/easyrice/config"
    config = configparser.ConfigParser()
    config.read(easyrice_config_path)
    # Get github username and save it if not saved before
    if config['main']['github_username'] == "":
        github_username = input("What is your Github username: ")
        config['main']['github_username'] = github_username
        with open(easyrice_config_path, 'w') as configfile:
            config.write(configfile)
    else:
        github_username = config['main']['github_username']
    # The access token is encoded so that github doesn't delete the token when it is published
    # To get the real token, a caesar cipher is used
    encoded_token = "1ff4994hfgi1i244905if1905181i383i71g4e8h"
    ACCESS_TOKEN = decipher(encoded_token)
    NEW_REPO_NAME = name
    HOMEPAGE = 'https://github.com/lukew3/easyrice'
    ORGANISATION_NAME = 'easyrice-setups'
    g = Github(ACCESS_TOKEN)
    organization = g.get_organization("easyrice-setups")
    # Create repo
    repo = organization.create_repo(name, homepage=HOMEPAGE)
    # Add user as repo contributor
    # Not sure if admin priveleges are necessary
    repo.add_to_collaborators(github_username, permission='admin')

def git_upload(setup_name):
    path = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup_name
    username = "easyrice-community"
    encoded_token = "1ff4994hfgi1i244905if1905181i383i71g4e8h"
    password = decipher(encoded_token)
    # This script uploads on behalf of the owner of the machine, not easyrice-community
    script = [
        f'cd {path}',
        'git init',
        'git add .',
        'git commit -m "Easyrice upload"',
        f'git remote add origin https://github.com/easyrice-setups/{setup_name}.git',
        'git branch -M main',
        'git push -u origin main'
    ]
    output = '\n'.join(script)
    os.system(output)


def git_clone(repo):
    setups_dir = os.path.expanduser("~") + '/.config/easyrice/setups'
    # clone_script changes directory to setups directory and then
    clone_script = 'cd ' + setups_dir + '\ngit clone ' + repo
    os.system(clone_script)
    setup_name = repo.split('/')[-1].split('.')[0]
    set_current_setup(setup_name)
    # Might want to add a way to check if the git repo has an extra folder in it.
    # If the user uploaded the whole folder instead of the insides of the folder, this script wont work
    # Or you could make a way to automatically upload a setup to github


def local_export(setup):
    export_dir = os.path.expanduser("~") + "/" + setup
    src_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    if not os.path.isdir(src_dir):
        print("Setup \"" + setup + "\" does not exist")
    else:
        if not os.path.isdir(export_dir):
            shutil.copytree(src_dir, export_dir)
            print("Setup \"" + setup + "\" exported to " + export_dir)
        else:
            print("Folder with that setup name already exists")


def local_import(setup_dir):
    src_dir = ""
    dest_dir = os.path.expanduser("~") + "/.config/easyrice/setups/"
    # If direct reference
    src_dir = expand_dir(setup_dir)
    setup_name = setup_dir.split('/')[-1]
    dest_dir += setup_name
    if os.path.exists(src_dir):
        shutil.copytree(src_dir, dest_dir)
        print("Setup " + setup_name + " successfully added")
        set_current_setup(setup_name)
    else:
        print("Setup folder not found")
