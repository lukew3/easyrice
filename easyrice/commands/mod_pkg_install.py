import os

git_url_dict = {
    'bspwm': 'https://github.com/baskerville/bspwm.git',
    'sxhkd': 'https://github.com/baskerville/sxhkd.git',
}

# Types guide is as follows:
"""
d: debian 'apt' repo available
f: fedora 'dnf' repo available
u: ubuntu 'apt-get' repo available
# Arch support is necessary, but I don't understand it much right now, I think aur is how you use it though
a: arch 'aur' repo available

#Install from source methods
0: No install from source available
1: `make & sudo make install` in top directory

"""
install_type_dict = {
    'bspwm': [1],
    'sxhkd': [1],
    ''
}

def get_install_script(package, distro_name):
    git_url = git_url_dict[package]
    install_method = install_type_dict[package]
    install_method_line = ''

    if install_method[0] == 1:
        install_method_line = 'make & sudo make install'
    script_list = [
        'git clone ' + clone_url,
        'cd ' + package_name,
        install_method_line,
        'cd ..',
        'rm -rf ' + package_name
    ]
    script = '\n'.join(script_list)
    return script


def bspwm(distro):
    bspwm_config_dir = os.path.expanduser("~") + "/.config/bspwm"
    script_list = [
        'git clone <a href="https://github.com/baskerville/bspwm.git" rel="nofollow">https://github.com/baskerville/bspwm.git</a>',
        'cd bspwm',
        'make & sudo make install',
        'mkdir ' + bspwm_config_dir,
        'mv /bspwm/examples/bspwmrc ' + bspwm_config_dir + '/bspwmrc'
        'chmod +x ' + bspwm_config_dir + '/.config/bspwm/bspwmrc'
    ]
    script = '\n'.join(script_list)
    return script

def sxhkd(distro):
    sxhkd_config_dir = os.path.expanduser("~") + "/.config/sxhkd"
    script_list = [
        'git clone <a href="https://github.com/baskerville/sxhkd.git" rel="nofollow">https://github.com/baskerville/sxhkd.git</a>',
        'cd sxhkd',
        'make & sudo make install',
        'mkdir ' + sxhkd_config_dir,
        'mv /sxhkd/examples/sxhkdrc ' + sxhkd_config_dir + '/sxhkdrc'
        'chmod +x ' + sxhkd_config_dir + '/.config/sxhkd/sxhkdrc'
    ]
    script = '\n'.join(script_list)
    return script
