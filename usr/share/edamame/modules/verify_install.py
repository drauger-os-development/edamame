#!shebang
# -*- coding: utf-8 -*-
#
#  verify_install.py
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
"""Verify that installation completed correctly"""
from __future__ import print_function
from sys import stderr
import os
from shutil import move
import subprocess as subproc
import apt
import auto_partitioner
import common

from modules import purge


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

    subproc.check_call(["efibootmgr", "--create", "--disk", disk, "--part",
                           part, "--loader",
                           r"\EFI\systemd\systemd-bootx64.efi", "--label",
                           distro], stdout=stderr.buffer, stderr=stderr.buffer)


def set_default_entry(distro):
    """Set default boot entry"""
    entries = subproc.check_output(["efibootmgr"]).decode().split("\n")
    entries = [each.split(" ") for each in entries]
    for each in range(len(entries) - 1, -1, -1):
        if entries[each] == [""]:
            del entries[each]
            continue
        if entries[each][0][:4] == "Boot":
            if not entries[each][0][4].isnumeric():
                if entries[each][0][:9] != "BootOrder":
                    del entries[each]
        else:
            del entries[each]
    for each in enumerate(entries):
        entries[each[0]][1] = " ".join(entries[each[0]][1:]).split('\t')[0]
        if len(entries[each[0]]) > 2:
            del entries[each[0]][2:]
        entries[each[0]][0] = entries[each[0]][0][4:-1]
    entries[0][1] = entries[0][1].split(",")
    code = ""
    for each in entries[1:]:
        if each[1] in ("UEFI OS", "Linux Boot Manager", distro):
            code = each[0]
            break
    if code == "":
        __eprint__("\t\t\t### WARNING ###")
        __eprint__("SYSTEMD-BOOT DOES NOT APPEAR TO BE ADDED TO THE EFI BOOT ORDER.")
        #__eprint__(f"entries data structure: {entries}")
        #__eprint__(f"Boot entry code: {code}")
    del entries[0][1][entries[0][1].index(code)]
    entries[0][1].insert(0, code)
    order = ",".join(entries[0][1])
    # clean up a bit
    del entries, code
    subproc.check_call(["efibootmgr", "-o", order])


def is_default_entry(distro):
    """Check if we are the default boot entry"""
    entries = subproc.check_output(["efibootmgr"]).decode().split("\n")
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
    __eprint__("\t\t\t###    verify_install.py STARTED    ###    ")
    if os.path.isdir("/home/home/live"):
        move("/home/home/live", "/home/" + username)
    try:
        os.remove("/home/" + username + "/Desktop/edamame.desktop")
    except FileNotFoundError:
        try:
            os.remove("/home/" + username + "/Desktop/system-installer.desktop")
        except FileNotFoundError:
            pass
    if auto_partitioner.is_EFI():
        # on UEFI, set as default entry
        status = is_default_entry(distro)
        if status in (False, None):
            if status is None:
                add_boot_entry(root, distro)
                set_default_entry(distro)
    cache = apt.cache.Cache()
    cache.open()
    if username != "drauger-user":
        if "edamame" in cache:
            if cache["edamame"].is_installed:
                cache["edamame"].mark_delete()
        if auto_partitioner.is_EFI():
            with cache.actiongroup():
                for each in cache:
                    if (("grub" in each.name) and each.is_installed):
                        if "common" not in each.name:
                            each.mark_delete()
            versions = common.unique([each.split("-")[1] for each in os.listdir("/boot") if len(each.split("-")) > 1])
            for release in versions:
                __eprint__(f"Generating Initramfs for Kernel v{ release }")
                subproc.check_call(["mkinitramfs", "-o",
                                   f"/boot/initrd.img-{ release }",
                                   release])
            subproc.check_call(["update-systemd-boot"])
        cache.commit()
        purge.autoremove(cache)
    cache.close()
    __eprint__("\t\t\t###    verify_install.py CLOSED    ###    ")
