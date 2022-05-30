#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  verify_install.py
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
"""Verify that installation completed correctly"""
from __future__ import print_function
from sys import stderr
from os import path, remove
from shutil import move
import subprocess
import apt

import modules.purge as purge


def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def add_boot_entry(root, distro):
    """Add the necessary boot entry"""
    if "nvme" in root:
        disk = root[:12]
        part = root[13:]
    else:
        disk = root[:8]
        part = root[8:]

    subprocess.check_call(["efibootmgr", "--create", "--disk", disk, "--part",
                           part, "--loader", "\EFI\systemd\systemd-bootx64.efi",
                           "--label", distro], stdout=stderr.buffer,
                          stderr=stderr.buffer)


def set_default_entry(distro):
    """Set default boot entry"""
    entries = subprocess.check_output(["efibootmgr"]).decode().split("\n")
    entries = [each.split(" ") for each in entries]
    del entries[0]
    del entries[0]
    del entries[-1]
    for each in enumerate(entries):
        entries[each[0]][1] = " ".join(entries[each[0]][1:])
        if len(entries[each[0]]) > 2:
            del entries[each[0]][2:]
        entries[each[0]][0] = entries[each[0]][0][4:-1]
    entries[0][1] = entries[0][1].split(",")
    code = ""
    for each in entries[1:]:
        if each[1] in ("UEFI OS", "Linux Boot Manager", distro):
            code = each[0]
            break
    del entries[0][1][entries[0][1].index(code)]
    entries[0][1].insert(0, code)
    order = ",".join(entries[0][1])
    # clean up a bit
    del entries, code
    subprocess.check_call(["efibootmgr", "-o", order])


def is_default_entry(distro):
    """Check if we are the default boot entry"""
    entries = subprocess.check_output(["efibootmgr"]).decode().split("\n")
    entries = [each.split(" ") for each in entries]
    del entries[0]
    del entries[0]
    del entries[-1]
    for each in enumerate(entries):
        entries[each[0]][1] = " ".join(entries[each[0]][1:])
        if len(entries[each[0]]) > 2:
            del entries[each[0]][2:]
        entries[each[0]][0] = entries[each[0]][0][4:-1]
    entries[0][1] = entries[0][1].split(",")
    code = entries[0][1][0]
    # we need to check if the entry is set as default
    for each in entries[1:]:
        if each[0] == code:
            if each[1] in ("UEFI OS", "Linux Boot Manager", distro):
                return True
    # we know it's not default. Check if it exists
    for each in entries[1:]:
        if (("UEFI OS" in each) or ("Linux Boot Manager" in each) or (distro in each)):
            return False
    # it is non-existant
    return None


def verify(username, root, distro):
    """Verify installation success"""
    __eprint__("    ###    verify_install.py STARTED    ###    ")
    if path.isdir("/home/home/live"):
        move("/home/home/live", "/home/" + username)
    try:
        remove("/home/" + username + "/Desktop/system-installer.desktop")
    except FileNotFoundError:
        pass
    if path.isdir("/sys/firmware/efi"):
        # on UEFI, set as default entry
        status = is_default_entry(distro)
        if status in (False, None):
            if status is None:
                add_boot_entry(root, distro)
                set_default_entry(disto)
    cache = apt.cache.Cache()
    cache.open()
    if username != "drauger-user":
        if (("system-installer" in cache) and cache["system-installer"].is_installed):
            cache["system-installer"].mark_delete()
        if path.isdir("/sys/firmware/efi"):
            with cache.actiongroup():
                for each in cache:
                    if (("grub" in each.name) and each.is_installed):
                        if "common" not in each.name:
                            each.mark_delete()
        cache.commit()
        purge.autoremove(cache)
    cache.close()
    __eprint__("    ###    verify_install.py CLOSED    ###    ")
