import os
import shutil
from .mod_utils import replace, set_current_setup, expand_dir

def upload(username, setup):
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    script = get_upload_script(setup_dir, username, setup)
    os.system(script)


def get_upload_script(path, user, repo):
    script = [
        f'cd {path}',
        'git init',
        'git add .',
        'git commit -m "Easyrice upload"',
        'curl -u \'' + user +
        '\' https://api.github.com/user/repos -d \'{\"name\":\"' + repo + '\"}\'',
        f'git remote add origin https://github.com/{user}/{repo}.git',
        'git branch -M main',
        'git push -u origin main'
    ]
    output = '\n'.join(script)
    return output


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
