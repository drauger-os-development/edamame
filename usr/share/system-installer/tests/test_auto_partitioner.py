#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_auto_partitioner.py
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
"""Tests for auto_partitioner"""
import auto_partitioner as ap
import os
import random
import json

def test_get_min_root_size_with_swap_part():
    """Make sure our math is correct to get the min root size, assuming no swap partition"""
    assert ap.get_min_root_size(swap=False) >= (ap.config["min root size"] * (1000 ** 2))
    assert ap.get_min_root_size(swap=False, bytes=False) >= ap.bytes_to_gb(ap.config["min root size"] * (1000 ** 2))


def test_get_min_root_size_without_swap_part():
    """make sure our root part is big enough to accommodate a swap file"""
    assert ap.get_min_root_size(ram_size=4, bytes=False) >= 29
    assert ap.get_min_root_size(ram_size=6, bytes=False) >= 31.449
    assert ap.get_min_root_size(ram_size=8, bytes=False) >= 33.828
    assert ap.get_min_root_size(ram_size=12, bytes=False) >= 38.464
    assert ap.get_min_root_size(ram_size=16, bytes=False) >= 43
    assert ap.get_min_root_size(ram_size=24, bytes=False) >= 51.8989
    assert ap.get_min_root_size(ram_size=64, bytes=False) >= 95


def test_is_EFI():
    """Check if the checks if a system is an EFI system are working"""
    assert os.path.isdir("/boot/efi") == ap.is_EFI()


def test_get_drive_path():
    """Ensure drive paths are always returned correctly"""
    # initial setup
    nvme = "/dev/nvme"
    mmcblk = "/dev/mmcblk"
    sata = "/dev/sd"
    ide = "/dev/hd"
    drive_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                     "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                     "w", "x", "y", "z"]
    nvme_list = {}
    mmcblk_list = {}
    sata_list = {}
    ide_list = {}
    # NVMe setup
    for each in range(random.randint(1, 45)):
        nvme_list[nvme + str(each)] = {}
    for each in nvme_list:
        total_drive_count = random.randint(1, 256)
        for current_drive_count in range(1, total_drive_count):
            nvme_list[each][each + "n" + str(current_drive_count)] = []
    """
    At this point, `nvme_list` should be set up like this:

    {
        "/dev/nvme1": {
            "/dev/nvme1n1": [],
            "/dev/nvme1n2": []
            },
        "/dev/nvme2": {
            "/dev/nvme2n1": [],
            "/dev/nvme2n2": []
            }
    }

    But we want this:

    {
        "/dev/nvme1": {
            "/dev/nvme1n1": [
                "/dev/nvme1n1p1",
                "/dev/nvme1n1p2",
                "/dev/nvme1n1p3"
                ],
            "/dev/nvme1n2": ["/dev/nvme1n2p1"]
            },
        "/dev/nvme2": {
            "/dev/nvme2n1": [
                "/dev/nvme2n1p1",
                "/dev/nvme2n1p2"
                ],
            "/dev/nvme2n2": [
                "/dev/nvme2n2p1",
                "/dev/nvme2n2p2",
                "/dev/nvme2n2p3",
                "/dev/nvme2n2p4"
                ]
            }
    }

    Just, larger.
    """
    for each in nvme_list:
        for each1 in nvme_list[each]:
            for part_count in range(1, random.randint(1, 256)):
                nvme_list[each][each1].append(each1 + "p" + str(part_count))
    # now we need to set up mmcblk, SATA, and IDE drive examples. Should be simple...
    # SATA set up
    for each in range(random.randint(1, len(drive_letters) - 1)):
        sata_list[sata + drive_letters[each]] = []
    for each in range(1, random.randint(1, 256)):
        for each1 in sata_list:
            sata_list[each1].append(each1 + str(each))
    # IDE set up
    for each in range(random.randint(1, len(drive_letters) - 1)):
        ide_list[ide + drive_letters[each]] = []
    for each in range(1, random.randint(1, 256)):
        for each1 in ide_list:
            ide_list[each1].append(each1 + str(each))
    # now just to setup for mmcblk
    for each in range(random.randint(1, 45)):
        mmcblk_list[mmcblk + str(each)] = []
    for each in mmcblk_list:
        total_drive_count = random.randint(1, 256)
        for current_drive_count in range(1, total_drive_count):
            mmcblk_list[each].append(each + "p" + str(current_drive_count))
    # check to make sure everything is valid
    # check mmcblk
    for each in mmcblk_list:
        for each1 in mmcblk_list[each]:
            assert each == ap.get_drive_path(each1)
        assert each == ap.get_drive_path(each)
    # check NVMe
    for each in nvme_list:
        # this, outter-most, loop needs no checks
        for each1 in nvme_list[each]:
            for each2 in nvme_list[each][each1]:
                assert each1 == ap.get_drive_path(each2)
            assert each1 == ap.get_drive_path(each1)
    # check SATA
    for each in sata_list:
        for each1 in sata_list[each]:
            assert each == ap.get_drive_path(each1)
        assert each == ap.get_drive_path(each)
    # check IDE
    for each in ide_list:
        for each1 in ide_list[each]:
            assert each == ap.get_drive_path(each1)
        assert each == ap.get_drive_path(each)
