# Development Setup and Tools

The following packages are required in order to do development for `system-istaller`. Most of these packages are available in most distributions of Linux and many come pre-installed in some distros.

 * `shellcheck`
 * `python3`
 * `gir1.2-gtk-3.0`
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
 
You can find a number of tests to make sure your programs work correctly in the `tests` directory. These are currently tailored to how these programs are written, i.e. they work on BASH scripts and the one Python script ran in the back end. None of the UI is tested yet. Feel free to write more tests and request their addition in a pull request.
 
 
Any and all shell scripts will eventually be converted to Python 3 or C/C++, preferably performing the same operations in as multi-threaded a fashion as possible, in order to accelerate installation. Furthermore, as time progresses, `system-installer` should become increasingly modular in order to allow others to change `system-installer` to better fit their needs and use case.


All Python code should conform to `PEP8` (excluding W191, tabs prefered) as closely as possible. 