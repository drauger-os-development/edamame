# Development Setup and Tools

The following packages are required in order to do development for `system-istaller`. Most of these packages are available in most distributions of Linux and many come pre-installed in some distros.

 * `shellcheck`
 * `python3`
 * `python-gtk2`
 * `bash`
 * `procps`
 * `grep`
 * `zenity`
 * `bc`
 * `p7zip-full`
 
The following are not required but may help out
 * `arch-install-scripts`
 * `coreutils`
 * `squashfs-tools`
 
 You can find a number of tests to make sure your programs work correctly in the `tests` directory. These are currently tailored to how these programs are written, i.e. they work on BASH scripts and the one Python script ran in the back end. None of the UI is tested yet.