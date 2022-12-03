#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_common.py
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
"""Test Common Library"""
import common
import random
import os
import string


def random_string(length=None):
    """Generate random string.

    If "length" is None, use a random length, 1-100.
    """
    # initializing size of string
    if not isinstance(length, (int, float)):
        N = random.randint(1,50)
    else:
        N = int(length)

    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))

    # return result
    return str(res)


def test_real_num(count=0):
    """Ensure we calculate real numbers correctly"""
    # set up
    test_numbers = []
    for each in range(10000):
        if random.choice([True, False]):
            # random float
            test_numbers.append(random.randint(-100000000,100000000) + random.random())
        else:
            # random int
            test_numbers.append(random.randint(-100000000,100000000))

    # run the test
    outputs = {}
    for each in test_numbers:
        outputs[each] = common.real_number(each)

    # evaluate results
    for each in outputs:
        if each <= 0:
            assert outputs[each] == 0
        else:
            assert isinstance(outputs[each], int)

    # test again, if necessary
    if count <= 200:
        count += 1
        test_real_num(count=count)


def test_recursive_mkdir():
    """Ensure recursive mkdir makes directories correctly and recurses
    correctly
    """
    for each in range(1000):
        # generate random path in current directory, 1000 times over
        path = []
        for each1 in range(random.randint(2, 40)):
            path.append(random_string())
        path2 = "/".join(path)

        # create random path
        common.recursive_mkdir(path2)

        # check if generated path exists
        test = ""
        for each in path:
            if test == "":
                test = each
            else:
                test = f"{ test }/{ each }"
            assert os.path.isdir(test)
        assert test == path2
        os.removedirs(path2)
