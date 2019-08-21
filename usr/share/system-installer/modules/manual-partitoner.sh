#!/bin/bash
# -*- coding: utf-8 -*-
#
#  manual-partitioner.sh
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
#
#
# This monstrosity of code barely works. Only fuck with it if you know
# what you are doing. If you have no idea, don't do it.
# Thou hath been warned.
EFI="$1"
partitioner="$2"
TYPE="$3"
if [ "$TYPE" == "NVMe" ]; then
	if [ "$EFI" == "200" ]; then
		fdisk "/dev/nvme0n1" << EOF
o
n
p
1

+"$EFI"M
n
p
2

+"$partitioner"G
a
1
p
w
q
EOF
		mkfs.fat -F 32 -l "UEFI" /dev/nvme0n1p1
		mkfs.ext4 -L "ROOT" /dev/nvme0n1p2
	elif [ "$EFI" == "-1" ]; then
		fdisk "/dev/nvme0n1" << EOF
o
n
p
1

+"$partitioner"G
a
1
p
w
q
EOF
		mkfs.ext4 -L "ROOT" /dev/nvme0n1p1
	else
		echo "Unknown Error: Improper EFI Detection" 1>&2
		/usr/share/system-installer/UI/error.py "Unknown Error: Improper EFI Detection"
		exit 2
	fi
	echo "/dev/nvme0n1"
elif [ "$TYPE" == "sd" ]; then
	LIST=$(lsblk -o name,type,label,size | grep "disk" | grep -v "Drauger OS")
	count=0
	for each in $LIST; do
		(( count+=1 ))
	done
	if [[ $count -gt 1 ]]; then
		coloumn=$(echo "$LIST" | awk '{print NF}')
		coloumn=$(echo "${coloumn[*]}" | sort -nr | head -n1)
		LIST_SIZES=$(echo "$LIST" | awk "{print \$$coloumn}" | sed 's/G//g')
		LIST_SIZES=$(echo "${LIST_SIZES[*]}" | sort -nr | head -n1)
		LIST=$(lsblk -o name,type,label,size | grep "disk" | grep -v "Drauger OS" | grep "$LIST_SIZES" | awk '{print $1}')
		count=0
		for each in $LIST; do
			(( count+=1 ))
		done
		if [[ $count -gt 1 ]]; then
			LIST=$(echo "$LIST" | tr '\n' '|')
			LIST=$(zenity --forms --add-list="Drives:" --list-values="$LIST" --text="An error was detected. Please manually select the installation drive.")
		fi
	fi
	LIST=$(echo "$LIST" | awk '{print $1}')
	if [ "$EFI" == "200" ]; then
		fdisk "/dev/$LIST" << EOF
o
n
p
1

+"$EFI"M
n
p
2

+"$partitioner"G
a
1
p
w
q
EOF
		mkfs.fat -F 32 -l "UEFI" /dev/"$LIST"1
		mkfs.ext4 -L "ROOT" /dev/"$LIST"2
	elif [ "$EFI" == "-1" ]; then
		fdisk "/dev/$LIST" << EOF
o
n
p
1

+"$partitioner"G
a
1
p
w
q
EOF
		mkfs.ext4 -L "ROOT" /dev/"$LIST"1
	else
		echo "Unknown Error: Improper EFI Detection" 1>&2
		/usr/share/system-installer/UI/error.py "Unknown Error: Improper EFI Detection"
		exit 2
	fi
	echo "/dev/$LIST"
fi
