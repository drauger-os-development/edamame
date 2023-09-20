# Testing Distros

This list details which distros have been tested and are known working with `system-installer`. Config changes to get `system-installer` working are acceptable.

## To test:
 - [ ] Get the distro booted up in a VM or on a live USB/CD/DVD
 - [ ] Run `git clone https://github.com/drauger-os-development/system-installer` to clone the repo
 - [ ] `cd` into the folder: `cd system-installer`
 - [ ] Make any necessary changes to the default config to get `system-installer` to work.
 - [ ] Install Packages needed to build: `sudo apt install python3-dev libpython3-dev`
 - [ ] Build the package: `./build.sh`
 - [ ] Install the package: `sudo apt install ../system-installer_*.deb`
 - [ ] Run `system-installer` in a terminal and try to install the OS!

## When testing, please do these things:
 - [ ] Install using the auto-partitioner (on both EFI and BIOS)
 - [ ] Install using the manual partitioner (on both EFI and BIOS)
 - [ ] Install with and without Restricted Extras enabled

## For extra credit, try:
 - [ ] Installing using Quick Install
 - [ ] Installing using OEM install (this includes the End User Experience)
 - [ ] Sending an Installation Report
 - [ ] Installing with a RAID array configured in the installer


## Tested Distros ✅
✅ **Drauger OS 7.5.1** - KNOWN WORKING

✅ **Drauger OS 7.6** - KNOWN WORKING
