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
from __future__ import print_function
from sys import stderr
from subprocess import Popen, check_output, check_call
from os import mkdir, path, chdir, listdir, remove, symlink, chmod
from shutil import rmtree, move, copyfile, copytree
import json
import UI
import modules
import chroot

# Make it easier for us to print to stderr
def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def __mount__(device, path):
    """Mount device at path
    It would be much lighter weight to use ctypes to do this
    But, that keeps throwing an 'Invalid Argument' error.
    Calling Mount with check_call is the safer option.
    """
    try:
        check_call(["mount", device, path])
    except:
        pass

def __update__(percentage):
    try:
        with open("/tmp/system-installer-progress.log", "w+") as progress:
            progress.write(str(percentage))
    except PermissionError:
        chmod("/tmp/system-installer-progress.log", 0o666)
        with open("/tmp/system-installer-progress.log", "w+") as progress:
            progress.write(str(percentage))


def install(settings):
    eprint("\t###\tinstaller.py STARTED\t###\t")
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
    # STEP 1: Partion and format the drive ( if needed )
    if settings["AUTO_PART"]:
        partitioning = json.loads(check_output(
            ["/usr/share/system-installer/modules/auto-partitioner.sh",
            settings["ROOT"], settings["EFI"], settings["HOME"]]))
        settings["ROOT"] = partitioning["ROOT"]
        settings["EFI"] = partitioning["EFI"]
        settings["HOME"] = partitioning["HOME"]
    if path.exists("/tmp/system-installer-progress.log"):
        remove("/tmp/system-installer-progress.log")
    __update__(12)
    # STEP 2: Mount the new partitions
    __mount__(settings["ROOT"], "/mnt")
    if settings["EFI"] != "NULL":
        try:
            mkdir("/mnt/boot")
        except FileExistsError:
            pass
        try:
            mkdir("/mnt/boot/efi")
        except FileExistsError:
            pass
        __mount__(settings["EFI"], "/mnt/boot/efi")
    if settings["HOME"] != "NULL":
        try:
            mkdir("/mnt/home")
        except FileExistsError:
            eprint("/mnt/home exists when it shouldn't. What the hell is going on???")
            pass
        __mount__(settings["HOME"], "/mnt/home")
    if settings["SWAP"] != "FILE":
        # This can happen in the background. No biggie.
        Popen(["swapon", settings["SWAP"]])
    else:
        eprint("SWAPFILE NOT CREATED YET")
    __update__(14)
    # STEP 3: Unsquash the sqaushfs and get the files where they need to go
    squashfs = ""
    with open("/etc/system-installer/default.json", "r") as config:
        squashfs = json.loads(config.read())["squashfs_Location"]
    if not path.exists(squashfs):
        eprint("\n\tSQUASHFS FILE DOES NOT EXIST\t\n")
        UI.error.show_error("\n\tSQUASHFS FILE DOES NOT EXIST\t\n")
    __update__(17)
    chdir("/mnt")
    eprint("CLEANING INSTALLATION DIRECTORY")
    death_row = listdir()
    for each in death_row:
        if ((each != "boot") and (each !="home")):
            rmtree(each)
    chdir("/mnt/boot")
    death_row = listdir()
    for each in death_row:
        if (each != "efi"):
            try:
                rmtree(each)
            except NotADirectoryError:
                remove(each)
    chdir("/mnt")
    eprint("\t###\tEXTRACTING SQUASHFS\t###\t")
    check_call(["unsquashfs", squashfs])
    eprint("\t###\tEXTRACTION COMPLETE\t###\t")
    file_list = listdir("/mnt/squashfs-root")
    for each in file_list:
        eprint("/mnt/squashfs-root/" + each + " --> /mnt/" + each)
        move("/mnt/squashfs-root/" + each, "/mnt/" + each)
    rmtree("/mnt/squashfs-root")
    try:
        mkdir("/mnt/boot")
    except FileExistsError:
        eprint("/mnt/boot already created")
    file_list = listdir("/boot")
    for each in file_list:
        try:
            eprint("/boot/" + each + " --> /mnt/boot/" + each)
            copyfile("/boot/" + each, "/mnt/boot/" + each)
        except IsADirectoryError:
            copytree("/boot/" + each, "/mnt/boot/" + each)
    copyfile("/tmp/system-installer-progress.log", "/mnt/tmp/system-installer-progress.log")
    remove("/tmp/system-installer-progress.log")
    symlink("/mnt/tmp/system-installer-progress.log","/tmp/system-installer-progress.log")
    __update__(32)
    # STEP 4: Update fstab
    eprint("\t###\tUpdating FSTAB\t###\t")
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
        eprint("/usr/share/system-installer/modules/" + each + " --> " + "/mnt/" + each)
        copyfile("/usr/share/system-installer/modules/" + each, "/mnt/" + each)
    __update__(35)
    # STEP 6: Run Master script inside chroot
    # don't run it as a background process so we know when it gets done
    eprint("/mnt/etc/resolv.conf" + " --> " + "/mnt/etc/resolv.conf.save")
    move("/mnt/etc/resolv.conf", "/mnt/etc/resolv.conf.save")
    copyfile("/etc/resolv.conf", "/mnt/etc/resolv.conf")
    __update__(36)
    # Check to make sure all these vars are set
    # if not, set them to some defaults
    if settings["LANG"] == "":
        eprint("$LANG_SET is not set. Defaulting to english")
        settings["LANG"] = "english"
    if settings["TIME_ZONE"] == "":
        eprint("$TIME_ZONE is not set. Defaulting to EST")
        settings["TIME_ZONE"] = "America/New_York"
    if settings["USERNAME"] == "":
        eprint("$USERNAME is not set. No default. Prompting user . . .")
        settings["USERNAME"] = check_output(["zenity", "--entry", r"--text=\"We're sorry. We lost your username somewhere in the chain. What was it again?\""]).decode()
        settings["USERNAME"] = settings["USERNAME"][0:len(settings["USERNAME"]) - 1]
    if settings["COMPUTER_NAME"] == "":
        eprint("$COMP_NAME is not set. Defaulting to drauger-system-installed")
        settings["COMPUTER_NAME"] = "drauger-system-installed"
    if settings["PASSWORD"] == "":
        eprint("$PASSWORD is not set. No default. Prompting user . . .")
        settings["PASSWORD"] = check_output(["zenity", "--entry", "--hide-text", r"--text=\"We're sorry. We lost your password somewhere in the chain. What was it again?\""]).decode()
        settings["PASSWORD"] = settings["PASSWORD"][0:len(settings["PASSWORD"]) - 1]
    if settings["EXTRAS"] == "":
        eprint("$EXTRAS is not set. Defaulting to false.")
        settings["EXTRAS"] = False
    if settings["UPDATES"] == "":
        eprint("$UPDATES is not set. Defaulting to false.")
        settings["UPDATES"] = False
    # ues check_call(["arch-chroot", "python3", "/master.py", ...]) because it
    # jumps through a lot of hoops for us.
    # check_call(["arch-chroot", "python3", "/master.py", settings], stdout=stderr.buffer)
    internet = modules.master.check_internet()
    real_root = chroot.arch_chroot("/mnt")
    modules.master.install(settings, internet)
    chroot.de_chroot(real_root, "/mnt")
    eprint("Removing installation scripts and resetting resolv.conf")
    for each in file_list:
        eprint("Removing /mnt/" + each)
        remove("/mnt/" + each)
    __update__(89)
    remove("/mnt/etc/resolv.conf")
    move("/mnt/etc/resolv.conf.save", "/mnt/etc/resolv.conf")
    __update__(98)
    file_list = listdir("/mnt/boot")
    for each in range(len(file_list) - 1, -1, -1):
        if "vmlinuz" not in file_list[each]:
            del file_list[each]
    if len(file_list) == 0:
        eprint("\t###\tKERNEL NOT INSTALLED. CORRECTING . . .\t###\t")
        copyfile("/usr/share/system-installer/modules/kernel.7z", "/mnt/kernel.7z")
        check_call(["arch-chroot", "/mnt", "\"bash -c '7z x /kernel.7z; dpkg -R --install /kernel/'\""])
        rmtree("/mnt/kernel")
        remove("/mnt/kernel.7z")
    file_list = list_dir("/mnt/boot/efi/loader/entries")
    if ((len(file_list) == 0) and ((settings["EFI"] == None) or (settings["EFI"] == "") or (settings["EFI"] == "NULL"))):
        eprint("\t###\tSYSTEMD-BOOT NOT CONFIGURED. CORRECTING . . .\t###\t")
        copyfile("/usr/share/system-installer/modules/systemd_boot_config.py", "/mnt/systemd_boot_config.py")
        check_call(["arch-chroot", "/mnt", "python3", "/systemd_boot_config.py", settings["ROOT"]])
        check_call(["arch-chroot", "/mnt", "/etc/kernel/postinst.d/zz-update-systemd-boot"])
        remove("/mnt/systemd_boot_config.py")
    try:
        rmtree("/mnt/home/" + settings["USERNAME"] + "/.config/xfce4/panel/launcher-3")
    except FileNotFoundError:
        pass
    __update__(100)
    remove("/tmp/system-installer-progress.log")
    remove("/mnt/tmp/system-installer-progress.log")
    eprint("\t###\tinstaller.py CLOSED\t###\t")

