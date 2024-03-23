#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
#
#  check_kernel_version.py
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
"""Compare installed kernel and kernel in included archive to ensure they match
This is done to prevent a bug that drops the user to an initramfs shell since a
kernel cannot be booted.
"""
import tarfile as tar
import subprocess
import os
import common


def __get_file_version__(local_repo, kernel_meta_pkg):
    """Get kernel version in included kernel archive"""
    if not os.path.exists(local_repo):
        try:
            tar_file = tar.open("/usr/share/edamame/kernel.tar.xz")
        except FileNotFoundError:
            tar_file = tar.open("/usr/share/edamame/kernel.tar.7z")
        files = tar_file.getnames()
        tar_file.close()
    else:
        files = os.listdir(local_repo)
    for each in range(len(files) - 1, -1, -1):
        if files[each] in ("kernel", "kernel/linux-meta"):
            del files[each]
            continue
        else:
            files[each] = files[each].split("/")[-1]
            files[each] = files[each].split("_")
            if files[each][0] == kernel_meta_pkg:
                del files[each][0]
            if files[each][-1] == "amd64.deb":
                del files[each][-1]
            files[each] = files[each][0]
    files = [each for each in files if "linux" in each]
    version = common.unique(files)[0]
    if version[:6] == "linux-":
        version = version[6:]
    if version[-2:] == "-0":
        version = version[:-2]
    if version[:8] == "headers-":
        version = version[8:]
    if version[:6] == "image-":
        version = version[6:]
    return version


def __get_installed_version__():
    """Get kernel version using `uname'"""
    return subprocess.check_output(["uname", "--release"]).decode("utf-8")[:-1]


def check_kernel_versions(local_repo, kernel_meta_pkg):
    """Compare kernel versions"""
    common.eprint("CHECKING KERNEL VERSIONS")
    file_version = __get_file_version__(local_repo, kernel_meta_pkg)
    installed_version = __get_installed_version__()
    if file_version == installed_version:
        common.eprint("KERNEL VERSIONS MATCH: SUCCESS")
        return True
    else:
        common.eprint("ERROR: KERNEL VERSION MISMATCH")
        common.eprint("FILE VERSION: %s" % (file_version))
        common.eprint("INSTALLED VERSION: %s" % (installed_version))
        common.eprint("USER LIKELY UPDATED EDAMAME TO A VERSION WITH NEWER KERNEL")
        common.eprint("PLEASE EITHER DOWNLOAD A NEW ISO, OR DO NOT UPDATE BEFORE INSTALLING")
        common.eprint("REBOOT, REFRAIN FROM UPDATING, AND ALL SHOULD BE WELL")
        return False
