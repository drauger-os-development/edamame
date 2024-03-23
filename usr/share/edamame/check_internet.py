#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
#
#  check_internet.py
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
"""Ping servers to see if we have internet"""
import json
import dns.resolver as res
import common


def ping(mirror):
    """Try doing a DNS resolution on the mirrors"""
    # We need just the domain name, so we have to parse things down a bit
    if mirror[:4] == "http":
        mirror = mirror.split("/")[2]
    if mirror[-1] == "/":
        mirror = mirror[:-1]
    try:
        res.resolve(mirror, "A")
        return True
    except (res.NoNameservers, res.NoAnswer):
        return False
    except res.NXDOMAIN:
        return None


def has_internet():
    """Check for internet, using mirrors and ping counts defined in
    the default `edamame` config file."""
    # Read Mirrors file
    with open("/etc/edamame/settings.json", "r") as mirrors_file:
        mirrors = json.load(mirrors_file)

    mirrors = mirrors["ping servers"]

    # get only the unique mirrors
    mirrors = common.unique(mirrors)
    # Get our ping times
    results = []
    try:
        # Ping all listed servers, in case one or more is blocked
        for each in mirrors:
            results.append(ping(each))
    except:
        return False
    true = 0
    false = 0
    for each in results:
        if each:
            true += 1
        else:
            false += 1

    return (true > false)
