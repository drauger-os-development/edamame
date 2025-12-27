# Testing Distros

This list details which distros have been tested and are known working with `edamame`. Config changes to get `edamame` working are acceptable.

## To test:
 - [ ] Get the distro booted up in a VM or on a live USB/CD/DVD
 - [ ] Run `git clone https://github.com/drauger-os-development/edamame` to clone the repo
 - [ ] `cd` into the folder: `cd edamame`
 - [ ] Make any necessary changes to the default config to get `edamame` to work.
 - [ ] Install Packages needed to build: `sudo apt install python3-dev libpython3-dev`
 - [ ] Build the package: `./build.sh --pool`
 - [ ] Install the package: `sudo apt install ./build/*`
 - [ ] Run `edamame` in a terminal and try to install the OS!

## When testing, please do these things:
 - [ ] Install using the auto-partitioner (on both EFI and BIOS)
 - [ ] Install using the manual partitioner (on both EFI and BIOS)
 - [ ] Install with and without Restricted Extras enabled
 - [ ] Install with and without Update During Install enabled

## For extra credit, try:
 - [ ] Installing using Quick Install
 - [ ] Installing using OEM install (this includes the End User Experience)
 - [ ] Sending an Installation Report
 - [ ] Installing with a RAID array configured in the installer


## Tested Distros ✅
✅ **Drauger OS 7.5.1** - KNOWN WORKING

✅ **Drauger OS 7.6** - KNOWN WORKING

✅ **Drauger OS 7.7** - KNOWN WORKING
