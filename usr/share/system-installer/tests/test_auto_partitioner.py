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
