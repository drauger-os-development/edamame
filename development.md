# Development environment setup

The following packages are required in order to do development for `system-installer`. Most of these packages are available in most distributions of Linux and many come pre-installed in some distros.

 * `python3`
 * `gir1.2-gtk-3.0`
 * `p7zip-full`
 * `python3-parted`
 * `python3-gnupg`
 * `libpython3.9-dev`

The following are not required but may help out
 * `arch-install-scripts`
 * `coreutils`
 * `squashfs-tools`
 * `pylint`

 To install all of the dependencies at once, use
 ```bash
 sudo apt install -y python3 gir1.2-gtk-3.0 p7zip-full python3-parted python3-gnupg libpython3.9-dev arch-install-scripts coreutils squashfs-tools pylint
 ```

# How to get started

Do you know some programming and want to help out, but haven't worked on someone else's codebase before?  This section is here for you.  These are some recommended steps on how to contribute without diving into specifics.

1. Create a Github account (if necessary)
    * It is strongly recommended to protect your github account with 2FA to protect us from your account being compromized.
    * SMS 2FA is not recommended
2. Download and install a git management tool.  
    * [Gitkraken](https://www.gitkraken.com) is recommended 
    * The rest of the guide assumes you are using Gitkraken.
3. Go to preferences==>SSH.  Generate a new private/public key.
4. Go to Github SSH settings and add your public key.
5. Open the Drauger OS Development repository you want to work on.
6. Click the fork button
7. Go to your repositories, you should now see your forked repository of the Drauger OS repository
8. Click on code ==> SSH and copy the URL provided
9. Go into Gitkraken and clone your forked repository using the SSH URL
10. When viewing your repository in Gitkraken, find the dev branch (remote) and have Gitkraken checkout.  You should be checked out to the current dev branch of your repository
    * While you are working, changes might be made to the Drauger OS repository you forked.  
    * If changes affect the files you are working on, you may need to rebase from your repository's page.  Be aware that your work may be lost, so backup your working files.
    * If you rebase, don't forget to pull from gitkraken.
11. Make the desired changes and commits.  
12. Push your commits to your repository as necessary
13. When you are finished making your changes, run through the pre-pull checklist
14. Go to the pull requests section of the Drauger OS repository and generate a pull request
    * Even if you have permissions to do so, don't approve pull requests you yourself generate

# Pre-pull checklist
- [ ] Run pylint
- [ ] Run unit tests
- [ ] Check type hinting
- [ ] Test the code (run the application)

# Pylint instructions
All Python code should conform to `PEP8` as closely as possible. If you open a pull request `pep8speaks` will provide feedback on your `PEP8` conformance.

A good rule of thumb is if your Python code gets a score of `7.5` or higher from `pylint`, and works correctly, the chances of having your pull request accepted is fairly high, but no pull request is guaranteed to be accepted.

If your code triggers pylint and you have a good reason for not complying to PEP8 standards, place a flag in your code to indicate you intentionally deviated from PEP8 standards.

```python
# pylint: disable=wrong-import-position
import widget
# pylint: enable=wrong-import-position
```

## How to set up and use Pylint

This assumes you have python3 and python3-pip installed

```bash
pip3 install pylint
python3 -m pylint testfile.py
```

Using "python3 -m" ensures the correct instance of pylint runs

# Unit test instructions
_more coming soon_

You can find a number of tests to make sure your programs work correctly in the `tests` directory. These are currently tailored to how these programs are written, i.e. they work Python scripts. None of the UI is tested yet. Feel free to write more tests and request their addition in a pull request.

If, after modifying a function, the unit test fails, fix the issue in the function.  Don't modify the unit test unless the functions interface has changed

# Type hinting instructions
_coming soon_

# Recommended coding practices
This section provides standards agreed upon by senior developers.  By following these guidelines, you reduce the likelihood the pull request will be returned.

* Your code should be self documenting (i.e. variable names, function names, etc.)
* Comment where necessary.  Assume someone else is going to read your code
* Docstrings will describe how others will interface with your function
    * other users should not need to read the code in your function to know how to use it
* Harden your function inputs
* Functions should have high functional cohesion -- doing one thing, and doing it well
* Functions should have loose coupling -- limited connections to other functions and high portability
* Minimize the scopes of variables
* Avoid duplicate code
* When able, prioritize code readability

