#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  check_internet.py
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
"""Ping servers to see if we have internet"""
from subprocess import check_output, CalledProcessError
import json


def unique(starting_list):
    """Function to get a list down to only unique elements"""
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in starting_list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return(unique_list)


def ping(mirror, count):
    """Ping the mirrors"""
    # We need just the domain name, so we have to parse things down a bit
    mirror = mirror.split("/")[2]
    command = ["ping", "-c", count, "-q", mirror]
    print("PINGING %s" % (mirror))
    # get the ping times
    output = check_output(command).decode("utf-8").split("\n")[-2]
    return float(output.split("/")[-2])

def has_internet():
    """Check for internet, using mirrors and ping counts defined in
    the default `system-installer` config file."""
    # Read Mirrors file
    with open("/etc/system-installer/default.json", "r") as mirrors_file:
        mirrors = json.load(mirrors_file)

    ping_count = mirrors["ping count"]
    mirrors = mirrors["ping servers"]

    # get only the unique mirrors
    mirrors = unique(mirrors)
    # Get our ping times
    try:
        # Ping all listed servers, in case one or more is blocked
        for each in mirrors:
            ping(each, ping_count)

    except CalledProcessError:
        return False

    return True
