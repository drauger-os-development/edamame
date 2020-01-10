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
echo "	###	auto-partioner.sh STARTED	###	" 1>&2
set -e
set -o pipefail
INSTALL_DISK="$1"
EFI="$2"
SIZE=$(lsblk | grep $(echo "$INSTALL_DISK" | sed 's:/dev/::g') | grep 'disk' | awk '{print $4}')
echo " ### WARNING: DD-ING DRIVE. NO DATA WILL BE RECOVERABLE. ### " 1>&2
dd if=/dev/zero of="$INSTALL_DISK" count=1 bs=512 1>&2
if $(echo "$INSTALL_DISK" | grep -q "nvme"); then
	PART1="$INSTALL_DISK"p1
	PART2="$INSTALL_DISK"p2
else
	PART1="$INSTALL_DISK"1
	PART2="$INSTALL_DISK"2
fi
if [ "$EFI" == "True" ]; then
	parted --script "$INSTALL_DISK" mktable gpt mkpart primary fat32 1M 201M mkpart primary ext4 201M "$SIZE" 1>&2
	mkfs.fat -F 32 "$PART1" 1>&2
	mkfs.ext4 "$PART2" 1>&2
	echo "EFI:$PART1 ROOT:$PART2"
else
	parted --script "$INSTALL_DISK" mktabel gpt mkpart primary ext4 1M "$SIZE" 1>&2
	mkfs.ext4 "$PART1" 1>&2
	echo "EFI:NULL ROOT:$PART1"
fi
partprobe
echo "	###	auto-partioner.sh CLOSED	###	" 1>&2
