# Todo

## Priority 1: Needs to be done before Beta release

- [ ] Wallpaper doesn't work when setup renamed because reference in config isn't edited
  - [ ] Maybe localize wallpaper after configs are transferred?
    - [ ] This would fix broken references to wallpapers when setups are deleted

- [ ] CLI: Make sure that cli follows standards and works similarly to other clis
  - [ ] Could head over to reddit r/commandline to see if they can help me out before release

- [ ] Find out if `install_config` method is the best way to initialize .config files (I'm almost certain it's not)

- [ ] Tell users what packages were not able to be installed automatically

- [ ] Fix annoying requirements installation when it's not always necessary
  - [ ] Could check installed packages from shell and then try to install if not found

## Priority 2: Needs to be done before regular release

- [ ] UPLOAD: If user doesn't accept request before clicking enter, upload it on behalf of easyrice-community

- [ ] Quickly check if a package is installed before running install script with:

```
import subprocess
retval = subprocess.call(["which", "packagename"])
if retval != 0:
    print("Packagename not installed!")
```

- [ ] If set_active is called when the setup is already active, skip process
  - [ ] Unless the user wants to refresh settings
    - [ ] Could add -f --force option to set-active to force refresh
    - [ ] It seems that i3-gaps just removes i3
      - [ ] Make sure this is the case and then remove i3 from requirements
      - [ ] Maybe remove i3 if i3-gaps is found in requirements automatically

## Priority 3: Nice improvements

- [ ] It would be nice if on startup, config files should be replaced with setup config files.
  - [ ] Config files should be replaced on close, but this is easier said than done
  - [ ] You also have to take into consideration installing the requirements

- [ ] CLONE: check for double folder when pulled
  - [ ] Doesn't need to be done if cloning is always done from easyrice-setups github organization

- [ ] If a package is not recognized when configuringrequirements, the user should be given an alternatepredicted title for the package, if that name is correct,the package  name should be corrected.
  - [ ] There might be a possibility that you could suggestrequirements to add based on installed packages and youwould just have to confirm that you want to save those requirements
    - [ ] Show a numbered list of requirements that areinstalled on your computer and are common in ricingsetups. Then type a list with numbers seperated by aspace to save to  requirements
      - [ ] The following script should return a list of all manually installed packages
 			  - [ ] `comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u)`

- [ ] INSTALL: Users should be able to use the install command to install a dependency on the users pc, then move the .config into the setups dotfile location
  - [ ] Not sure if I like this one anymore

- [ ] Clean up comments, put them in todo list

- [ ] Fix inconsistencies

- [ ] Add ability to add custom .desktop entries to desktop environment manager
 	- [ ] You can have a seperate entry for each setup you want to use on a regular basis

## Unsorted random ideas

- [ ] Maybe I could make a python package that can install from source for different projects
  - [ ] Pretty much just the mod_pkg_install thing but usable and installable outside of easyrice
