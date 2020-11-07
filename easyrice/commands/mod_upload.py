import os

def main(username, setup):
    setup_dir = os.path.expanduser("~") + "/.config/easyrice/setups/" + setup
    script = get_upload_script(setup_dir, username, setup)
    os.system(script)

def get_upload_script(path, user, repo):
    script = []
    script.append(f'cd {path}')
    script.append('git init')
    script.append('git add .')
    script.append('git commit -m "Easyrice upload"')
    # It would be preferable if I could use f string for this next one but I don't think you can
    script.append('curl -u \'' + user + '\' https://api.github.com/user/repos -d \'{\"name\":\"' + repo + '\"}\'')
    script.append(f'git remote add origin https://github.com/{user}/{repo}.git')
    script.append('git branch -M main')
    script.append('git push -u origin main')
    output = '\n'.join(script)
    return output
