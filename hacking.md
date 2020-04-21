HACKING
---

Hacking on `system-installer` is meant to be relatively easy. Some points of note:

 * Most scripts in `/usr/share/system-installer/modules` are copied into the `chroot` during the configuration portion of the installation
 * Any scripts copied into said `chroot` will have access to environmental variables containing most, if not all, necessary data for installation
   * These environmental variables only exist for what is ideally a short time: the configuration step of installation
   * They are created from within the `chroot`, so they should not be accessible outside of it.
   * Once the `chroot` is closed, all environmental variables are lost


However, there are some limitations:

 * Anything with "partitioner" in the name in `/usr/share/system-installer/modules` will neither be copied into the `chroot`, nor have access to any environmental variables
 * `dpkg` and it's front end `apt` must be present for installation, as they are used for installing the kernel
 * No part of the GUI has access to any environmental variables
 * A file, `kernel.7z`, is created upon creation of the *.deb package. This file is necessary as it provides a fall-back kernel for installation when the internet is inaccessible.
 
 
 Installation Procedure
 ---
  1. Obtain user settings - Partition the drive if needed
   
  2. Mount the partitions in the places they will be in the finished system, this includes swap if it is already present.
  
  3. Extract the squashfs, the path to which is defined in `/etc/system-installer/default.config`
  
  4. Move the files extracted from the squashfs to the installation directory - this is to circumvent a bug with `unsquashfs` where it won't actually place the files where they are supposed to go. It will instead make a folder named `squashfs-root`, and extract the squashfs there.
  
  5. use `arch-chroot` to `chroot` into the newly created OS and configure the installation
  
  6. 
 
 
 Notable files for hacking
 ---
 
```

/usr/share/system-installer/installer.sh
/usr/share/system-installer/modules/MASTER.sh
/usr/share/system-installer/modules/install_extras.sh
/usr/share/system-installer/modules/manual-partitioner.sh
/usr/share/system-installer/modules/systemd_boot_config.py

```