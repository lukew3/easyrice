# Todo

## Must Add:
- [ ] Fix bad documentation
- [ ] CLONE: check for double folder when pulled
- [ ] UPLOAD: Test upload with user outside of the easyrice-setups organization
  - [ ] Could do this myself with an alternate account
- [ ] CLI: Make sure that cli follows standards and works similarly to other clis
  - [ ] Could head over to reddit r/commandline to see if they can help me out before release


## Should Add

- [ ] Clean up comments, put them in todo list
- [ ] Fix inconsistencies
- [ ] Add ability to add custom .desktop entries to desktop environment manager
 	- [ ] You can have a seperate entry for each setup you want to use on a regular basis
- [ ] Decide if setups should have README's automatically generated when they upload to github
- [ ] UPLOAD: If github repo already exists, don't attempt to create a new repo. Instead, just add and commit current changes
- [ ] INSTALL: Users should be able to use the install command to install a dependency on the users pc, then move the .config into the setups dotfile location

- [ ] If a package is not recognized when configuring requirements, the user should be given an alternate predicted title for the package, if that name is correct, the package  name should be corrected.
  - [ ] There might be a possibility that you could suggest requirements to add based on installed packages and you would just have to confirm that you want to save those  requirements
    - [ ] Show a numbered list of requirements that are installed on your computer and are common in ricing setups. Then type a list with numbers seperated by a space to save to  requirements
      - [ ] The following script should return a list of all manually installed packages
 			  - [ ] comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u)
        
- [ ] It would be nice if on startup, config files should be replaced with setup config files.
  - [ ] Config files should be replaced on close, but this is easier said than done
  - [ ] You also have to take into consideration installing the requirements

- [ ] It seems that i3-gaps just removes i3
  - [ ] Make sure this is the case and then remove i3 from requirements
  - [ ] Maybe remove i3 if i3-gaps is found in requirements automatically

- [ ] If set_active is called when the setup is already active, skip process
  - [ ] Unless the user wants to refresh settings
    - [ ] Could add -f --force option to set-active to force refresh

- [ ] Quickly check if a package is installed before running install script with:

```
import subprocess
retval = subprocess.call(["which", "packagename"])
if retval != 0:
    print("Packagename not installed!")
```

- [ ] Maybe localize wallpaper after configs are transferred?
  - [ ] This would fix broken references to wallpapers when setups are deleted

- [ ] UPLOAD: If user doesn't accept request before clicking enter, upload it on behalf of easyrice-community

- [ ] Add a copy argument to copy a setup to a new setup with everything the same except for the setup name

- [ ] Find out if `install_config` method is the best way to initialize .config files (I'm almost certain it's not)
