#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  set_wallpaper.py
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
from __future__ import print_function
from sys import argv, stderr, version_info
from os import listdir
from subprocess import check_call
from shutil import move

# Make it easier for us to print to stderr
def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


def set_wallpaper(username):
    eprint("\t###\tset_wallpaper.py STARTED\t###\t")
    ls = listdir()
    for each in ls:
        if (("wallpaper" in each) and ("set_wallpaper.py" != each)):
            move(each, "/home/" + username + "/.config/" + each)
            check_call(["xfconf-query", "-c", "xfce4-desktop", "-p",
                        "/backdrop/screen0/monitor0/workspace0/last-image",
                        "-s", "/home/" + username + "/.config/" + each])
            break
    eprint("\t###\tset_wallpaper.py CLOSED\t###\t")



