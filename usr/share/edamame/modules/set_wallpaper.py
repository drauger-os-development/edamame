#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  set_wallpaper.py
#
#  Copyright 2023 Thomas Castleman <batcastle@draugeros.org>
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
"""Set user wallpaper"""
from __future__ import print_function
from sys import stderr
from os import listdir, path
from subprocess import check_call, CalledProcessError
from shutil import move, copytree


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def set_wallpaper(username):
    """Set wallpaper. Wallpapers to set must be in /user-data"""
    eprint("    ###    set_wallpaper.py STARTED    ###    ")
    if not path.isdir("/user-data"):
        eprint("""/user-data does not exist.
Not using Advanced Quick Install's Wallpaper functionality.""")
        eprint("    ###    set_wallpaper.py CLOSED    ###    ")
        return
    ls = listdir("/user-data")
    screens = []
    for each in ls:
        if "wallpaper." in each:
            try:
                with open("/user-data/screens.list", "r") as data:
                    screens = data.read().split("\n")
            except FileNotFoundError:
                pass
            if "monitor0" not in screens:
                screens.append("monitor0")
            move("/user-data/" + each,
                 "/home/" + username + "/.config/" + each)
    if len(screens) == 0:
        for each in ls:
            copytree("/user-data/" + each,
                     "/home/" + username + "/.config/" + each)
        screens = ls
    for each in screens:
        if path.exists("/home/" + username + "/.config/" + each):
            file_name = each + "/" + listdir("/home/%s/.config/%s" % (username,
                                                                      each))[0]
        else:
            file_type = listdir("/home/" + username + "/.config")
            for each1 in file_type:
                if "wallpaper." in each1:
                    file_name = each1
                    break
        try:
            check_call(["xfconf-query", "-c", "xfce4-desktop", "-p",
                        "/backdrop/screen0/" + each + "/workspace0/last-image",
                        "-s", "/home/" + username + "/.config/" + file_name])
        except CalledProcessError:
            check_call(["xfconf-query", "-c", "xfce4-desktop", "--create",
                        "-p",
                        "/backdrop/screen0/" + each + "/workspace0/last-image",
                        "--type", "string", "-s",
                        "/home/" + username + "/.config/" + file_name])

    eprint("    ###    set_wallpaper.py CLOSED    ###    ")
