# Todo

## Must Add:
- [ ] Fix bad documentation
- [ ] CLONE: check for double folder when pulled
- [ ] UPLOAD: get it to work
  - [ ] Instead of uploading to github, you could just upload to a custom made github organization that hosts setups.
	  - [ ] This would actually be really good because setups will be prevented from having the same name
		- [ ] And I could maintain consistency
		- [ ] There should be a way that the creator can havve modifier priveleges, or push updates
			- [ ] It might not be a huge problem if they don't though, I could just add them as a PR.
				- [ ] Could add trusted individuals to the organization


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

- [ ] Add ability to transfer wallpaper and other assets

- [ ] It seems that i3-gaps just removes i3
  - [ ] Make sure this is the case and then remove i3 from requirements
  - [ ] Maybe remove i3 if i3-gaps is found in requirements automatically

- [ ] Add ability to pass -n SETUP_NAME for NEW.

- [ ] If set_active is called when the setup is already active, skip process
  - [ ] Unless the user wants to refresh settings
    - [ ] Could add -f --force option to set-active to force refresh

- [ ] Could possibly add a list of already installed packages so that the install requirements process is faster and doesn't have to run through all of the requirements
  - [ ] Might not be good because somebody might remove a package and confuse easyrice

- [ ] Quickly check if a package is installed before running install script with:

```
import subprocess
retval = subprocess.call(["which", "packagename"])
if retval != 0:
    print("Packagename not installed!")
```
- [ ] Fix weird naming and deprecated function in mod_new
