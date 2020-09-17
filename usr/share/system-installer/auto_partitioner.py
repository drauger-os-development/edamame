#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  auto_partitioner.py
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
"""Auto-partition Drive selected for installation"""
import common
import subprocess
import json
import sys


limiter = 16 * (1 ** 9)


def __parted__(device, args):
    """Make call to parted

    device: Should be path to device file (e.g.: /dev/foo)
    command: command to be run, as a list (e.g.: ["mkpart", "primary", "ext4", "0%", "100%"])
    """
    # pre-define command
    command = ["parted", "--script", str(device)]
    # make sure `args' is a list
    if not isinstance(args, list):
        raise TypeError("`args' argument not of type `list'")
    # append arguments to our command
    for each in args:
        command.append(str(each))
    # run our command
    return subprocess.check_output(command).decode()


def check_disk_state():
    """Check disk state as registered with lsblk

    Returns data as dictionary"""
    command = ["lsblk", "--json", "--paths", "--bytes", "--output",
               "name,size,type,fstype"]
    data = json.loads(subprocess.check_output(command))["blockdevices"]
    for each in range(len(data) - 1, -1, -1):
        if data[each]["type"] == "loop":
            del data[each]
    return data


def __make_efi__(device, start="0%", end="200M"):
    """Make EFI partition

    Start defaults to beginning of the drive
    end defaults to the 200MB mark on the drive
    """
    __parted__(device, ["mkpart", "primary", "fat32", str(start), str(end)])
    drive = check_disk_state()
    for each in drive:
        if each["name"] == device:
            drive = each["children"]
            break
    for each in range(len(drive) - 1, -1, -1):
        if drive[each]["fstype"] not in ("vfat", "fat32"):
            del drive[each]
    drive = drive[0]["name"]
    process = Popen(["mkfs.fat", "-F", "32", drive], stdout=sys.stderr.buffer,
                                                stdin=PIPE, stderr=PIPE)
    process.communicate(input=bytes("y\n", "utf-8"))


def __make_root__(device, start="201M", end="100%"):
    """Make root partition

    Start defaults to 201MB mark on the drive
    end defaults to the end of the drive
    """
    __parted__(device, ["mkpart", "primary", "ext4", str(start), str(end)])
    for each in drive:
        if each["name"] == device:
            drive = each["children"]
            break
    for each in range(len(drive) - 1, -1, -1):
        if drive[each]["fstype"] not in ("ext4", "EXT4"):
            del drive[each]
    drive = drive[0]["name"]
    process = Popen(["mkfs.ext4", drive], stdout=stderr.buffer, stdin=PIPE,
                                              stderr=PIPE)
    process.communicate(input=bytes("y\n", "utf-8"))


def __make_home__(device, start="35%", end="100%"):
    """Easy sorta-macro to make a home partiton"""
    __make_root__(device, start, end)


def __generate_return_data__(home, efi, part1, part2, part3):
    """Generate return data for wherever we are in the code"""
    parts = {}
    if efi:
        parts["EFI"] = part1
        parts["ROOT"] = part2
    else:
        parts["EFI"] = None
        parts["ROOT"] = part1
    if home != "MAKE":
        parts["HOME"] = home
    else:
        if efi:
            parts["HOME"] = part3
        else:
            parts["HOME"] = part2
    return parts


def __get_part_endpoints__(root):
    """Get partition endpoints on drive `root'"""
    data = __parted__(root, ["unit", "MB", "print"]).split("\n")
    for each in enumerate(data):
        data[each[0]] = data[each[0]].split(" ")
        if data[each[0]][0] == "Number":
            delete_point = each[0]
    data = data[delete_point + 1:]
    for each in enumerate(data):
        for each1 in range(len(data[each[0]]) - 1, -1, -1):
            if data[each[0]][each1] == "":
                del data[each[0]][each1]
    for each in range(len(data) - 1, -1, -1):
        if data[each] == []:
            del data[each]
        else:
            data[each] = data[each][:5]
    return data


def __get_new_entry__(old, new):
    """Get name of new partition"""
    for each in range(len(new) - 1, -1, -1):
        if new[each] in old:
            del new[each]
    data = []
    for each in new:
        data.append(new["name"])
    return data


def __get_children__(data, drive):
    """Get partitions of a drive"""
    for each in data:
        if each["name"] == drive:
            return each["children"]


def partition(root, efi, home):
    """Partiton our installation drive"""
    common.eprint("\t###\tauto_partioner.py STARTED\t###\t")
    part1 = None
    part2 = None
    part3 = None
    if home in ("NULL", "null", None, "MAKE"):
        common.eprint("MAKING NEW PARTITION TABLE.")
        __parted__(root, ["mktable", "gpt"])
    else:
        common.eprint("HOME PARTITION EXISTS. NOT MAKING NEW PARTITION TABLE")

    # That was the easy part. Now comes the part that needs some inteligence
    partitions = check_disk_state()
    for each in partitions:
        if ((each["name"] == root) and (each["size"] == limiter)):
            if home == "MAKE":
                common.eprint("CANNOT MAKE HOME PARTITION. NOT ENOUGH SPACE.")
                raise RuntimeError("CANNOT MAKE HOME PARTITION. NOT ENOUGH SPACE.")
            else:
                if efi:
                    __make_efi__(root)
                    part1 = __get_new_entry__(__get_children__(partitions,
                                                               root),
                                              __get_children__(check_disk_state(),
                                                               root))[0]
                    partitions = check_disk_state()
                    __make_root__(root)
                    part2 = __get_new_entry__(__get_children__(partitions,
                                                               root),
                                              __get_children__(check_disk_state(),
                                                               root))[0]
                else:
                    __make_root__(root)
                    part1 = __get_new_entry__(__get_children__(partitions,
                                                               root),
                                              __get_children__(check_disk_state(),
                                                               root))[0]
                partitions = check_disk_state()
                common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
                return __generate_return_data__(home, efi, part1, part2, part3)
    # Handled 16GB drives
    # From here until 64GB drives, we want our root partition to be AT LEAST
    # 16GB
    if home == "MAKE":
        # If home == "MAKE", we KNOW there are no partitons because we made a
        # new partition table
        root_end = "16G"
        if (efi and (part1 != None)):
            __make_efi__(root)
            part1 = __get_new_entry__(__get_children__(partitions, root),
                                      __get_children__(check_disk_state(),
                                                       root))[0]
            partitions = check_disk_state()
            __make_root__(root, end=root_end)
            part2 = __get_new_entry__(__get_children__(partitions, root),
                                      __get_children__(check_disk_state(),
                                                       root))[0]
            partitions = check_disk_state()
            __make_home__(root, start=root_end)
            part3 = __get_new_entry__(__get_children__(partitions, root),
                                      __get_children__(check_disk_state(),
                                                       root))[0]
            partitions = check_disk_state()
        elif part1 != None:
            __make_root__(root, start="0%", end=root_end)
            part1 = __get_new_entry__(__get_children__(partitions, root),
                                      __get_children__(check_disk_state(),
                                                       root))[0]
            partitions = check_disk_state()
            __make_home__(root, start=root_end)
            part2 = __get_new_entry__(__get_children__(partitions, root),
                                      __get_children__(check_disk_state(),
                                                       root))[0]
            partitions = check_disk_state()
        common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
        return __generate_return_data__(home, efi, part1, part2, part3)
    elif home in ("NULL", "null", None):
        # If home == any possible 'null' value,
        # we KNOW there are no partitons because we made a
        # new partition table
        if efi:
            __make_efi__(root)
            part1 = __get_new_entry__(__get_children__(partitions, root),
                                      __get_children__(check_disk_state(),
                                                       root))[0]
            partitions = check_disk_state()
            __make_root__(root)
            part2 = __get_new_entry__(__get_children__(partitions, root),
                                      __get_children__(check_disk_state(),
                                                       root))[0]
            partitions = check_disk_state()
        else:
            __make_root__(root, start="0%")
            part1 = __get_new_entry__(__get_children__(partitions, root),
                                      __get_children__(check_disk_state(),
                                                       root))[0]
            partitions = check_disk_state()
        common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
        return __generate_return_data__(home, efi, part1, part2, part3)
    else:
        # This one we need to figure out if the home partiton is on the drive
        # we are working on or elsewhere
        if "nvme" in home:
            check = home[:-2]
        else:
            check = home[:-1]
        if root == check:
            # It IS on the same drive. We need to figure out where at and work
            # around it
            # NOTE: WE NEED TO WORK IN MB ONLY IN THIS SECTION
            data = __get_part_endpoints__(root)
            # We now know:
                # Where each partiton starts and stops
                # How big each partition is
                # Each partition number
                # Each partition's FS type
            # Lets make some partitons!
            if efi:
                for each in enumerate(data):
                    # This loop makes our EFI partition
                    if each[0] == 0:
                        start_check = 0
                    else:
                        start_check = float(data[each[0] - 1][1][:-2])
                    end_check = float(data[each[0]][2][:-2])
                    if (end_check - start_check) >= 200:
                        __make_efi__(root, start=data[each[0] - 1][1][:-1],
                                    end=data[each[0]][1][:-1])
                        part1 = __get_new_entry__(__get_children__(partitions,
                                                                   root),
                                                  __get_children__(check_disk_state(),
                                                                 root))[0]
                        partitions = check_disk_state()
                        # We MUST make sure to break here or else we will make a
                        # shit ton of 200 MB partitions on the drive
                        break
                # refresh our partition end points
                data = __get_part_endpoints__(root)
            # Find our largest gap
            gap = []
            for each in enumerate(data):
                if each[0] == 0:
                    start_check = 0
                else:
                    start_check = float(data[each[0] - 1][1][:-2])
                end_check = float(data[each[0]][2][:-2])
                gap.append(end_check - start_check)
            gap = max(gap)
            # Make our root partition
            for each in enumerate(data):
                if each[0] == 0:
                    start_check = 0
                else:
                    start_check = float(data[each[0] - 1][1][:-2])
                end_check = float(data[each[0]][2][:-2])
                if (end_check - start_check) == gap:
                    __make_root__(root, start=data[each[0] - 1][1][:-1],
                                 end=data[each[0]][1][:-1])
                    if efi:
                        part2 = __get_new_entry__(__get_children__(partitions,
                                                                   root),
                                                  __get_children__(check_disk_state(),
                                                                   root))[0]
                    else:
                        part1 = __get_new_entry__(__get_children__(partitions,
                                                                   root),
                                                  __get_children__(check_disk_state(),
                                                                   root))[0]
                    partitions = check_disk_state()
            ### WORK IN PROGRESS ###
        else:
            # it's elsewhere. We're good.
            if efi:
                __make_efi__(root)
                part1 = __get_new_entry__(__get_children__(partitions, root),
                                        __get_children__(check_disk_state(),
                                                         root))[0]
                partitions = check_disk_state()
                __make_root__(root)
                part2 = __get_new_entry__(__get_children__(partitions, root),
                                          __get_children__(check_disk_state(),
                                                           root))[0]
                partitions = check_disk_state()
            else:
                __make_root__(root, start="0%")
                part1 = __get_new_entry__(__get_children__(partitions, root),
                                          __get_children__(check_disk_state(),
                                                           root))[0]
                partitions = check_disk_state()
        part3 = home
    # Figure out what parts are for what
    # Return that data as a dictonary
    common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
    return __generate_return_data__(home, efi, part1, part2, part3)


