#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  install_extras.py
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
    __eprint__("    ###    install_extras.py STARTED    ###    ")
    # Make sure our cache is up to date and open
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    NVIDIA = False
    # Check PCI list
    pci = subprocess.check_output(["lspci", "-q"]).decode()
    # Install list, append extra stuff to this
    install_list = ["ubuntu-restricted-extras", "ubuntu-restricted-addons"]
    # Broadcom wifi cards (my condolences to all users of these infernal things)
    if "broadcom" in pci.lower():
        # Newer cards take different drivers from older cards
        for each in ("BCM43142", "BCM4331", "BCM4360", "BCM4352"):
            if each in pci:
                install_list = install_list + ["broadcom-sta-dkms", "dkms",
                                               "wireless-tools"]
                break
        if len(install_list) == 2:
            for each in ("BCM4311", "BCM4312", "BCM4313", "BCM4321", "BCM4322",
                         "BCM43224", "BCM43225", "BCM43227", "BCM43228"):
                if each in pci:
                    install_list.append("bcmwl-kernel-source")
                    break
    # Nvidia graphics cards
    if "nvidia" in pci.lower():
        # this isn't the ideal thing to do. Logic will be added later to handle
        # installing drivers and `disable-nouveau` for older cards.
        install_list.append("nvidia-driver-latest")
    # Install everything we want
    with cache.actiongroup():
        for each in install_list:
            cache[each].mark_install()
    cache.commit()
    # Purge all the stuff we don't want
    purge.purge_package("gstreamer1.0-fluendo-mp3")
    cache.close()
    __eprint__("    ###    install_extras.py CLOSED    ###    ")
