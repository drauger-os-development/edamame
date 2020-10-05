#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  install_updates.py
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
"""Install system updates from apt"""
from __future__ import print_function
from sys import stderr
import apt

import modules.purge as purge


# Make it easier for us to print to stderr
def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)

def update_system():
    """update system through package manager"""
    __eprint__("\t###\tinstall_updates.py STARTED\t###\t")
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    cache.upgrade(dist_upgrade=True)
    cache.commit()
    purge.autoremove(cache)
    cache.close()
    __eprint__("\t###\tinstall_updates.py CLOSED\t###\t")
