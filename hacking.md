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
  
  9. Set up bootloader
  
    a) GRUB for BIOS
    b) systemd-boot for UEFI
    
  10. Configure Bootloader
 
 
 Notable files for hacking
 ---
 
```

/usr/share/system-installer/installer.py
/usr/share/system-installer/modules/master.py
/usr/share/system-installer/modules/install_extras.sh
/usr/share/system-installer/modules/manual-partitioner.sh
/usr/share/system-installer/modules/systemd_boot_config.py

```