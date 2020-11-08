#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  installer.py
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
"""Main module controling the installation process"""
from __future__ import print_function
from subprocess import Popen, check_output, check_call, CalledProcessError
from os import mkdir, path, chdir, listdir, remove, symlink, chmod
from shutil import rmtree, move, copyfile, copytree
import tarfile as tar
import json
import UI
import modules
import chroot
import common
import auto_partitioner


def __mount__(device, path_dir):
    """Mount device at path
    It would be much lighter weight to use ctypes to do this
    But, that keeps throwing an 'Invalid Argument' error.
    Calling Mount with check_call is the safer option.
    """
    try:
        check_call(["mount", device, path_dir])
    except CalledProcessError:
        pass


def __update__(percentage):
    """Update progress percentage file"""
    try:
        with open("/tmp/system-installer-progress.log", "w+") as progress:
            progress.write(str(percentage))
    except PermissionError:
        chmod("/tmp/system-installer-progress.log", 0o666)
        with open("/tmp/system-installer-progress.log", "w+") as progress:
            progress.write(str(percentage))


def install(settings):
    """Begin installation proceidure

    settings should be a dictionary with the following values:
        AUTO_PART : bool
        ROOT : device path as str
        HOME : device path as str
        EFI : device path
        SWAP : device path or 'FILE'
        LANG : language as str
        TIME_ZONE : 'Region/SubRegion' as str
        USERNAME : str
        PASSWORD : str
        EXTRAS : bool
        UPDATES : bool
        LOGIN : bool
        MODEL : keyboard model as str
        LAYOUT : keyboard layout as str
        VARIENT : keyboard varient as str

    You can read in /etc/system-installer/quick-install-template.json with
    json.loads()["DATA"] to see an example of acceptable settings
    """
    common.eprint("\t###\tinstaller.py STARTED\t###\t")
    work_dir = "/tmp/quick-install_working-dir"
    # STEP 1: Partion and format the drive ( if needed )
    if settings["AUTO_PART"]:
        partitioning = auto_partitioner.partition(settings["ROOT"],
                                                  settings["EFI"],
                                                  settings["HOME"])
        settings["ROOT"] = partitioning["ROOT"]
        settings["EFI"] = partitioning["EFI"]
        settings["HOME"] = partitioning["HOME"]
    if path.exists("/tmp/system-installer-progress.log"):
        remove("/tmp/system-installer-progress.log")
    __update__(12)
    # STEP 2: Mount the new partitions
    __mount__(settings["ROOT"], "/mnt")
    if settings["EFI"] not in ("NULL", None, ""):
        try:
            mkdir("/mnt/boot")
        except FileExistsError:
            pass
        try:
            mkdir("/mnt/boot/efi")
        except FileExistsError:
            pass
        __mount__(settings["EFI"], "/mnt/boot/efi")
    if settings["HOME"] not in ("NULL", None, ""):
        try:
            mkdir("/mnt/home")
        except FileExistsError:
            common.eprint("/mnt/home exists when it shouldn't. We have issues...")
        __mount__(settings["HOME"], "/mnt/home")
    if settings["SWAP"] != "FILE":
        # This can happen in the background. No biggie.
        Popen(["swapon", settings["SWAP"]])
    else:
        common.eprint("SWAPFILE NOT CREATED YET")
    __update__(14)
    # STEP 3: Unsquash the sqaushfs and get the files where they need to go
    squashfs = ""
    with open("/etc/system-installer/default.json", "r") as config:
        squashfs = json.loads(config.read())["squashfs_Location"]
    if not path.exists(squashfs):
        common.eprint("\n\tSQUASHFS FILE DOES NOT EXIST\t\n")
        UI.error.show_error("\n\tSQUASHFS FILE DOES NOT EXIST\t\n")
    __update__(17)
    chdir("/mnt")
    common.eprint("CLEANING INSTALLATION DIRECTORY")
    death_row = listdir()
    for each in death_row:
        if each not in ("boot", "home"):
            common.eprint("Removing " + each)
            try:
                rmtree(each)
            except NotADirectoryError:
                remove(each)
    chdir("/mnt/boot")
    death_row = listdir()
    for each in death_row:
        if each != "efi":
            try:
                rmtree(each)
            except NotADirectoryError:
                remove(each)
    chdir("/mnt")
    common.eprint("\t###\tEXTRACTING SQUASHFS\t###\t")
    check_call(["unsquashfs", squashfs])
    common.eprint("\t###\tEXTRACTION COMPLETE\t###\t")
    file_list = listdir("/mnt/squashfs-root")
    for each in file_list:
        try:
            common.eprint("/mnt/squashfs-root/" + each + " --> /mnt/" + each)
            move("/mnt/squashfs-root/" + each, "/mnt/" + each)
        except FileExistsError as e:
            common.eprint("ERROR: %s" % (e))
    rmtree("/mnt/squashfs-root")
    try:
        mkdir("/mnt/boot")
    except FileExistsError:
        common.eprint("/mnt/boot already created")
    file_list = listdir("/boot")
    for each in file_list:
        try:
            common.eprint("/boot/" + each + " --> /mnt/boot/" + each)
            copyfile("/boot/" + each, "/mnt/boot/" + each)
        except IsADirectoryError:
            copytree("/boot/" + each, "/mnt/boot/" + each)
    copyfile("/tmp/system-installer-progress.log",
             "/mnt/tmp/system-installer-progress.log")
    remove("/tmp/system-installer-progress.log")
    symlink("/mnt/tmp/system-installer-progress.log",
            "/tmp/system-installer-progress.log")
    __update__(32)
    # STEP 4: Update fstab
    common.eprint("\t###\tUpdating FSTAB\t###\t")
    remove("/mnt/etc/fstab")
    fstab_contents = check_output(["genfstab", "-U", "/mnt"]).decode()
    with open("/mnt/etc/fstab", "w+") as fstab:
        fstab.write(fstab_contents + "\n")
    __update__(34)
    # STEP 5: copy scripts into chroot
    file_list = listdir("/usr/share/system-installer/modules")
    for each in range(len(file_list) - 1, -1, -1):
        if "partitioner" in file_list[each]:
            del file_list[each]
    for each in file_list:
        if each == "__pycache__":
            continue
        common.eprint("/usr/share/system-installer/modules/%s --> /mnt/%s" %
                      (each, each))
        copyfile("/usr/share/system-installer/modules/" + each, "/mnt/" + each)
    __update__(35)
    # STEP 6: Run Master script inside chroot
    # don't run it as a background process so we know when it gets done
    common.eprint("/mnt/etc/resolv.conf" + " --> " + "/mnt/etc/resolv.conf.save")
    move("/mnt/etc/resolv.conf", "/mnt/etc/resolv.conf.save")
    copyfile("/etc/resolv.conf", "/mnt/etc/resolv.conf")
    __update__(36)
    # Check to make sure all these vars are set
    # if not, set them to some defaults
    if settings["LANG"] == "":
        common.eprint("$LANG_SET is not set. Defaulting to english")
        settings["LANG"] = "english"
    if settings["TIME_ZONE"] == "":
        common.eprint("$TIME_ZONE is not set. Defaulting to EST")
        settings["TIME_ZONE"] = "America/New_York"
    if settings["USERNAME"] == "":
        common.eprint("$USERNAME is not set. No default. Prompting user . . .")
        settings["USERNAME"] = check_output(["zenity", "--entry",
                                             r"""--text=\"We're sorry.
                                             We lost your username somewhere in the chain.
                                             What was it again?\""""]
                                            ).decode()
        settings["USERNAME"] = settings["USERNAME"][0:-1]
    if settings["COMPUTER_NAME"] == "":
        common.eprint("$COMP_NAME is not set. Defaulting to drauger-system-installed")
        settings["COMPUTER_NAME"] = "drauger-system-installed"
    if settings["PASSWORD"] == "":
        common.eprint("$PASSWORD is not set. No default. Prompting user . . .")
        settings["PASSWORD"] = check_output(["zenity", "--entry",
                                             "--hide-text",
                                             r"""--text=\"We're sorry.
                                             We lost your password somewhere in the chain.
                                             What was it again?\""""]
                                            ).decode()
        settings["PASSWORD"] = settings["PASSWORD"][0:-1]
    if settings["EXTRAS"] == "":
        common.eprint("$EXTRAS is not set. Defaulting to false.")
        settings["EXTRAS"] = False
    if settings["UPDATES"] == "":
        common.eprint("$UPDATES is not set. Defaulting to false.")
        settings["UPDATES"] = False
    # ues check_call(["arch-chroot", "python3", "/master.py", ...]) because it
    # jumps through a lot of hoops for us.
    # check_call(["arch-chroot", "python3", "/master.py", settings],
    # stdout=stderr.buffer)
    # Copy live system networking settings into installed system
    rmtree("/mnt/etc/NetworkManager/system-connections")
    copytree("/etc/NetworkManager/system-connections",
             "/mnt/etc/NetworkManager/system-connections")
    if path.exists(work_dir) and path.exists(work_dir + "/assets"):
        ls = listdir(work_dir + "/assets")
        mkdir("/mnt/user-data")
        if "master" in ls:
            file_type = listdir(work_dir + "/assets/master")[0].split("/")[-1].split(".")[-1]
            copyfile(work_dir + "/assets/master/wallpaper." + file_type,
                     "/mnt/user-data/wallpaper." + file_type)
            copyfile(work_dir + "/assets/screens.list",
                     "/mnt/user-data/screens.list")
        else:
            for each in ls:
                copytree(work_dir + "/assets/" + each,
                         "/mnt/user-data/" + each)
    real_root = chroot.arch_chroot("/mnt")
    modules.master.install(settings)
    chroot.de_chroot(real_root, "/mnt")
    common.eprint("Removing installation scripts and resetting resolv.conf")
    for each in file_list:
        common.eprint("Removing /mnt/" + each)
        try:
            remove("/mnt/" + each)
        except FileNotFoundError:
            pass
        except IsADirectoryError:
            rmtree("/mnt/" + each)
    __update__(89)
    remove("/mnt/etc/resolv.conf")
    move("/mnt/etc/resolv.conf.save", "/mnt/etc/resolv.conf")
    __update__(98)
    file_list = listdir("/mnt/boot")
    for each in range(len(file_list) - 1, -1, -1):
        if "vmlinuz" not in file_list[each]:
            del file_list[each]
    if len(file_list) == 0:
        common.eprint("\t###\tKERNEL NOT INSTALLED. CORRECTING . . .\t###\t")
        copyfile("/usr/share/system-installer/modules/kernel.tar.xz",
                 "/mnt/kernel.tar.xz")
        root_dir = chroot.arch_chroot("/mnt")
        tar_file = tar.open("kernel.tar.xz")
        tar_file.extractall()
        tar_file.close()
        check_call(["dpkg", "-R", "--install", "/kernel"])
        chroot.de_chroot(root_dir, "/mnt")
        rmtree("/mnt/kernel")
        remove("/mnt/kernel.tar.xz")
    file_list = listdir("/mnt/boot/efi/loader/entries")
    if ((len(file_list) == 0) and ((settings["EFI"] is None) or
                                   (settings["EFI"] == "") or (settings["EFI"] == "NULL"))):
        common.eprint("\t###\tSYSTEMD-BOOT NOT CONFIGURED. CORRECTING . . .\t###\t")
        copyfile("/usr/share/system-installer/modules/systemd_boot_config.py",
                 "/mnt/systemd_boot_config.py")
        check_call(["arch-chroot", "/mnt", "python3",
                    "/systemd_boot_config.py", settings["ROOT"]])
        check_call(["arch-chroot", "/mnt",
                    "/etc/kernel/postinst.d/zz-update-systemd-boot"])
        remove("/mnt/systemd_boot_config.py")
    try:
        rmtree("/mnt/home/" + settings["USERNAME"] +
               "/.config/xfce4/panel/launcher-3")
    except FileNotFoundError:
        pass
    __update__(100)
    common.eprint("\t###\tinstaller.py CLOSED\t###\t")
