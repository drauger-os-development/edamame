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
if $(echo "$INSTALL_DISK" | grep -q "nvme"); then
	PART1="$INSTALL_DISK"p1
	PART2="$INSTALL_DISK"p2
else
	PART1="$INSTALL_DISK"1
	PART2="$INSTALL_DISK"2
fi
if [ "$EFI" == "True" ]; then
	fdisk "$INSTALL_DISK" << EOF
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
	mkfs.fat -F 32 -l "UEFI" "$PART1"
	mkfs.ext4 -L "ROOT" "$PART2"
else
	fdisk "$INSTALL_DISK" << EOF
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
	mkfs.ext4 -L "ROOT" "$PART1"
fi
echo "	###	auto-partioner.sh CLOSED	###	" 1>&2
