import os

def main(username, setup):
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    script = get_upload_script(setup_dir, username, setup)
    os.system(script)

def get_upload_script(path, user, repo):
    script = [
    f'cd {path}',
    'git init',
    'git add .',
    'git commit -m "Easyrice upload"',
    'curl -u \'' + user + '\' https://api.github.com/user/repos -d \'{\"name\":\"' + repo + '\"}\'',
    f'git remote add origin https://github.com/{user}/{repo}.git',
    'git branch -M main',
    'git push -u origin main'
    ]
    output = '\n'.join(script)
    return output
