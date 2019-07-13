#!/bin/bash
# -*- coding: utf-8 -*-
#
#  auto-partioner.sh
#
#  Copyright 2019 Thomas Castleman <contact@draugeros.org>
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
set -e
EFI="$1"
disks=$(lsblk -o name,type,label | grep "disk" | grep -v "Drauger OS" | awk '{print $1}')
if $(echo "$disks" | grep -q "nvme0n*"); then
	DISK="nvme0n1"
	DISK1="nvme0n1p1"
	DISK2="nvme0n1p2"
elif $(echo "$disks" | grep -q "sd"); then
	disks=$(echo "$disks" | grep "sd")
	set -- $disks
	disks="$1"
	DISK="$disks"
	DISK1="$disks"1
	DISK2="$disks"2
else
	echo "No partitonable disks detected" 1>&2
	/usr/share/system-installer/UI/error.py "No partitionable disks detected" 2
	exit 2
fi
if [ "$EFI" == "200" ]; then
	fdisk "/dev/$DISK" << EOF
	o
	n
	p
	1

	+200M
	n
	p
	2


	a
	1
	p
	w
	q
	EOF
	mkfs.fat -F 32 -l "UEFI" /dev/"$DISK1"
	mkfs.ext4 -L "ROOT" /dev/"$DISK2"
else
	fdisk "/dev/$DISK" << EOF
	o
	n
	p
	1
	
	
	a
	1
	p
	w
	q
	EOF
	mkfs.ext4 -L "ROOT" /dev/"$DISK1"
fi
echo "/dev/$DISK"
