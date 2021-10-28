# Development Setup and Tools

The following packages are required in order to do development for `system-installer`. Most of these packages are available in most distributions of Linux and many come pre-installed in some distros.

 * `python3`
 * `gir1.2-gtk-3.0`
 * `p7zip-full`
 * `python3-parted`
 * `python3-gnupg`

The following are not required but may help out
 * `arch-install-scripts`
 * `coreutils`
 * `squashfs-tools`
 * `pylint`

 To install all of the dependencies at once, use
 ```bash
 sudo apt install -y python3 gir1.2-gtk-3.0 p7zip-full python3-parted python3-gnupg arch-install-scripts coreutils squashfs-tools pylint
 ```

You can find a number of tests to make sure your programs work correctly in the `tests` directory. These are currently tailored to how these programs are written, i.e. they work Python scripts. None of the UI is tested yet. Feel free to write more tests and request their addition in a pull request.

All Python code should conform to `PEP8` as closely as possible. If you open a pull request `pep8speaks` will provide feedback on your `PEP8` conformance.

A good rule of thumb is if your Python code gets a score of `7.5` or higher from `pylint`, and works correctly, the chances of having your pull request accepted is fairly high, but no pull request is guaranteed to be accepted.
