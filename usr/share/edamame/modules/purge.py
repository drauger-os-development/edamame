#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
#
#  purge.py
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
"""Make it easier to purge packages from the system"""
import apt


def purge_package(pkg_name):
    """Purge packages from system using apt

    arguments: pkg_name
                - Should be a list of package names to purge
                - Can also remove a single package (provided as a string),
                    but this is less efficient
    """
    if isinstance(pkg_name, str):
        pkg_name = [pkg_name]
    cache = apt.cache.Cache()
    cache.open()
    with cache.actiongroup():
        for pkg in pkg_name:
            for each in cache:
                if pkg == each.name:
                    each.mark_delete()
    cache.commit()
    cache.close()


def autoremove(cache):
    """Auto-remove emulation using apt Python library"""
    # the autoremove function does not exist. So, emulate it
    cache.open()
    with cache.actiongroup():
        for each in cache:
            if each.is_auto_removable:
                each.mark_delete()
    cache.commit()
