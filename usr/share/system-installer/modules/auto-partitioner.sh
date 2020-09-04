#!/bin/bash
# -*- coding: utf-8 -*-
#
#  auto-partioner.sh
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
{
    builtin echo -e "\t###\tauto-partioner.sh STARTED\t###\t"
    set -e
    set -o pipefail
    INSTALL_DISK="$1"
    EFI="$2"
    HOME_DATA="$3"
    if $(builtin echo "$INSTALL_DISK" | grep -q "nvme"); then
        PART1="$INSTALL_DISK"p1
        PART2="$INSTALL_DISK"p2
        PART3="$INSTALL_DISK"p3
    else
        PART1="$INSTALL_DISK"1
        PART2="$INSTALL_DISK"2
        PART3="$INSTALL_DISK"3
    fi
    builtin echo "MAKING NEW PARTITION TABLE."
    if [ "$EFI" == "True" ] || [ "$EFI" == "TRUE" ]; then
        parted --script "$INSTALL_DISK" mktable gpt
    else
        parted --script "$INSTALL_DISK" mktable msdos
    fi
    if [ "$EFI" == "True" ] || [ "$EFI" == "TRUE" ]; then
        # we need 2 partitions: /boot/efi and /
        # we make /boot/efi first, then /
        if [[ "$HOME_DATA" == "MAKE" ]]; then
            #Make home partition
            parted --script "$INSTALL_DISK" mktable gpt mkpart primary fat32 0% 200M
            parted --script "$INSTALL_DISK" mkpart primary ext4 201M 30%
            parted --script "$INSTALL_DISK" mkpart primary ext4 30% 100%
        else
            #don't make one. Reset $PART3
            parted --script "$INSTALL_DISK" mkpart primary fat32 0% 200M
            parted --script "$INSTALL_DISK" mkpart primary ext4 201M 100%
            PART3="$HOME_DATA"
        fi
        sleep 1s
        set +e
        sfdisk --reorder "$INSTALL_DISK"
        builtin echo "PARTITION NUMBERING MODIFIED. CHECK FSTAB OF OTHER INSTALLED OSs TO ENSURE THEY WILL STILL WORK."
        parted --script "$INSTALL_DISK" set 1 boot on
        # apply FS on both, use "builtin echo -e "y\n"" piped into mkfs.fat and mkfs.ext4 to force it to make the FS
        builtin echo -e "y\n" | mkfs.fat -F 32 "$PART1"
        builtin echo -e "y\n" | mkfs.ext4 "$PART2"
        # if we have a home partition, set the FS on it too
        if [[ "$HOME_DATA" == "MAKE" ]]; then
            builtin echo -e "y\n" | mkfs.ext4 "$PART3"
        fi
    else
        #only need one partition cause we are using BIOS
        if [[ "$HOME_DATA" == "MAKE" ]]; then
            #Make home partition
            parted --script "$INSTALL_DISK" mktabel msdos mkpart primary ext4 0% 30%
            parted --script "$INSTALL_DISK" mkpart primary ext4 30% 100%

        else
            #don't make one. Reset $PART3
            parted --script "$INSTALL_DISK" mkpart primary ext4 0% 100%
            PART3="$HOME_DATA"
        fi
        sleep 1s
        set +e
        sfdisk --reorder "$INSTALL_DISK"
        builtin echo "PARTITION NUMBERING MODIFIED. CHECK FSTAB OF OTHER INSTALLED OSs TO ENSURE THEY WILL STILL WORK."
        parted --script "$INSTALL_DISK" set 1 boot on
        builtin echo -e "y\n" | mkfs.ext4 "$PART1"
    fi
    partprobe
    builtin echo -e "\t###\tauto-partioner.sh CLOSED\t###\t"
} 1>&2
if [ "$EFI" == "True" ] || [ "$EFI" == "TRUE" ]; then
    builtin echo "{\"EFI\":\"$PART1\", \"ROOT\":\"$PART2\", \"HOME\":\"$PART3\"}"
else
    builtin echo "{\"EFI\":\"NULL\", \"ROOT\":\"$PART1\", \"HOME\":\"$PART3\"}"
fi
