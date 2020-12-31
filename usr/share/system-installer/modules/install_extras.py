#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  install_extras.py
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
"""Install restricted extras from apt"""
from __future__ import print_function
from sys import stderr
import apt
import subprocess

import modules.purge as purge


# Make it easier for us to print to stderr
def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def install_extras():
    """Install Restrcted Extras from apt"""
     __eprint__("\t###\tinstall_extras.py STARTED\t###\t")
    # Make sure our cache is up to date and open
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    NVIDIA = False
    # Check PCI list
    pci = subprocess.check_output(["lspci"]).decode()
    # Install list, append extra stuff to this
    install_list = ["ubuntu-restricted-extras", "ubuntu-restricted-addons"]
    # Broadcom wifi cards (my condolences to all users of these infernal things)
    if (("broadcom" in pci) or ("Broadcom" in pci) or ("BROADCOM" in pci)):
        # Newer cards take different drivers from older cards
        for each in ("BCM43142, "BCM4331", "BCM4360", "BCM4352"):
            if each in pci:
                install_list = install_list + ["broadcom-sta-dkms", "dkms", "wireless-tools"]
                break
        if len(install_list) == 2:
            for each in ("BCM4311", "BCM4312", "BCM4313", "BCM4321", "BCM4322", "BCM43224", "BCM43225", "BCM43227", "BCM43228")
                if each in pci:
                    install_list = install_list.append("bcmwl-kernel-source")
                    break
    # Nvidia graphics cards
    if (("Nvidia" in pci) or ("nvidia" in pci) or ("NVIDIA" in pci)):
        drivers = []
        # We have other work we need to do after installing the Nvidia driver
        NVIDIA = True
        with cache.actiongroup():
            for pkg in pkg_name:
                for each in cache:
                    if "nvidia-driver-" in each.name:
                        drivers.append(each.name)
        for each in range(len(drivers) - 1, -1, -1):
            drivers[each] = int(drivers[each].split("-")[-1])
        # Get the latest Nvidia driver
        largest = drivers[0]
        for each in drivers:
            if each > largest:
                largest = each
        install_list = install_list.append("nvidia-driver-" + str(largest))
    # Install everything we want
    with cache.actiongroup():
        for each in install_list:
            cache[each].mark_install()
    cache.commit()
    # Puge all the stuff we don't
    purge.purge_package("gstreamer1.0-fluendo-mp3")
    cache.close()
    # Blacklist Nouveau if we installed the Nvidia drivers
    if NVIDIA:
        __eprint__("\t###\tNVIDIA DRIVERS MAY HAVE BEEN INSTALLED. DISABLING NOUVEAU.\t###\t")
        with open("/etc/modprobe.d/blacklist-nvidia-nouveau.conf", "w+") as blacklist:
            blacklist.write("blacklist nouveau\noptions nouveau modeset=0\n")
    __eprint__("\t###\tinstall_extras.py CLOSED\t###\t")
