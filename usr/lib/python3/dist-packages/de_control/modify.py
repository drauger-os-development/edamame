#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  modify.py
#
#  Copyright 2022 Thomas Castleman <contact@draugeros.org>
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
"""Modify DE/WM settings and configuration"""
import sys
import os


def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


def for_desktop(username):
    """Make modifications to the DE/WM to optimize for the DESKTOP
    experience.
    """
    __eprint__("DESKTOP DETECTED. EDITING PANEL ACCORDINGLY.")
    try:
        os.remove("/home/" + username + "/.config/xfce4/panel/battery-12.rc")
    except FileNotFoundError:
        pass
    with open("/home/" + username + "/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml", "r") as file:
        xml = file.read().split("\n")
    for each in range(len(xml) - 1, -1, -1):
        if "battery" in xml[each]:
            del xml[each]
    xml = "\n".join(xml)
    with open("/home/" + username + "/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml", "w") as file:
        file.write(xml)


def for_laptop():
    """make modifications to the DE/WM to optimize for the LAPTOP
    experience.
    """
    pass
