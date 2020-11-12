#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  check_kernel_version.py
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
"""Compare installed kernel and kernel in included archive to ensure they match
This is done to prevent a bug that drops the user to an initramfs shell since a
kernel cannot be booted.
"""
import tarfile as tar
import subprocess
import common


def __get_file_version__():
    """Get kernel version in included kernel archive"""
    try:
        tar_file = tar.open("/usr/share/system-installer/modules/kernel.tar.xz")
    except FileNotFoundError:
        tar_file = tar.open("/usr/share/system-installer/modules/kernel.tar.7z")
    files = tar_file.getnames()
    tar_file.close()
    for each in range(len(files) - 1, -1, -1):
        if files[each] in ("kernel", "kernel/linux-meta-xanmod"):
            del files[each]
            continue
        else:
            files[each] = files[each].split("/")[-1]
            files[each] = files[each].split("_")
            if files[each][0] == "linux-xanmod":
                del files[each]
            else:
                try:
                    files[each] = files[each][1]
                except IndexError:
                    del files[each]
    return common.unique(files)[0]


def __get_installed_version__():
    """Get kernel version using `uname'"""
    release = subprocess.check_output(["uname",
                                       "--release"]).decode("utf-8")[:-1]
    version = subprocess.check_output(["uname",
                                       "--kernel-version"]).decode("utf-8")[:-1]
    version = version.split(" ")[0]
    if version[0] == "#":
        version = version[1:]
    return "%s-%s" % (release, version)


def check_kernel_versions():
    """Compare kernel versions"""
    common.eprint("CHECKING KERNEL VERSIONS")
    file_version = __get_file_version__()
    installed_version = __get_installed_version__()
    if file_version == installed_version:
        common.eprint("KERNEL VERSIONS MATCH: SUCCESS")
        return True
    else:
        common.eprint("ERROR: KERNEL VERSION MISMATCH")
        common.eprint("FILE VERSION: %s" % (file_version))
        common.eprint("INSTALLED VERSION: %s" % (installed_version))
        common.eprint("USER LIKELY UPDATED system-installer TO A VERSION WITH NEWER KERNEL")
        common.eprint("PLEASE EITHER DOWNLOAD A NEW ISO, OR DO NOT UPDATE BEFORE INSTALLING")
        common.eprint("REBOOT, REFRAIN FROM UPDATING, AND ALL SHOULD BE WELL")
        return False
