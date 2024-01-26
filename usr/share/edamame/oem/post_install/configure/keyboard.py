#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  keyboard.py
#
#  Copyright 2024 Thomas Castleman <batcastle@draugeros.org>
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
"""Configure a user's keyboard"""
import subprocess
import os
from sys import stderr


def configure(MODEL, LAYOUT, VARIENT):
    """Configure a user's keyboard"""
    if MODEL != "OEM":
        with open("/usr/share/X11/xkb/rules/base.lst", "r") as xkb_conf:
            kcd = xkb_conf.read()
        kcd = kcd.split("\n")
        for each1 in enumerate(kcd):
            kcd[each1[0]] = kcd[each1[0]].split()
        try:
            os.remove("/etc/default/keyboard")
        except FileNotFoundError:
            pass
        xkbm = ""
        xkbl = ""
        xkbv = ""
        for each1 in kcd:
            if " ".join(each1[1:]) == MODEL:
                xkbm = each1[0]
            elif " ".join(each1[1:]) == LAYOUT:
                xkbl = each1[0]
            elif " ".join(each1[1:]) == VARIENT:
                xkbv = each1[0]
        with open("/etc/default/keyboard", "w+") as xkb_default:
            xkb_default.write("""XKBMODEL=\"%s\"
XKBLAYOUT=\"%s\"
XKBVARIANT=\"%s\"
XKBOPTIONS=\"\"

BACKSPACE=\"guess\"
""" % (xkbm, xkbl, xkbv))
        subprocess.Popen(["udevadm", "trigger", "--subsystem-match=input",
                          "--action=change"], stdout=stderr.buffer)
