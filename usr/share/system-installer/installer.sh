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
#this file handles most of the installation process OUTSIDE the chroot
echo "1"
set -e
set -o pipefail
EFI="$1"
partitioner="$2"
TYPE="$3"
LANG="$4"
TIME_ZONE="$5"
USERNAME="$6"
COMPNAME="$7"
PASS="$8"
EXTRAS="$9"
UPDATES="$10"
SWAP="$11"
#STEP 1: Partion and format the drive
echo "3"
if [ "$partioner" == "auto" ]; then
	#use the autopartioner
	MOUNT=$(/usr/share/system-installer/modules/auto-partitoner.sh "$EFI")
else
	#use the config the user asked for to partion the drive
	MOUNT=$(/usr/share/system-installer/modules/manual-partitoner.sh "$EFI" "$partitioner" "$TYPE")
fi
echo "12"
#STEP 2: Mount the new partitions
if [ "$EFI" == "200" ]; then
	if $(echo "$MOUNT" | grep -q "nvme"); then
		mount "$MOUNT"p2 /mnt
		if [ ! -d /mnt/boot/efi ]; then
			mkdir /mnt/boot/efi
		fi
		mount "$MOUNT"p1 /mnt/boot/efi
	else
		mount "$MOUNT"2 /mnt
		if [ ! -d /mnt/boot/efi ]; then
			mkdir /mnt/boot/efi
		fi
		mount "$MOUNT"1 /mnt/boot/efi
	fi
else
	if $(echo "$MOUNT" | grep -q "nvme"); then
		mount "$MOUNT"p1 /mnt
	else
		mount "$MOUNT"1 /mnt
	fi
fi
echo "14"
#STEP 3: Unsquash the sqaushfs and get the files where they need to go
SQUASHFS=$(cat /etc/system-installer/default.config | sed 's/squashfs_Location=//')
if [ ! -f "$SQUASHFs" ]; then
	echo "SQUASHFS FILE DOES NOT EXIST" 1>&2
	/usr/share/system-installer/UI/error.py "SQUASHFS FILE DOES NOT EXIST"
	exit 2
fi
echo "17"
unsquashfs "$SQUASHFS" -d /mnt
echo "32"
#STEP 4: Update fstab
rm /mnt/etc/fstab
touch /mnt/etc/fstab
echo "# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system>	<mount point>	<type>	<options>	<dump>	<pass>
LABEL=ROOT	/	ext4	defaults	0	1" > /mnt/etc/fstab
if [ "$EFI" == "200" ]; then
	echo "LABEL=URFI	/boot/efi	defaults	0	2" >> /mnt/etc/fstab
fi
chmod 644 /mnt/etc/fstab
echo "34"
#STEP 5: copy scripts into chroot
LIST=$(ls /usr/share/system-installer/modules)
LIST=$(echo $LIST | grep -v "partitoner")
for each in $LIST; do
	cp "/usr/share/system-installer/modules/$each" "/mnt/$each"
done
echo "35"
#STEP 6: Run Master script inside chroot
#don' run it as a background process so we know when it gets done
mv /mnt/etc/resolv.conf /mnt/resolv.conf.save
cp /etc/resolv.conf /mnt/etc/resolv.conf
echo "36"
chroot /mnt '/MASTER.sh' "$LANG $TIME_ZONE $USERNAME $COMP_NAME $PASS $EXTRAS $UPDATES $SWAP $EFI $MOUNT" 2>/tmp/system-installer.log
#STEP 7: Clean up
#I know this isn't the best way of doing this, but it is easier than changing each of the file name in $LIST
for each in $LIST; do
	rm "/mnt/$each"
done
echo "89"
rm /mnt/etc/resolv.conf
mv /mnt/etc/resolv.conf.save /mnt/etc/resolv.conf
echo "100"
