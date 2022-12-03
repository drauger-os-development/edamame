#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  auto_partitioner.py
#
#  Copyright 2022 Thomas Castleman <contact@draugeros.org>
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
import json
import time
import os
import sys
import subprocess
import parted
import psutil
import common


def gb_to_bytes(gb):
    """Convert GB to Bytes"""
    return gb * (10 ** 9)


def bytes_to_gb(b):
    """Convert Bytes to GB"""
    return b / (10 ** 9)


def is_EFI():
    """Get if the current system is using EFI"""
    return os.path.isdir("/sys/firmware/efi")


# GET DEFAULT CONFIG
LIMITER = gb_to_bytes(32)
PARTITIONING_ENABLED = True

# get configuration for partitioning
config = {
            "partitioning": {
                "EFI": {
                    "EFI": {
                        "START": 0,
                        "END": 500
                            },
                    "ROOT": {
                        "START": 501,
                        "END": "40%",
                        "fs": "btrfs"
                            },
                    "HOME": {
                        "START": "40%",
                        "END": "100%",
                        "fs": "btrfs"
                            }
                        },
                "BIOS": {
                    "ROOT": {
                        "START": 0,
                        "END": "40%",
                        "fs": "ext4"
                            },
                    "HOME": {
                        "START": "40%",
                        "END": "100%",
                        "fs": "btrfs"
                            }
                        },
                "GENERAL": {
                    "min root size": 23000,
                    "mdswh": 128
                        }
            }
        }

try:
    with open("/etc/system-installer/settings.json", "r") as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    config_data = config


# check to make sure packager left this block in
if "partitioning" in config_data:
    new_config = config_data["partitioning"]
else:
    common.eprint("Partitioning settings not found. Cannot partition drives automatically")
    PARTITIONING_ENABLED = False


if is_EFI():
    try:
        new_config = new_config["EFI"]  | new_config["GENERAL"]
        config = config["partitioning"]["EFI"] | config["partitioning"]["GENERAL"]
    except KeyError:
        common.eprint("EFI or General partitioning details not defined. Falling back to defaults")
        print("EFI or General partitioning details not defined. Falling back to defaults")
        new_config = config["partitioning"]["EFI"] | config["partitioning"]["GENERAL"]
else:
    try:
        new_config = new_config["BIOS"] | new_config["GENERAL"]
        config = config["partitioning"]["BIOS"] | config["partitioning"]["GENERAL"]
    except KeyError:
        common.eprint("BIOS or General partitioning details not defined. Falling back to defaults")
        print("BIOS or General partitioning details not defined. Falling back to defaults")
        new_config = config["partitioning"]["BIOS"] | config["partitioning"]["GENERAL"]




# make sure everything is there. If not, substitute in defaults
# we don't use config["partitioning"][<key>] syntax here because
# if we enter any of
# these if-statements, then we are not using the built-in settings.
# In which case, because of the above
# block, if we are using externally sourced settings, then config will
# be pared down for us. And if we
# are using the built-in settings, then we won't enter any of
if "ROOT" not in new_config:
    new_config["ROOT"] = config["ROOT"]
if "HOME" not in new_config:
    new_config["HOME"] = config["HOME"]
if is_EFI():
    if "EFI" not in new_config:
        new_config["EFI"] = config["EFI"]
if "min root size" not in new_config:
    new_config["min root size"] = config["min root size"]
if "mdswh" not in new_config:
    new_config["mdswh"] = config["mdswh"]
config = new_config
    # if not, fall back to internal default


def size_of_part(part_path, bytes=False):
    """Get the size of the partition at `part_path`

    If `bytes` is True, return size in bytes.
    Else, return size in gigabytes.
    """
    # Get the root Drive
    root = get_drive_path(part_path)
    # connect to that drive's partition table
    device = parted.getDevice(root)
    try:
        disk = parted.Disk(device)
    except parted._ped.DiskLabelException:
        raise OSError(f"NO PARTITION TABLE EXISTS ON { root } ")
    # Grab the right partiton
    part = disk.getPartitionByPath(part_path)
    # get size
    size = part.getSize(unit="b")
    # size conversion, if necessary
    if not bytes:
        size = bytes_to_gb(size)
    return size


def get_drive_path(part_path):
    """Get drive path from partition path"""
    if ("nvme" in part_path) or ("mmc" in part_path):
        output = part_path[:part_path.index("p")]
    else:
        count = 0
        for each in part_path:
            if not each.isnumeric():
                count+=1
            else:
                break
        output = part_path[:count]
    return output


def get_min_root_size(swap=True, ram_size=False, ram_size_unit=True,
                      bytes=True):
    """Get minimum root partition size as bytes

    When `swap' == True, factor in the ideal size of swap file for
    the current system's RAM.

    If `ram_size' is not an int or float, RAM of the
    current system will be used.

    if `ram_size_unit' is True, `ram_size' should be in GB. When `ram_size_unit'
    is False, `ram_size' should be in bytes.

    If `bytes` is True, return size in bytes.
    Else, return size in gigabytes.
    """
    if swap:
        if type(ram_size) not in (int, float):
            mem = psutil.virtual_memory().total
        else:
            if ram_size_unit:
                mem = gb_to_bytes(ram_size)
            else:
                mem = ram_size
        swap_amount = round((mem + ((mem / 1024 ** 3) ** 0.5) * 1024 ** 3))
    else:
        swap_amount = 0
    min_root_size = swap_amount + (config["min root size"] * (1000 ** 2))
    if not bytes:
        min_root_size = bytes_to_gb(min_root_size)
    return min_root_size


def check_disk_state():
    """Check disk state as registered with lsblk

    Returns data as dictionary
    """
    try:
        subprocess.check_call(["partprobe"])
    except subprocess.CalledProcess:
        print("`partprobe` failed. Provided info may not be up-to-date.")
    time.sleep(0.1)
    command = ["lsblk", "--json", "--paths", "--bytes", "--output",
               "name,size,type,fstype"]
    data = json.loads(subprocess.check_output(command))["blockdevices"]
    for each in range(len(data) - 1, -1, -1):
        if data[each]["type"] == "loop":
            del data[each]
    return data


def get_fs(part_name: str):
    """Get filesystem type for given partition"""
    disk = check_disk_state()
    for each in disk:
        if each["name"] == part_name:
            return each["fstype"]
        if "children" in each:
            for each1 in each["children"]:
                if each1["name"] == part_name:
                    return each1["fstype"]


def __mkfs__(device, fs):
    """Set partition filesystem"""
    # pre-define command
    if "ext" in fs:
        force = "-F"
    else:
        force = "-f"
    command = ["mkfs", "-t", fs, force, str(device)]
    try:
        try:
            data = subprocess.check_output(command).decode()
        except UnicodeDecodeError:
            return ""
    except subprocess.CalledProcessError as error:
        data = error.output.decode()
    return data


if is_EFI():
    def __mkfs_fat__(device):
        """Set partition filesystem to FAT32"""
        # pre-define command
        command = ["mkfs.fat", "-F", "32", str(device)]
        try:
            data = subprocess.check_output(command).decode()
        except subprocess.CalledProcessError as error:
            data = error.output.decode()
        return data


    def __make_efi__(device, start=config["EFI"]["START"],
                     end=config["EFI"]["END"]):
        """Make EFI partition"""
        disk = parted.Disk(device)
        start_geo = parted.geometry.Geometry(device=device,
                                             start=parted.sizeToSectors(start,
                                                                        "MB",
                                                                        device.sectorSize),
                                             end=parted.sizeToSectors(start + 10,
                                                                      "MB",
                                                                      device.sectorSize))
        end_geo = parted.geometry.Geometry(device=device,
                                           start=parted.sizeToSectors(common.real_number(end - 20),
                                                                      "MB",
                                                                      device.sectorSize),
                                           end=parted.sizeToSectors(end + 10,
                                                                    "MB",
                                                                    device.sectorSize))
        min_size = parted.sizeToSectors(common.real_number((end - start) - 25),
                                        "MB",
                                        device.sectorSize)
        max_size = parted.sizeToSectors(common.real_number((end - start) + 20),
                                        "MB",
                                        device.sectorSize)
        const = parted.Constraint(startAlign=device.optimumAlignment,
                                  endAlign=device.optimumAlignment,
                                  startRange=start_geo, endRange=end_geo,
                                  minSize=min_size, maxSize=max_size)
        geometry = parted.geometry.Geometry(start=start,
                                            length=parted.sizeToSectors(end - start,
                                                                        "MB",
                                                                        device.sectorSize),
                                            device=device)
        new_part = parted.Partition(disk=disk,
                                    type=parted.PARTITION_NORMAL,
                                    geometry=geometry)
        new_part.setFlag(parted.PARTITION_BOOT)
        disk.addPartition(partition=new_part, constraint=const)
        disk.commit()
        time.sleep(0.1)
        __mkfs_fat__(new_part.path)
        return new_part.path


def sectors_to_size(sectors, sector_size):
    """Convert number of sectors to sector size"""
    return (sectors * sector_size) / 1000 ** 2


def __make_root__(device, start=config["ROOT"]["START"],
                  end=config["ROOT"]["END"], fs=config["ROOT"]["fs"]):
    """Make root partition"""
    # __parted__(device, ["mkpart", name, fs, str(start), str(end)])
    size = sectors_to_size(device.length, device.sectorSize)
    try:
        if start[-1] == "%":
            start = int(start[:-1]) / 100
            start = int(size * start)
    except TypeError:
        pass
    try:
        if end[-1] == "%":
            end = int(end[:-1]) / 100
            end = int(size * end)
    except TypeError:
        pass
    disk = parted.Disk(device)
    s_geo = parted.geometry.Geometry(device=device,
                                     start=parted.sizeToSectors(common.real_number(start - 20),
                                                                "MB",
                                                                device.sectorSize),
                                     end=parted.sizeToSectors(start + 20,
                                                              "MB",
                                                              device.sectorSize))
    e_geo = parted.geometry.Geometry(device=device,
                                     start=parted.sizeToSectors(common.real_number(end - 100),
                                                                "MB",
                                                                device.sectorSize),
                                     end=parted.sizeToSectors(end, "MB",
                                                              device.sectorSize))
    min_size = parted.sizeToSectors(common.real_number((end - start) - 250),
                                    "MB",
                                    device.sectorSize)
    max_size = parted.sizeToSectors(common.real_number((end - start) + 250),
                                    "MB",
                                    device.sectorSize)
    const = parted.Constraint(startAlign=device.optimumAlignment,
                              endAlign=device.optimumAlignment,
                              startRange=s_geo, endRange=e_geo,
                              minSize=min_size,
                              maxSize=max_size)
    geo = parted.geometry.Geometry(start=parted.sizeToSectors(start, "MB",
                                                              device.sectorSize),
                                   length=parted.sizeToSectors((end - start),
                                                               "MB",
                                                               device.sectorSize),
                                   device=device)
    new_part = parted.Partition(disk=disk,
                                type=parted.PARTITION_NORMAL,
                                geometry=geo)
    try:
        disk.addPartition(partition=new_part, constraint=const)
    except parted._ped.PartitionException:
        # Simply use the geometry of the first free space region, if it is big enough
        data = disk.getFreeSpaceRegions()
        sizes = {}
        for each in data:
            sizes[each.getSize(unit="b")] = each
        sizes_sorted = sorted(sizes)
        made = False
        for each in range(len(sizes_sorted) - 1, -1, -1):
            if sizes[sizes_sorted[each]].getSize(unit="b") >= get_min_root_size():
                s_geo = parted.geometry.Geometry(device=device,
                                                 start=parted.sizeToSectors(common.real_number(sizes[sizes_sorted[each]].start - 2000),
                                                                            "MB",
                                                                            device.sectorSize),
                                                 end=parted.sizeToSectors(sizes[sizes_sorted[each]].start + 2000,
                                                                          "MB",
                                                                          device.sectorSize))
                e_geo = parted.geometry.Geometry(device=device,
                                                 start=parted.sizeToSectors(common.real_number(sizes[sizes_sorted[each]].end - 2000),
                                                                            "MB",
                                                                            device.sectorSize),
                                                 end=parted.sizeToSectors(sizes[sizes_sorted[each]].end + 2000, "MB",
                                                                          device.sectorSize))
                min_size = parted.sizeToSectors(common.real_number((sizes[sizes_sorted[each]].end - sizes[sizes_sorted[each]].start) - 2000),
                                                "MB",
                                                device.sectorSize)
                max_size = parted.sizeToSectors(common.real_number((sizes[sizes_sorted[each]].end - sizes[sizes_sorted[each]].start) + 2000),
                                                "MB",
                                                device.sectorSize)
                const = parted.Constraint(startAlign=device.optimumAlignment,
                                          endAlign=device.optimumAlignment,
                                          startRange=s_geo, endRange=e_geo,
                                          minSize=min_size,
                                          maxSize=max_size)
                new_part = parted.Partition(disk=disk,
                                            type=parted.PARTITION_NORMAL,
                                            geometry=sizes[sizes_sorted[each]])
                try:
                    disk.addPartition(partition=new_part, constraint=const)
                except:
                    break
                made = True
                break
        if not made:
            common.eprint("WAS NOT ABLE TO CREATE ROOT PARTITION. LIKELY NOT ENOUGH SPACE FOR ONE.")
            common.eprint("INSTALLATION WILL FAIL")

    disk.commit()
    time.sleep(0.1)
    __mkfs__(new_part.path, fs)
    return new_part.path


def __make_home__(device, new_start=config["HOME"]["START"],
                  new_end=config["HOME"]["END"], new_fs=config["HOME"]["fs"]):
    """Easy sorta-macro to make a home partiton"""
    return __make_root__(device, start=new_start, end=new_end, fs=new_fs)


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


def __make_root_boot__(device):
    """Make Root partition bootable.

This ONLY works if the root partition is the only partition on the drive
"""
    disk = parted.Disk(device)
    partitions = disk.getPrimaryPartitions()
    partitions[0].setFlag(parted.PARTITION_BOOT)
    disk.commit()


def make_part_boot(part_path):
    """Make a partition bootable.

    This is useful for ensuring that users make their EFI partiton
    (or root partition in the case of BIOS systems) bootable.

    part_path should be set to the path to the partition device file.
    So, if a user's EFI partition is the first partition on a SATA or USB
    interface, part_path should be:

        /dev/sda1

    If the user's EFI partition is the 5th partition on the first NVMe drive on
    the first NVMe bus:

        /dev/nvme0n1p5

    etc...
    """
    # Get root drive
    root = get_drive_path(part_path)
    # get Device
    device = parted.getDevice(root)
    # get entire partition table
    disk = parted.Disk(device)
    # narrow down to just primary partitions
    partitions = disk.getPrimaryPartitions()
    # mark designated partition as bootable
    try:
        if "nvme" in part_path:
            partitions[int(part_path[part_path.index("p") + 1:])].setFlag(parted.PARTITION_BOOT)
        else:
            partitions[int(part_path[8:])].setFlag(parted.PARTITION_BOOT)
    except IndexError:
        return
    # We don't have commitment issues here!
    disk.commit()


def clobber_disk(device):
    """Reset drive"""
    common.eprint("DELETING PARTITIONS.")
    device.clobber()
    disk = parted.freshDisk(device, "gpt")
    disk.commit()
    return disk


def delete_part(part_path):
    """Delete partiton indicated by path"""
    device = parted.getDevice(get_drive_path(part_path))
    disk = parted.Disk(device)
    part = disk.getPartitionByPath(part_path)
    disk.deletePartition(part)
    disk.commit()


def partition(root, efi, home, raid_array):
    """Partition drive 'root' for Linux installation

root: needs to be path to installation drive (i.e.: /dev/sda, /dev/nvme0n1)
efi: booleen indicated whether system was booted with UEFI
home: whether to make a home partition, or if one already exists

Possible values:
  None, 'NULL':            Do not make a home partition, and one does not exist
  'MAKE':                  Make a home partition on the installation drive
  (some partition path):   path to a partition to be used as home directory
"""
    # Initial set up for partitioning
    common.eprint("\t###\tauto_partioner.py STARTED\t###\t")
    part1 = None
    part2 = None
    part3 = None
    if raid_array["raid_type"] not in (None, "OEM"):
        if raid_array["raid_type"].lower() == "raid0":
            raid_array["raid_type"] = 0
        elif raid_array["raid_type"].lower() == "raid1":
            raid_array["raid_type"] = 1
        elif raid_array["raid_type"].lower() == "raid10":
            raid_array["raid_type"] = 10
        for each in raid_array["disks"]:
            if each in ("1", "2"):
                if raid_array["disks"][each] is None:
                    # Invalid RAID array. Do not create.
                    raid_array["raid_type"] = None
    # We double check this to ensure we are working with valid RAID arrays
    if raid_array["raid_type"] is not None:
        disks = []
        for each in raid_array["disks"]:
            if raid_array["disks"][each] is not None:
                disks.append(raid_array["disks"][each])
        raid_array["disks"] = disks
    device = parted.getDevice(root)
    try:
        disk = parted.Disk(device)
    except parted._ped.DiskLabelException:
        common.eprint("NO PARTITION TABLE EXISTS. MAKING NEW ONE . . .")
        disk = parted.freshDisk(device, "gpt")
    # sectors_to_size() returns size in MBs, multiply by 1 million to convert to bytes
    size = sectors_to_size(device.length, device.sectorSize) * 1000000
    if ((home in ("NULL", "null",
                  None, "MAKE")) and (raid_array["raid_type"] is None)):
        disk = clobber_disk(device)
    elif raid_array["raid_type"] is not None:
        disk = clobber_disk(device)
        common.eprint("CREATING RAID ARRAY")
        common.eprint(f"RAID TYPE: {raid_array['raid_type']}")
        if not make_raid_array(raid_array["disks"], raid_array["raid_type"]):
            common.eprint("INITIAL RAID ARRAY CREATION FAILED. FORCING . . .")
            if not make_raid_array(raid_array["disks"], raid_array["raid_type"],
                                   force=True):
                common.eprint("FORCED RAID ARRAY CREATION FAILED. BAD DRIVE?")
                common.eprint("FALLING BACK TO NO HOME PARTITION.")
                home = None
    else:
        # we know there is a pre-existing home partition
        # determine if it is on the same drive and act accordingly
        home_drive = get_drive_path(home)
        if home_drive == root:
            common.eprint("HOME PARTITION EXISTS. NOT DELETING PARTITIONS.")
        else:
            disk = clobber_disk(device)
    if size <= LIMITER:
        if efi:
            part1 = __make_efi__(device)
            part2 = __make_root__(device, end="100%")
        else:
            part1 = __make_root__(device, start="0%", end="100%")
            __make_root_boot__(device)
        common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
        return __generate_return_data__(home, efi, part1, part2, part3)
    # Handled 16GB drives
    # From here until 64GB drives, we want our root partition to be AT LEAST
    # 16GB
    if home == "MAKE":
        # If home == "MAKE", we KNOW there are no partitons because we made a
        # new partition table
        if size >= gb_to_bytes(config["mdswh"]):
            root_end = int((size * 0.35) / (1000 ** 2))
        else:
            root_end = get_min_root_size()
        if (efi and (part1 is None)):
            part1 = __make_efi__(device)
            part2 = __make_root__(device, end=root_end)
            part3 = __make_home__(device, new_start=root_end)
        elif part1 is None:
            part1 = __make_root__(device, start="0%", end=root_end)
            __make_root_boot__(device)
            part2 = __make_home__(device, new_start=root_end)
        common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
        return __generate_return_data__(home, efi, part1, part2, part3)
    if home in ("NULL", "null", None):
        # If home == any possible 'null' value,
        # we KNOW there are no partitons because we made a
        # new partition table
        if efi:
            part1 = __make_efi__(device)
            part2 = __make_root__(device, end="100%")
        else:
            part1 = __make_root__(device, start="0%", end="100%")
            __make_root_boot__(device)
        common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
        return __generate_return_data__(home, efi, part1, part2, part3)
    # This one we need to figure out if the home partiton is on the drive
    # we are working on or elsewhere
    if root == get_drive_path(home):
        # It IS on the same drive. We need to figure out where at and work
        # around it
        # NOTE: WE NEED TO WORK IN MB ONLY IN THIS SECTION
        disk = parted.Disk(device)
        data = disk.getFreeSpaceRegions()
        sizes = {}
        for each in data:
            sizes[each.length] = each
        sizes_sorted = sorted(sizes)
        # Lets make some partitons!
        if efi:
            for each in sizes_sorted:
                if sizes[each].getSize() >= 200:
                    end = sizes[each].start + parted.sizeToSectors(200, "MB",
                                                                   device.sectorSize)
                    end = sectors_to_size(end, device.sectorSize)
                    part1 = __make_efi__(device, start=sizes[each].start,
                                         end=end)
                    part2 = __make_root__(device, start=end,
                                          end=sizes[each].end)
                    break
        else:
            for each in sizes_sorted:
                if sizes[each].getSize() >= 200:
                    part1 = __make_root__(device, start=sizes[each].start + 1,
                                          end=sizes[each].end - 1)
                    __make_root_boot__(device)
                    break
        common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
        return __generate_return_data__(home, efi, part1, part2, part3)
    # it's elsewhere. We're good.
    if efi:
        part1 = __make_efi__(device)
        part2 = __make_root__(device, end="100%")
    else:
        part1 = __make_root__(device, start="0%", end="100%")
        __make_root_boot__(device)
    part3 = home
    # Figure out what parts are for what
    # Return that data as a dictonary
    common.eprint("\t###\tauto_partioner.py CLOSED\t###\t")
    return __generate_return_data__(home, efi, part1, part2, part3)


def make_raid_array(disks: list, raid_type: int, force=False) -> bool:
    """Make BTRFS RAID Array
    Supported RAID Types:
        RAID0: Minimum 2 drives, max performance, no resiliancey
        RAID1: Minimum 2 drives, max resiliancey, minimum performance
        RAID5: 3-16 drives, poor resiliancey, great read performance, poor write performance
        RAID6: Minimum 4 drives. Medium resiliancey, great read performance, worse write performance
        RAID10: Minimum 4 drives, Medium resiliancey, Great performance

    raid_type should be an int indicating the RAID type desired so:
        raid_type == 0: use RAID0
        raid_type == 1: use RAID1
        etc.

    Any ints other than 0, 1, 5, 6, and 10 will throw a ValueError

    disks should be a list of the disks desired in the RAID array. A ValueError
    will be thrown if the list is too short or too long.

    Returns True if array was successfully completed. False otherwise.
    You can then mount the array by calling `mount' on any of the devices in the
    disks list.
    """
    raid_types_dict = {0: "raid0",
                       1: "raid1",
                       5: "raid5",
                       6: "raid6",
                       10: "raid10"}
    command = ["mkfs.btrfs", "-d"]
    if force:
        command.insert(1, "-f")
    if raid_type not in raid_types_dict:
        raise ValueError(f"'{raid_type}' not a valid BTRFS RAID type")
    if raid_type in (0, 1):
        if len(disks) < 2:
            raise ValueError(f"Not enough disks for RAID{raid_type}")
    elif raid_type == 5:
        if not 3 <= len(disks) <= 16:
            raise ValueError("Not enough/Too many disks for RAID5")
    elif raid_type in (6, 10):
        if len(disks) < 4:
            raise ValueError(f"Not enough disks for RAID{raid_type}")
    for each in disks:
        if not os.path.exists(each):
            raise FileNotFoundError(f"Device not found: {each}")
    command.append(raid_types_dict[raid_type])
    if raid_type not in (0, 5, 6):
        command.append("-m")
        command.append(raid_types_dict[raid_type])
    command = command + disks
    try:
        subprocess.check_call(command, stderr=sys.stderr.buffer,
                              stdout=sys.stderr.buffer)
        return True
    except subprocess.CalledProcessError:
        return False
