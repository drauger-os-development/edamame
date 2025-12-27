#!shebang
# -*- coding: utf-8 -*-
#
#  install_updates.py
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
"""Install system updates from apt"""
from __future__ import print_function
from sys import stderr
import os
import apt
import subprocess as subproc

import modules.purge as purge


# Make it easier for us to print to stderr
def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def update_flatpak():
    """Update any installed Flatpaks

    We only do this for system-wide installations, in order to avoid possible issues.
    """
    subproc.check_call(["flatpak", "--system", "update", "-y"])


def cache_commit(cache):
    """Run apt.cache.commit(), with error handling"""
    try:
        cache.commit()
    except apt.cache.LockFailedException:
        try:
            os.mkdir("/var/cache")
        except FileExistsError:
            pass
        try:
            os.mkdir("/var/cache/apt")
        except FileExistsError:
            pass
        try:
            os.mkdir("/var/cache/apt/archives")
        except FileExistsError:
            pass
        with open("/var/cache/apt/archives/lock", "w+") as file:
            file.write("")
        os.chmod("/var/cache/apt/archives/lock", 0o640)
        os.chown("/var/cache/apt/archives/lock", 0, 0)
        cache.commit()


def update_system():
    """update system through package manager"""
    __eprint__("\t\t\t###    install_updates.py STARTED    ###    ")
    cache = apt.cache.Cache()
    try:
        cache.update()
    except apt.cache.FetchFailedException:
        subproc.check_call(["apt-get", "update"])
    cache.open()
    try:
        cache.upgrade()
        cache_commit(cache)
    except (apt.cache.FetchFailedException, apt.cache.LockFailedException, apt.apt_pkg.Error):
            try:
                subproc.check_call(["apt-get", "-o", 'Dpkg::Options::="--force-confold"', "--force-yes", "-y", "upgrade"])
            except subproc.CalledProcessError:
                print("ERROR: Possible held packages. Update may be partially completed.")
    purge.autoremove(cache)
    cache.close()
    update_flatpak()
    __eprint__("\t\t\t###    install_updates.py CLOSED    ###    ")
