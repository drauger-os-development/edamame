#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  install_extras.py
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
"""Install restricted extras from apt"""
from __future__ import print_function
from sys import stderr
import apt
import subprocess as subproc
import urllib3
import os
import json

import modules.purge as purge


# Make it easier for us to print to stderr
def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def http_get(url):
    """Preform HTTP GET request"""
    http = urllib3.PoolManager()
    data = http.request("GET", url).data.decode()
    return data


def determine_driver(card):
    """Determine which Nvidia driver is needed for a given card."""
    # Get Nvidia driver archive page
    data = http_get("https://www.nvidia.com/en-us/drivers/unix/")
    # Parse the page
    data = data.split('\n')
    for each in data:
        if "Linux x86_64/AMD64" in each:
            linux_drivers = each.split("<br>")[1:-1]
            break
    drivers = {}
    """
    Associate each driver with it's download page link
    We do this because the download page has the information on it as to which cards each driver supports
    """
    for each in linux_drivers:
        partial_parse = each.split("href=\"")[1].split('"')
        driver_code = partial_parse[1][1:].split(".")[0].strip()
        link = partial_parse[0].strip()
        if driver_code not in drivers.keys():
            drivers[driver_code] = link
    # Search driver download page for mentions of card installed
    options = []
    for each in drivers:
        data = http_get(drivers[each])
        if card in data:
            options.append(int(each))
    # sort all options and return the one with the largest version code
    # This code is going to be the most recent driver
    options.sort()
    return options[-1]

def detect_nvidia():
    """Detect what NVIDIA card is in use"""
    try:
        pci = subproc.check_output("lspci -qmm | grep -i 'nvidia' | grep -E 'VGA|3D'", shell=True).decode().split('\n')
    except subproc.CalledProcessError:
        return None
    pci = pci[0]
    pci = pci[list(pci).index('[') + 1:list(pci).index(']')]
    if "Rev." in pci:
        index = pci.split().index("Rev.")
        pci = " ".join(pci.split()[:index])
    return pci


def detect_realtek():
    """Detect what Realtek card is in use"""
    try:
        pci = subproc.check_output("lspci -qmm | grep -i 'realtek'", shell=True).decode().split('\n')[0]
    except subproc.CalledProcessError:
        return None
    toggle = False
    start = 0
    count = 2
    device = None
    for each in enumerate(pci):
        if (not toggle) and (each[1] == '"'):
            toggle = True
            start = each[0]
        elif (toggle) and (each[1] == '"'):
            toggle = False
            if count == 0:
               device = pci[start + 1:each[0]].split(" ")[0].lower()
               break
            else:
                count -= 1
    return device


def install_extras():
    """Install Restrcted Extras from apt"""
    __eprint__("\t\t\t###    install_extras.py STARTED    ###    ")
    # Make sure our cache is up to date and open
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    NVIDIA = False
    # Check PCI list
    pci = subproc.check_output(["lspci", "-q"]).decode()
    # Install list, append extra stuff to this
    standard_install_list = ["ubuntu-restricted-extras", "ubuntu-restricted-addons"]
    additional_install_list = []
    # Broadcom wifi cards (my condolences to all users of these infernal things)
    if "broadcom" in pci.lower():
        # Newer cards take different drivers from older cards
        for each in ("BCM43142", "BCM4331", "BCM4360", "BCM4352"):
            if each in pci:
                additional_install_list = additional_install_list + ["broadcom-sta-dkms", "dkms",
                                               "wireless-tools"]
                break
        if len(additional_install_list) == 2:
            for each in ("BCM4311", "BCM4312", "BCM4313", "BCM4321", "BCM4322",
                         "BCM43224", "BCM43225", "BCM43227", "BCM43228"):
                if each in pci:
                    additional_install_list.append("bcmwl-kernel-source")
                    break
    # Realtek cards. Not as bad as Broadcom, but still suck
    if "realtek" in pci.lower():
        with open("/etc/edamame/realtek.json", "r") as file:
            drivers = json.load(file)
        device = detect_realtek()
        try:
            driver = drivers[device]
            additional_install_list.append(driver)
        except KeyError:
            __eprint__("\t\t\t### WARNING ###")
            __eprint__(f"NO REALTEK DRIVER FOUND FOR DEVICE: {device}")
            __eprint__("IT IS LIKELY THAT ANY DRIVERS NEEDED ARE BUILT INTO THE KERNEL.")
    # Nvidia graphics cards
    if "nvidia" in pci.lower():
        needed_driver = determine_driver(detect_nvidia())
        latest_deps_raw = subproc.check_output(["apt-cache", "depends", "nvidia-driver-latest"]).decode().split('\n')[1:]
        latest_deps = [each.split(": ")[1] for each in latest_deps_raw]
        for each in latest_deps:
            if "nvidia-driver" in each:
                nvidia_driver = int(each.split("-")[-1])
                break
        if needed_driver < nvidia_driver:
            if f"nvidia-driver-{needed_driver}" in cache:
                additional_install_list.append(f"nvidia-driver-{needed_driver}")
                additional_install_list.append("disable-nouveau")
            else:
                __eprint__("\t\t\t### WARNING ###")
                __eprint__(f"NO NVIDIA DRIVER FOUND MATCHING MAJOR VERSION CODE: {needed_driver}")
                __eprint__("IT IS LIKELY THAT ANY AVAILABLE DRIVERS THAT __MIGHT__ WORK ARE TOO HEAVY FOR YOUR SYSTEM.")
                __eprint__("WE __STRONGLY__ SUGGEST THAT YOU REMAIN USING THE OPEN-SOURCE NOUVEAU DRIVERS.")
        else:
            additional_install_list.append("nvidia-driver-latest")
    # Install everything we want
    os.environ["DEBIAN_FRONTEND"] = "noninteractive"
    try:
        with cache.actiongroup():
            for each in standard_install_list:
                cache[each].mark_install()
        cache.commit()
    except apt.cache.FetchFailedException:
        __eprint__("\t\t\t### WARNING ###")
        __eprint__("INSTALLATION OF STANDARD RESTRICTED EXTRAS FAILED. CONTINUING TO DRIVERS...")
     try:
        with cache.actiongroup():
            for each in additional_install_list:
                cache[each].mark_install()
        cache.commit()
    except apt.cache.FetchFailedException:
        __eprint__("\t\t\t### WARNING ###")
        __eprint__("INSTALLATION OF DRIVERS FAILED.")
    # Purge all the stuff we don't want

    purge.purge_package("gstreamer1.0-fluendo-mp3")
    cache.close()
    __eprint__("    ###    install_extras.py CLOSED    ###    ")
