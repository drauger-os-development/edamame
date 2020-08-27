#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  make_user.py
#
#  Copyright 2020 Thomas Castleman <contact@draugeros.org>
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
from os import path
from shutil import move, rmtree

import modules.set_wallpaper as set_wallpaper


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def __fix_home__(username):
    """Fix home path"""
    if path.exists("/home/home/live"):
        move("/home/home/live", "/home/" + username)
        try:
            rmtree("/home/home")
        except FileNotFoundError:
            pass
    else:
        eprint("An error occured setting home directory. Hopefully the user's own files are there?")


def make_user(username):
    """Set up the user's profile by modifying the Live user"""
    eprint("\t###\tmake_user.py STARTED\t###\t")
    if path.exists("/home/" + username):
        eprint("Original home folder found. Substituting it in . . .")
        rmtree("/home/live")
    elif path.exists("/home/home/live"):
        __fix_home__(username)
    else:
        eprint("Fixing refrences to old home . . .")
        with open("/home/live/.config/gtk-3.0/bookmarks", "r") as bookmark_file:
            bookmarks = bookmark_file.read().split("\n")
        for each in enumerate(bookmarks):
            bookmarks[each[0]] = bookmarks[each[0]].split("/home/live")
        for each in enumerate(bookmarks):
            bookmarks[each[0]] = ("/home/" + username).join(bookmarks[each[0]])
        with open("/home/live/.config/gtk-3.0/bookmarks", "w") as bookmark_file:
            bookmark_file.write("\n".join(bookmarks))
        try:
            move("/home/live", "/home/" + username)
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
    set_wallpaper.set_wallpaper(username)
    eprint("\t###\tmake_user.py CLOSED\t###\t")
