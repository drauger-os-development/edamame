#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  chroot.py
#
#  Copyright 2023 Thomas Castleman <batcastle@draugeros.org>
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
"""Provide similar functionality to arch-chroot, in Python"""
from os import chroot, fchdir, O_RDONLY, chdir, path, close
from os import open as get
from subprocess import check_call, CalledProcessError


def __mount__(device, path_dir, fstype="", options=""):
    """Mount necessary psudeo-filesystems"""
    if device == "/run":
        try:
            check_call(["mount", device, path_dir, "--bind"])
        except CalledProcessError:
            pass
    else:
        try:
            check_call(["mount", device, path_dir, "-t",
                        fstype, "-o", options])
        except CalledProcessError:
            pass


def __unmount__(path_dir):
    """unmount psudeo-filesystems"""
    try:
        check_call(["umount", path_dir])
    except CalledProcessError:
        pass


def arch_chroot(path_dir):
    """replicate arch-chroot functionality in Python"""
    real_root = get("/", O_RDONLY)
    if path_dir[len(path_dir) - 1] == "/":
        path_dir = path_dir[0:len(path_dir) - 2]
    __mount__("proc", path_dir + "/proc", "proc", "nosuid,noexec,nodev")
    __mount__("sys", path_dir + "/sys", "sysfs", "nosuid,noexec,nodev,ro")
    if path.exists(path_dir + "/sys/firmware/efi/efivars"):
        __mount__("efivars", path_dir + "/sys/firmware/efi/efivars",
                  "efivarfs", "nosuid,noexec,nodev")
    __mount__("udev", path_dir + "/dev", "devtmpfs", "mode=0755,nosuid")
    __mount__("devpts", path_dir + "/dev/pts",
              "devpts", "mode=0620,gid=5,nosuid,noexec")
    __mount__("shm", path_dir + "/dev/shm", "tmpfs", "nosuid,noexec,nodev")
    __mount__("/run", path_dir + "/run")
    __mount__("tmp", path_dir + "/tmp", "tmpfs",
              "mode=1777,strictatime,nodev,nosuid")
    chdir(path_dir)
    chroot(path_dir)
    return real_root


def de_chroot(real_root, path_dir):
    """exit chroot from arch_chroot()

real_root should be the return value from arch_chroot()
path_dir should be the directory we initially chrooted into
"""
    __unmount__(path_dir + "/proc")
    __unmount__(path_dir + "/sys")
    if path.exists(path_dir + "/sys/firmware/efi/efivars"):
        __unmount__(path_dir + "/sys/firmware/efi/efivars")
    __unmount__(path_dir + "/dev")
    __unmount__(path_dir + "/dev/pts")
    __unmount__(path_dir + "/dev/shm")
    __unmount__(path_dir + "/run")
    __unmount__(path_dir + "/tmp")
    fchdir(real_root)
    chroot(".")
    close(real_root)
