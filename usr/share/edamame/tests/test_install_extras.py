#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_install_extras.py
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
"""Test Common Library"""
from modules import install_extras as ie


test_nvidia = [
        [("128B", "GeForce GT 710"), False],
        [("1B06", "GeForce GTX 1080 TI"), True],
        [("119A", "GeForce GTX 860M"), True],
        [("1008", "GeForce GTX 780 TI 6GB"), True],
        [("2203", "GeForce RTX 3090 TI"), True],
        [("2187", "GeForce GTX 1650 Super"), True],
        [("28A0", "GeForce RTX 4060 Max-Q / Mobile"), True],
        [("0041", "GeForce 6800"), False],
        [("2484", "GeForce RTX 3070"), True]
    ]

def test_determine_driver():
    """Test and make sure we always get a driver version for cards we are supposed to."""
    for each in test_nvidia:
        result = ie.determine_driver(each[0])
        print(each[0])
        if isinstance(result, str):
            assert result.isdecimal()
        elif isinstance(result, int):
            assert True
        else:
            assert result is None
        print(result)
        if result is None:
            assert (not each[1])
        else:
            assert each[1]
