import os

def get_install_script(package, distro_name):

    pass


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
