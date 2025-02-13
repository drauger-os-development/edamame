#!shebang
# -*- coding: utf-8 -*-
#
#  install_extras.py
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
"""Install restricted extras from apt"""
from __future__ import print_function
from sys import stderr
import apt
import subprocess as subproc
import os
import json
import gzip

import modules.purge as purge


# Make it easier for us to print to stderr
def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def check_compat(version_number: int, card: tuple) -> bool:
    """Download driver meta package"""
    try:
        subproc.check_call(["apt-get", "download", f"nvidia-driver-{version_number}"])
    except subproc.CalledProcessError:
        # We likely lost internet. Return False since we don't know for sure.
        return False

    # Extract Data
    files = os.listdir()
    deb_file = None
    for each in files:
        if f"nvidia-driver-{version_number}" in each:
            if ".deb" == each[-4:]:
                deb_file = each
                break
    # File has gone missing. Return False.
    if deb_file == None:
        return False
    test_folder = f"test-nvidia-driver-{version_number}"
    os.mkdir(test_folder)
    try:
        subproc.check_call(["dpkg", "--extract", deb_file, test_folder])
    except subproc.CalledProcessError:
        # Something is corrupt with the deb package. Return False.
        return False

    # Open and read the ReadMe file
    needed_file = f"{test_folder}/usr/share/doc/nvidia-driver-{version_number}/README.txt.gz"
    with gzip.open(needed_file, "rt") as file:
        contents = file.read().split("\n")

    # Parse Readme
    passed_toc = False
    key = "Appendix A. Supported NVIDIA GPU Products"
    line_num = 0
    for each in contents:
        if each == key:
            if passed_toc:
                line_num += 1
                contents = contents[line_num:]
                break
            else:
                passed_toc = True
        line_num += 1
    key = "A1. CURRENT NVIDIA GPUS"
    line_num = 0
    for each in contents:
        if each == key:
            if passed_toc:
                line_num += 1
                contents = contents[line_num:]
                break
            else:
                passed_toc = True
        line_num += 1
    contents = contents[4:]
    line_num = 0
    for each in contents:
        if each == "":
            break
        line_num += 1
    contents = contents[:line_num]
    for each in enumerate(contents):
        contents[each[0]] = each[1].split("  ")
        contents[each[0]] = [each1 for each1 in contents[each[0]] if each1 != ""]
        contents[each[0]][0] = contents[each[0]][0][1:]
        contents[each[0]][1] = contents[each[0]][1][:4]
        if contents[each[0]][0][:7].lower() == "nvidia ":
            contents[each[0]][0] = contents[each[0]][0][7:]

    # check for support
    supported = False
    for each in contents:
        if each[0].lower() == card[1].lower():
            if each[1].lower() == card[0].lower():
                supported = True

    # Clean up
    os.remove(deb_file)
    subproc.check_call(["rm", "-rf", test_folder]) # This is easier than calling whatever the Pythonic way of removing folders recursively is.

    return supported


def determine_driver(card: tuple) -> int:
    """Determine which Nvidia driver is needed for a given card."""
    # Get Nvidia drivers available in apt
    packages = subproc.check_output(["apt-cache", "search", "^nvidia-driver-"]).decode()
    packages = packages.split("\n")

    # Filter the packages
    for each in range(len(packages) - 1, -1, -1):
        if "nvidia-driver-" != packages[each][:14]:
            del packages[each]
        elif "open" in packages[each].split(" - ")[0]:
            del packages[each]
        elif "server" in packages[each].split(" - ")[0]:
            del packages[each]
        elif "core" in packages[each].split(" - ")[0]:
            del packages[each]
        elif "lrm" in packages[each].split(" - ")[0]:
            del packages[each]
        elif "transitional" in packages[each].lower():
            del packages[each]
        else:
            packages[each] = packages[each].split(" - ")[0]
    del packages[packages.index("nvidia-driver-latest")]

    # Parse package names
    packages = [int(each.split("-")[-1]) for each in packages]
    packages.sort(reverse=True)

    # Check for compatability
    for each in packages:
        if check_compat(each, card):
            return each
    # Nothing is compatable. Return None.
    return None


def detect_nvidia() -> tuple:
    """Detect what NVIDIA card is in use"""
    try:
        pci = subproc.check_output("lspci -qnnmm | grep -i 'nvidia' | grep -E 'VGA|3D'", shell=True).decode().split('\n')
    except subproc.CalledProcessError:
        return None
    pci = pci[0]
    pci = pci.split('" "')[2]
    card_name = pci[list(pci).index('[') + 1:list(pci).index(']')]
    pci = pci.split(f"[{card_name}] ")[1]
    pci = pci[list(pci).index('[') + 1:list(pci).index(']')]
    if "Rev." in card_name:
        index = card_name.split().index("Rev.")
        card_name = " ".join(card_name.split()[:index])
    return (pci, card_name)


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
        # Figure our what driver we need
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
