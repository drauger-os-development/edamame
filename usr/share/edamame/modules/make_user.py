#!shebang
# -*- coding: utf-8 -*-
#
#  make_user.py
#
#  Copyright 2025 Thomas Castleman <batcastle@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""Make user profile"""
from __future__ import print_function
from sys import stderr
import os
from shutil import move, rmtree
import subprocess

import modules.set_wallpaper as set_wallpaper


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def __fix_home__(username):
    """Fix home path"""
    if os.path.exists("/home/home/live"):
        move("/home/home/live", "/home/" + username)
        try:
            rmtree("/home/home")
        except FileNotFoundError:
            pass
    else:
        eprint("An error occured setting home directory. Hopefully the user's own files are there?")


def make_user(username):
    """Set up the user's profile by modifying the Live user

    This function is also responsible for setting up a user's home directory
    as well as their groups.
    """
    eprint("\t\t\t###    make_user.py STARTED    ###    ")
    new_home = "/home/" + username
    if os.path.exists(new_home):
        eprint("Original home folder found. Substituting it in . . .")
        try:
            rmtree("/home/live")
        except FileNotFoundError:
            # literally a 1 in a trillion chance of happening, but just in case
            if username != "home":
                rmtree("/home/home")
    elif os.path.exists("/home/home/live"):
        __fix_home__(username)
    else:
        eprint("Fixing refrences to old home . . .")
        try:
            with open("/home/live/.config/gtk-3.0/bookmarks", "r") as bookmark_file:
                bookmarks = bookmark_file.read().split("\n")
            for each in enumerate(bookmarks):
                bookmarks[each[0]] = bookmarks[each[0]].split("/home/live")
            for each in enumerate(bookmarks):
                bookmarks[each[0]] = (new_home).join(bookmarks[each[0]])
            with open("/home/live/.config/gtk-3.0/bookmarks", "w") as bookmark_file:
                bookmark_file.write("\n".join(bookmarks))
        except FileNotFoundError:
            eprint("gtk-3.0/bookmarks not found. Moving on...")
        try:
            move("/home/live", new_home)
        except FileNotFoundError:
            __fix_home__(username)
    with open("/etc/passwd", "r") as passwd_file:
        passwd = passwd_file.read().split("\n")
    for each in enumerate(passwd):
        passwd[each[0]] = passwd[each[0]].split("live")
    for each in enumerate(passwd):
        passwd[each[0]] = username.join(passwd[each[0]])
    with open("/etc/passwd", "w") as passwd_file:
        passwd_file.write("\n".join(passwd))
    # Make sure groups are okay
    default_groups = ["adm", "sudo", "cdrom", "audio",
                      "dip", "plugdev"]
    subprocess.check_output(["groupmod", "--new-name", username, "live"])
    subprocess.check_output(["usermod", "-G", ",".join(default_groups),
                             "-a", username])
    # Home directory has correct perms
    for root, dirs, files, in os.walk(new_home):
        for dev in dirs:
            try:
                os.chown(os.path.join(root, dev), 1000, 1000)
            except FileNotFoundError:
                pass
        for dev in files:
            try:
                os.chown(os.path.join(root, dev), 1000, 1000)
            except FileNotFoundError:
                pass
    os.chown(new_home, 1000, 1000)
    os.chmod(new_home, 0o755)
    set_wallpaper.set_wallpaper(username)
    eprint("\t\t\t###    make_user.py CLOSED    ###    ")
