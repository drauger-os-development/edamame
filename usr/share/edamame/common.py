#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
#
#  common.py
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
"""Common functions and other data for edamame"""
import sys
import os


def unique(starting_list):
    """Function to get a list down to only unique elements"""
    # initialize a null list
    # unique_list = []
    # traverse for all elements
    # for each in starting_list:
        # check if exists in unique_list or not
        # if each not in unique_list:
            # unique_list.append(each)
    # return unique_list
    return list(set(starting_list))


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


def real_number(num):
    """Take an int or float and return an int that is 0 or higher

    This DOES NOT return absolute value. Any negative numbers will return 0.
    Passing in anything other than an int or float will raise a TypeError
    Valid floats that are passed are truncated, not rounded.
    """
    if not isinstance(num, (int, float)):
        raise TypeError("Not a valid int or float")
    if num >= 0:
        return int(num)
    return 0


def recursive_mkdir(path):
    """ Recursively make directories down a file path

    This function is functionally equivallent to: `mkdir -p {path}'
    """
    path = path.split("/")
    for each in enumerate(path):
        dir = "/".join(path[:each[0] + 1])
        # prevent calling mkdir() on an empty string
        if dir != "":
            try:
                os.mkdir(dir)
            except FileExistsError:
                pass

def item_in_list(item, array):
    """Check if an item is in a list. This is supposed to be faster than:

    'item' in 'array'

    This only speeds things up in situations with more than about 10 items in a list
    """
    new_arr = set(array)
    for each in array:
        if item == each:
            return True
    return False
