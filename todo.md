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

- [ ] It is probably important to be able to test your setup without regarding your previously installed packages.
  - [ ] This can be achieved by creating a seperate user profile with no installed packages and then deleting that profile after testing

- [ ] Might need a dependency requirement file that is only edited by the computer
   - [ ] Holds the names of the packages that need to be installed in order for requirements to be installed

- [ ] REMOVE: If the current active setup is about to be removed, inform the user and ask if they want to continue(y/n)
  - [ ] Tell them how to set new active setup

- [ ] On startup, config files should be replaced with setup config files.
  - [ ] Config files should be replaced on close, but this is easier said than done

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
- [ ] Fix weird naming and deprecated function in mod_new
- [ ] When creating the wm run command make sure that the wm is correctly identified in the list of requirements. Currently it is identified by being the first requirement in the list. Possibly have a list of possible wms and if an item is on requirements list and wm list, that is the wm. If no common package is found, just use the first item in the list.

- [ ] Test if upload works for users outside of organization owners

- [ ] Remove newline character from last item of requirements_list in NEW

- [ ] Maybe localize wallpaper after configs are transferred?
  - [ ] This would fix broken references to wallpapers when setups are deleted

- [ ] Add simple cookiecutter readme to repos uploaded to github

- [ ] UPLOAD: If user doesn't accept request before clicking enter, upload it on behalf of easyrice-community
