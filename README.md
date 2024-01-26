# Edamame
System Installation Utility for Drauger OS.

**Formerly known as `system-installer`**

`edamame` aims to provide a fast, modular method of installing a Debian-based operating system. As of now, it is not advised for use on systems that Linux new-comers will frequent, due to it's reliance upon `gparted` and the users understanding of how partitioning works.


[Click here to view the current list of known bugs](https://github.com/drauger-os-development/edamame/blob/master/known-bugs.md)

[Click here to view the list of planned features](https://github.com/drauger-os-development/edamame/blob/master/planned-features.md)

[Click here for notes on hacking on `edamame`](https://github.com/drauger-os-development/edamame/blob/master/hacking.md)

`edamame` currently is known working only on Drauger OS, but is being adapted to work on other Debian-based OSs as well. `edamame` is designed NOT to be specific to Drauger OS. So testing on other distros is encouraged!


## Notable features


 * Add PPAs inside the installer, post installation
 * Quick-install config file support
 * One of the *fastest* installation utilities in Linux today (1-to-2.5 minutes (ish)) on a quad-core CPU with 4 GB of RAM and decent, reliable internet)


## Development


 Interested in helping out with development? Great! Check out the notes on how to get started with development [here](https://github.com/drauger-os-development/edamame/blob/master/development.md).

## Other Notes


### `edamame` requires `systemd`
This drawback is in place for a number of reasons:
 * `systemd-boot` is easier and more reliable to install on UEFI than GRUB
 * `systemd` makes setting up everything from keyboard to language to time significantly easier
 * `systemd` is present on most Linux systems

### `edamame` uses `GRUB` on `BIOS`, `systemd-boot` on `UEFI`
 * `systemd-boot` does not support BIOS
 * `GRUB` is a pain on UEFI

### Max 40+ MB *.deb
The *.deb is currently +40 MB because it packs a kernel to install inside the *.deb file.

This can be circumvented by passing the `--pool` flag to `build.sh`, and results in a *.deb with no kernel archive. To use this DEB, please be sure to have a folder in your ISO storing all necessary packages (kernel and systemd-boot-manager) and have that folder defined in `etc/edamame/settings.json`. 
