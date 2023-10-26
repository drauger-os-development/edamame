#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  auto_login_set.py
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
"""Set Autologin setting for the current user"""
from __future__ import print_function
from sys import stderr, argv
import os
import subprocess as sp

def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def auto_login_set(login, username):
    """Set Auto-Login Setting for the current user"""
    eprint("    ###    auto_login_set.py started    ###    ")
    new_conf = ""
    accepted = ("lightdm", "sddm")
    dm = determine_display_manager()
    if dm not in accepted:
        eprint("No supported DM found.")
        eprint(f"DM found: {dm}")
        return
    eprint(f"DM in use: {dm}")

    # specifics for different DMs
    if dm == accepted[0]:
        file = "/etc/lightdm/lightdm.conf"
        key = "autologin-user"
    elif dm == accepted[1]:
        if os.path.exists("/etc/sddm.conf.d/settings.conf"):
            file = "/etc/sddm.conf.d/settings.conf"
        elif os.path.exists("/etc/sddm.conf.d/kde_settings.conf"):
            file = "/etc/sddm.conf.d/kde_settings.conf"
        else:
            eprint("SDDM in use but settings file not found.")
            return
        key = "User"

    # Generic settings handler
    with open(file, "r") as conf:
        new_conf = conf.read()
    os.remove(file)
    new_conf = new_conf.split('\n')
    for each in enumerate(new_conf):
        if each[0] == 0:
            continue
        new_conf[each[0]] = new_conf[each[0]].split('=')
    applied = False
    for each in enumerate(new_conf):
        if each[0] == 0:
            continue
        if each[1][0] == key:
            if login in ("0", 0, False):
                eprint(f"DISABLING AUTO-LOGIN for USER {username}")
                del new_conf[each[0]]
            else:
                eprint(f"ENABLING AUTO-LOGIN for USER {username}")
                new_conf[each[0]][1] = username
                applied = True
            break
    for each in range(len(new_conf) - 1, -1, -1):
        if new_conf[each] == [""]:
            del new_conf[each]
    if (not applied) and (login in ("1", 1, True)):
        if dm == accepted[0]:
            new_conf.append([key, username])
        elif dm == accepted[1]:
            for each in enumerate(new_conf):
                if "Autologin" in each[1]:
                    new_conf.insert(each[0] + 1, [key, username])
                    break
    for each in enumerate(new_conf):
        if each[0] == 0:
            continue
        new_conf[each[0]] = "=".join(new_conf[each[0]])
    with open(file, "w+") as conf:
        for each in new_conf:
            conf.write(each)
            conf.write('\n')
    eprint("    ###    auto_login_set.py closed    ###    ")


def determine_display_manager():
    """Determine which display manager is in use"""
    # get known DMs
    recognized_dms = ("gdm3", "lightdm", "sddm", "lxdm", "nodm", "wdm", "xdm")
    dm_status = {}
    for each in recognized_dms:
        # get status of DMs
        dm_status[each] = sp.check_output(["systemctl", "show",
                                           "--no-pager",
                                           each]).decode().split("\n")
        for each1 in dm_status[each]:
            if "ActiveState" in each1:
                dm_status[each] = (each1.split("=")[1] == "active")
    # return active DMs
    for each in dm_status:
        if dm_status[each]:
            return each


if __name__ == '__main__':
    auto_login_set(argv[1], argv[2])
