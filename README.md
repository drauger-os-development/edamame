# system-installer
System Installer for Drauger OS.

`system-installer` aims to provide a fast, modular method of installing a Debian-based operating system. As of now, it is not advised for use on systems that Linux new-comers will frequent, due to it's reliance upon `gparted` and the users understanding of how partitioning works.


[Click here to view the curreent list of known bugs](https://github.com/drauger-os-development/system-installer/blob/master/known-bugs.md)

[Click here to view the list of planned features](https://github.com/drauger-os-development/system-installer/blob/master/planned-features.md)

`system-installer` currently works only on Drauger OS, but may be adapted to work on other Debian-based OSs later. 


 Notable features
---

 * Add PPAs inside the installer, post installation
 * `chroot` access to the installed system, from within the installer
 * Quick-install config file support
 * One of the *fastest* installation utilities in Linux today (2-to-3 minutes (ish)) on a quad-core CPU with 4 GB of RAM and decent, reliable internet)
 
 
 Development
 ---
 
 Interested in helping out with development? Great! Check out the notes on how to get started with development [here](https://github.com/drauger-os-development/system-installer/blob/master/development.md).