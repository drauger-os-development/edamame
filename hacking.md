HACKING
---

Hacking on `system-installer` is meant to be relatively easy. Some points of note:

 * Most scripts in `/usr/share/system-installer/modules` are copied into the `chroot` during the configuration portion of the installation
 * If you want to have something else done during installation, perform the following:
   * In `master.py` in the `MainInstallation` class, write a function to perform the action you need.
   * Do not put `self` in  the arguments
   * Put arguments in all caps so that when the process for your function is started, it receives the data it needs
   * Do not pre-pend the function with an underscore (_) or it will not be executed.
     * If you wish to make a helper function, you may add it to the class, as long as you pre-pend it with an underscore (_) so that it will not be mistakenly executed.


However, there are some limitations:

 * Anything with "partitioner" in the name in `/usr/share/system-installer/modules` will not be copied into the `chroot`
 * `dpkg` and it's front end `apt` must be present for installation, as they are used for installing the kernel
 * A file, `kernel.7z`, is created upon creation of the *.deb package. This file is necessary as it provides a fall-back kernel for installation when the internet is inaccessible.
 
 
Installation Procedure
---
  1. Obtain user settings - Partition the drive if needed
   
  2. Mount the partitions in the places they will be in the finished system, this includes swap if it is already present.
  
  3. Extract the squashfs, the path to which is defined in `/etc/system-installer/default.json`
  
  4. Move the files extracted from the squashfs to the installation directory - this is to circumvent a bug with `unsquashfs` where it won't actually place the files where they are supposed to go. It will instead make a folder named `squashfs-root`, and extract the squashfs there.
  
  5. use the `chroot` function in `chroot.py` to `chroot` into the newly created OS and configure the installation
  
  6. Set up keyboard, time zone, language, username, password, auto-login (if set). Install updates and restricted extras if needed. This is all done in parallel, except things pertaining to the package manager, which is done sequentially.
  
  7. Install the kernel
  
  8. Make an initramfs
  
  9. Set up & configure bootloader
  
    a) GRUB for BIOS
    b) systemd-boot for UEFI
  
  
Project Layout
---

System Installer is designed to be as modular as possible. While it still has a long way to go, there are 2 main modules:

- UI Module
 	- Located at `/usr/share/system-installer/UI`
 	- Essential Functions:
 		- `UI.error.show_error()`
 			- Takes a markup formatted string
 			- displays string as an error to the user
 		- `UI.main.show_main()`
 			- Takes no arguments
 			- Retreives Settings from user
 			- Returns either a dictionary of settings, or a file path to pull settings from
 		- `UI.confirm.show_confirm()`
 			- Takes settings, each entry in the dictionary, as an argument
 			- Displays settings to user, to confirm them for accuracy
 			- Returns a Boolean, True for proceed, False for halt
 		- `UI.progress.show_progress()`
 			- Takes no arguments
 			- Returns `None`
 			- Monitors `/tmp/system-installer.log` and `/tmp/system-installer-progress.log` to show the user what is being done during install and how far along install is.
 		- `UI.success.show_success()`
 			- Takes settings dictionary as argument
 			- Shows user installation success window
 			- Allows user to dump settings to JSON file for usage with Quick Install later on
 				- Also will grab network settings, wallpaper, and more if requested. A spec for Quick Install formatting will be released later.
 			- All other functions included in this window are at the developer's discretion as nothing else is used elsewhere in System Installer
 			- Returns `None`
 			
- Installation Module
	- Located at `/usr/share/system-installer/modules`
	- The installation module can be further broken down into sub modules, each with it's own segment of installation it works on.
	- Everything in this module is orchestrated by the `master.py` file
	- Essential Functions:
		- `modules.master.check_internet()`
			- Takes no arguments
			- Checks for internet access
			- Returns Boolean, True if internet access present, False if not present
		- `modules.master.install()`
			- Takes two arguments: settings dictionary, modules.master.check_internet() return value
			- Handles installation procedure
			- Returns `None`
			- Should be multi-threaded in order to speed up installation
				- The stock function is multi-threaded using the multiprocessing library
	
The UI module is the most replaceable module. As long as the necessary functions are available to `engine.py`, it can easily be replaced with a Qt UI, a GTK UI that looks totally different, or something else!


Settings
---

Settings are defined in `/etc/system-installer/default.json`

 - `squashfs_location`
   - Location of the squashfs file to unpack
 - `distro`
   - Name of the distro `system-installer` is running on. Use thise for branding.
 - `report_to`
   - Email address to send installation reports to
     - Must be a valid email address
     - Installation reporting is opt-in only
 - `ping servers`
   - URLs to ping to check for internet access
   - DO NOT use IP addresses.
     - While IP addresses will work, DNS resolution will not be checked if they are used
   - Optimal with 2 - 4 URLS
 - `ping count`
   - Number of times to ping each URL in `ping servers`
     - Higher numbers increase the likelyhood of internet working correctly
     - Lower numbers decrese installation time on slow internet connections
   - Optimal when 2 or 3
 - `partitioning`
   - Partitioning layout when using automatic partitioning
   - This is the ONLY entry here that is optional. If `partitioning` is not defined, an internally stored default will be used instead.
   - Entries that must be defined
     - `EFI`
     - `ROOT`
     - `HOME`
     - `min root size`
     - `mdswh`
   - `EFI`, `ROOT`, and `HOME` configuration entries
     - `START` and `END` define the start and end points of the partitions
     - `fs` filesystem type to use for the partition, not honored for `EFI`
     - All of supported entries must be defined in each of `ROOT`, `HOME`, or `EFI`
   - `min root size` must be an integer that dictates the minimum size of the root partition in MiB
   - `mdswh` stands for 'minimum drive size with home', and is the size smallest drive you can install Drauger OS to and have a seperate `/home` partition on the same drive.
 
Notable files for hacking
---
 
```
/usr/share/system-installer/installer.py
/usr/share/system-installer/modules/master.py
/usr/share/system-installer/modules/install_extras.sh
/usr/share/system-installer/modules/manual-partitioner.sh
/usr/share/system-installer/modules/systemd_boot_config.py
/etc/system-installer/default.json

```