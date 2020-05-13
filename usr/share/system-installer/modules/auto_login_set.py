#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  auto_login_set.py
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
"""Set Autologin setting for the current user"""
from __future__ import print_function
from sys import stderr, argv
from os import remove

def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def auto_login_set(login, username):
    """Set Auto-Login Setting for the current user"""
    eprint("\t###\tauto_login_set.py started\t###\t")
    new_conf = ""
    with open("/etc/lightdm/lightdm.conf", "r") as conf:
        new_conf = conf.read()
    remove("/etc/lightdm/lightdm.conf")
    new_conf = new_conf.split('\n')
    for each in enumerate(new_conf):
        if each[0] == 0:
            continue
        new_conf[each[0]] = new_conf[each[0]].split('=')
    for each in enumerate(new_conf):
        if each[0] == 0:
            continue
        if new_conf[each[0]][0] == "autologin-user":
            if login in ("0", 0, False):
                del new_conf[each[0]]
            else:
                new_conf[each[0]][1] = username
            break
    for each in enumerate(new_conf):
        if each[0] == 0:
            continue
        new_conf[each[0]] = "=".join(new_conf[each[0]])
    with open("/etc/lightdm/lightdm.conf", "w+") as file:
        for each in new_conf:
            file.write(each)
            file.write('\n')
    eprint("\t###\tauto_login_set.py closed\t###\t")

if __name__ == '__main__':
    auto_login_set(argv[1], argv[2])
