#!/bin/bash
# -*- coding: utf-8 -*-
#
#  installer.sh
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
#this file handles most of the installation process
set -e
set -o pipefail
EFI="$1"
partitioner="$2"
LANG="$3"
TIME_ZONE="$4"
USERNAME="$5"
COMPNAME="$6"
PASS="$7"
EXTRAS="$8"
UPDATES="$9"
#STEP 1: Partion and format the drive
if [ "$partioner" == "auto" ]; then
	#use the autopartioner
	/usr/share/system-installer/modules/auto-partitioner.sh "$EFI"
else
	#use the config the user asked for to partion the drive
	/usr/share/system-installer/modules/manual-partitioner.sh "$EFI" "$partitioner"
fi
#STEP 2: Unsquash the sqaushfs and get the files where they need to go
SQUASHFS=$(cat /etc/system-installer/default.config | sed 's/squashfs_Location=//')
if [ ! -f "$SQUASHFs" ]; then
	echo "SQUASHFS FILE DOES NOT EXIST"
	/usr/share/system-installer/UI/error.py "SQUASHFS FILE DOES NOT EXIST"
	exit 2
fi
