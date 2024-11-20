#!shebang
# -*- coding: utf-8 -*-
#
#  installer.py
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
"""Main module controling the installation process"""
from subprocess import Popen, check_output, check_call, CalledProcessError
import os
import shutil
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
        with open("/tmp/edamame-progress.log", "w+") as progress:
            progress.write(str(percentage))
    except PermissionError:
        os.chmod("/tmp/edamame-progress.log", 0o666)
        with open("/tmp/edamame-progress.log", "w+") as progress:
            progress.write(str(percentage))


def install(settings: dict, local_repo: str, ui_type: str) -> None:
    """Begin installation proceidure

    settings should be a dictionary with the following values:
        AUTO_PART : bool
        ROOT : device path as str
        HOME : device path as str
        EFI : device path
        SWAP : device path or 'FILE'
        raid_array : dict containing the following values:
            raid_type : raid type (0, 1, 10) as str. e.g.: "RAID10", if not used, None
            disks : disk of numbers 1-4 as keys, with their values being the disks
                    to use for the RAID array. If not used, None.
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

    You can read in /etc/edamame/quick-install-template.json with
    json.loads()["DATA"] to see an example of acceptable settings
    """
    common.eprint("    ###    installer.py STARTED    ###    ")
    UI = UI.load_UI(ui_type)
    work_dir = "/tmp/quick-install_working-dir"
    # STEP 1: Partion and format the drive ( if needed )
    if settings["AUTO_PART"]:
        partitioning = auto_partitioner.partition(settings["ROOT"],
                                                  settings["EFI"],
                                                  settings["HOME"],
                                                  settings["raid_array"])
        settings["ROOT"] = partitioning["ROOT"]
        settings["EFI"] = partitioning["EFI"]
        settings["HOME"] = partitioning["HOME"]
    else:
        if settings["EFI"] in ("NULL", None, "", False):
            auto_partitioner.make_part_boot(settings["ROOT"])
        else:
            auto_partitioner.make_part_boot(settings["EFI"])
    if os.path.exists("/tmp/edamame-progress.log"):
        os.remove("/tmp/edamame-progress.log")
    __update__(12)
    # STEP 2: Mount the new partitions
    __mount__(settings["ROOT"], "/mnt")
    if settings["EFI"] not in ("NULL", None, "", False):
        try:
            os.mkdir("/mnt/boot")
        except FileExistsError:
            pass
        try:
            os.mkdir("/mnt/boot/efi")
        except FileExistsError:
            pass
        __mount__(settings["EFI"], "/mnt/boot/efi")
    if settings["HOME"] not in ("NULL", None, ""):
        try:
            os.mkdir("/mnt/home")
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
    with open("/etc/edamame/settings.json", "r") as file:
        config = json.loads(file.read())
    if not os.path.exists(config["squashfs_Location"]):
        common.eprint("\n    SQUASHFS FILE DOES NOT EXIST    \n")
        UI.error.show_error("\n\tSQUASHFS FILE DOES NOT EXIST\t\n")
    __update__(17)
    os.chdir("/mnt")
    common.eprint("CLEANING INSTALLATION DIRECTORY")
    death_row = os.listdir()
    for each in death_row:
        if each not in ("boot", "home"):
            common.eprint("Removing " + each)
            try:
                shutil.rmtree(each)
            except NotADirectoryError:
                os.remove(each)
    try:
        os.chdir("/mnt/boot")
        death_row = os.listdir()
        for each in death_row:
            if each != "efi":
                try:
                    shutil.rmtree(each)
                except NotADirectoryError:
                    os.remove(each)
        os.chdir("/mnt")
    except FileNotFoundError:
        pass
    common.eprint("    ###    EXTRACTING SQUASHFS    ###    ")
    cmd = ["unsquashfs", config["squashfs_Location"]]
    # we're doing this as a tuple/list so that more can be added to this list later
    if auto_partitioner.get_fs(settings["ROOT"]) in ("ext2",):
        cmd.append("-no-xattrs")
    check_call(cmd)
    common.eprint("    ###    EXTRACTION COMPLETE    ###    ")
    file_list = os.listdir("/mnt/squashfs-root")
    for each in file_list:
        try:
            common.eprint("/mnt/squashfs-root/" + each + " --> /mnt/" + each)
            shutil.move("/mnt/squashfs-root/" + each, "/mnt/" + each)
        except shutil.Error as e:
            common.eprint("ERROR: %s" % (e))
    shutil.rmtree("/mnt/squashfs-root")
    try:
        os.mkdir("/mnt/boot")
    except FileExistsError:
        common.eprint("/mnt/boot already created")
    shutil.copyfile("/tmp/edamame-progress.log",
                    "/mnt/tmp/edamame-progress.log")
    os.remove("/tmp/edamame-progress.log")
    os.symlink("/mnt/tmp/edamame-progress.log",
            "/tmp/edamame-progress.log")
    __update__(32)
    # STEP 4: Update fstab
    common.eprint("    ###    Updating FSTAB    ###    ")
    os.remove("/mnt/etc/fstab")
    fstab_contents = check_output(["genfstab", "-U", "/mnt"]).decode()
    with open("/mnt/etc/fstab", "w+") as fstab:
        fstab.write(fstab_contents + "\n")
    __update__(34)
    # STEP 5: Extract Tar ball if needed, copy files to installation drive
    if not os.path.exists(local_repo):
        common.eprint("EXTRACTING KERNEL.TAR.XZ")
        tar_file = tar.open("/usr/share/edamame/kernel.tar.xz")
        tar_file.extractall(path="/")
        tar_file.close()
        common.eprint("EXTRACTION COMPLETE")
        # try to use the default path. If an OSError or PermissionError is thrown,
        # default to a path that should be good. This may mean more memory usage
        # since /tmp is in memory, not on disk. But that's a sacrifice we can make here
        try:
            common.recursive_mkdir(local_repo)
        except (OSError, PermissionError):
            local_repo = "/tmp/edamame/repo"
            common.recursive_mkdir(local_repo)
        # Copy everything into local_repo at top level
        # We COULD go ahead and copy everything where it needs to be, but that would
        # make for more code and an extra check I don't wanna bother with right now
        branches = os.listdir("/kernel")
        for each in branches:
            lv2 = os.listdir("/kernel/" + each)
            for each1 in lv2:
                shutil.move(f"/kernel/{each}/{each1}", f"{local_repo}/{each1}")
    shutil.copytree(local_repo, "/mnt/repo")
    __update__(35)
    # STEP 6: Run Master script inside chroot
    # don't run it as a background process so we know when it gets done
    common.eprint("/mnt/etc/resolv.conf" + " --> " + "/mnt/etc/resolv.conf.save")
    shutil.move("/mnt/etc/resolv.conf", "/mnt/etc/resolv.conf.save")
    shutil.copyfile("/etc/resolv.conf", "/mnt/etc/resolv.conf")
    __update__(36)
    # Copy live system networking settings into installed system
    shutil.rmtree("/mnt/etc/NetworkManager/system-connections")
    shutil.copytree("/etc/NetworkManager/system-connections",
                    "/mnt/etc/NetworkManager/system-connections")
    if os.path.exists(work_dir) and os.path.exists(work_dir + "/assets"):
        ls = os.listdir(work_dir + "/assets")
        os.mkdir("/mnt/user-data")
        if "master" in ls:
            file_type = os.listdir(work_dir + "/assets/master")[0].split("/")[-1].split(".")[-1]
            shutil.copyfile(work_dir + "/assets/master/wallpaper." + file_type,
                            "/mnt/user-data/wallpaper." + file_type)
            shutil.copyfile(work_dir + "/assets/screens.list",
                            "/mnt/user-data/screens.list")
        else:
            for each in ls:
                shutil.copytree(work_dir + "/assets/" + each,
                                "/mnt/user-data/" + each)
    real_root = chroot.arch_chroot("/mnt")
    modules.master.install(settings, config["distro"].replace(" ", "_"))
    chroot.de_chroot(real_root, "/mnt")
    common.eprint("Resetting resolv.conf")
    os.remove("/mnt/etc/resolv.conf")
    shutil.move("/mnt/etc/resolv.conf.save", "/mnt/etc/resolv.conf")
    __update__(96)
    try:
        file_list = os.listdir("/mnt/boot/efi/loader/entries")
    except FileNotFoundError:
        file_list = []
    if ((len(file_list) == 0) and (settings["EFI"] not in (None, "", "NULL", False))):
        common.eprint("    ###    SYSTEMD-BOOT NOT CONFIGURED. CORRECTING . . .    ###    ")
        check_call(["arch-chroot", "/mnt", "systemd-boot-manager", "-r"])
    try:
        shutil.rmtree("/mnt/home/" + settings["USERNAME"] +
                      "/.config/xfce4/panel/launcher-3")
    except FileNotFoundError:
        pass
    __update__(100)
    common.eprint("    ###    installer.py CLOSED    ###    ")
