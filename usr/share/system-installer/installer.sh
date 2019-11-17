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
echo "	###	$0 STARTED	###	" 1>&2
echo "1"
#set -e
set -o pipefail
partitioner="$1"
LANG_SET="$2"
TIME_ZONE="$3"
USERNAME="$4"
COMP_NAME="$5"
PASS="$6"
EXTRAS="$7"
UPDATES="$8"
#SWAP="$11"
echo "3"
partitioner=$(echo "$partitioner" | sed 's/,/ /g' | sed 's/ROOT://' | sed 's/EFI://' | sed 's/HOME://' | sed 's/SWAP://')
ROOT=$(echo "$partitioner" | awk '{print $1}' | sed 's/:/ /g')
EFI=$(echo "$partitioner" | awk '{print $2}')
HOME_DATA=$(echo "$partitioner" | awk '{print $3}' | sed 's/:/ /g')
SWAP=$(echo "$partitioner" | awk '{print $4}')
#STEP 1: Partion and format the drive
# Don't worry about this right now. Taken care of earlier.
#if [ "$partitioner" == "auto" ]; then
	##use the autopartioner
	#MOUNT=$(/usr/share/system-installer/modules/auto-partitoner.sh "$EFI")
#else
	##use the config the user asked for to partion the drive
	#MOUNT=$(/usr/share/system-installer/modules/manual-partitoner.sh "$EFI" "$partitioner" "$TYPE")
#fi
set -Ee
echo "12"
#STEP 2: Mount the new partitions
mount "$(echo $ROOT | awk '{print $1}')" /mnt
if [ "$EFI" != "NULL" ]; then
	mkdir -p /mnt/boot/efi
	mount "$EFI" /mnt/boot/efi
fi
echo "$HOME_DATA" | grep -q "NULL" 1>/dev/null 2>/dev/null
TEST="$?"
if [ "$TEST" != "0" ]; then
	mkdir -p /mnt/home
	mount "$(echo "$HOME_DATA" | awk '{print $1}')" /mnt/home
fi
if [ "$SWAP" != "FILE" ]; then
	swapon "$SWAP"
else
	echo "SWAP FILE SUPPORT NOT IMPLEMENTED YET" 1>&2
fi
#if [ "$EFI" == "200" ]; then
	#if $(echo "$MOUNT" | grep -q "nvme"); then
		#mount "$MOUNT"p2 /mnt
		#if [ ! -d /mnt/boot/efi ]; then
			#mkdir /mnt/boot/efi
		#fi
		#mount "$MOUNT"p1 /mnt/boot/efi
	#else
		#mount "$MOUNT"2 /mnt
		#if [ ! -d /mnt/boot/efi ]; then
			#mkdir /mnt/boot/efi
		#fi
		#mount "$MOUNT"1 /mnt/boot/efi
	#fi
#else
	#if $(echo "$MOUNT" | grep -q "nvme"); then
		#mount "$MOUNT"p1 /mnt
	#else
		#mount "$MOUNT"1 /mnt
	#fi
#fi
echo "14"
#STEP 3: Unsquash the sqaushfs and get the files where they need to go
SQUASHFS=$(cat /etc/system-installer/default.config | sed 's/squashfs_Location=//')
if [ "$SQUASHFS" == "" ] || [ ! -f "$SQUASHFS" ]; then
	echo "SQUASHFS FILE DOES NOT EXIST" 1>&2
	/usr/share/system-installer/UI/error.py "SQUASHFS FILE DOES NOT EXIST"
	exit 2
fi
echo "17"
cd /mnt
{
	echo "CLEANING INSTALLATION DIRECTORY."
	#cleaning the long way in order to handle some bugs
	list=$(ls -A)
	for each in $list; do
		if [ "$each" != "boot" ]; then
			rm -rf "$each"
		else
			cd boot
			list2=$(ls -A)
			for each2 in $list2; do
				if [ "$each2" != "efi" ]; then
					rm -rf "$each2"
				else
					rm -rf efi/*
				fi
			done
			cd ..
		fi
	done
} 1>&2
echo "EXTRACTING SQUASHFS" 1>&2
unsquashfs "$SQUASHFS" 1>/dev/null
# While it would be faster to do something like:
#	mv squashfs-root/{.,}* ../
# This keeps throwing errors. So, we use this much more verbose, but easier to control, loop:
file_list=$(ls squashfs-root)
set +Ee
for each in $file_list; do
	mv -v /mnt/squashfs-root/$each /mnt/$each 1>&2
done
rm -rfv squashfs-root 1>&2
mkdir /mnt/boot 2>/dev/null || echo "/mnt/boot already created" 1>&2
cp -Rv /boot/* /mnt/boot 1>&2
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
UUID=$(blkid -s PARTUUID -o value $(echo $ROOT | awk '{print $1}'))	/	$(echo $ROOT | awk '{print $2}')	defaults	0	1" > /mnt/etc/fstab
if [ "$EFI" != "NULL" ]; then
	echo "UUID=$(blkid -s PARTUUID -o value $EFI)	/boot/efi	vfat	defaults	0	2" >> /mnt/etc/fstab
fi
if $(echo "$HOME_DATA" | grep -q "NULL"); then
	echo "UUID=$(blkid -s PARTUUID -o value $(echo $HOME_DATA | awk '{print $1}'))	/home	$(echo $HOME_DATA | awk '{print $2}')	defaults	0	3" >> /mnt/etc/fstab
fi
if [ "$SWAP" != "FILE" ]; then
	echo "UUID=$(blkid -s PARTUUID -o value $SWAP)	none	swap	sw	0	0" >> /mnt/etc/fstab
	# DO NOT PUT A HANDLER FOR SWAP FILES HERE
	# THIS IS DONE IN MASTER.sh
fi
chmod 644 /mnt/etc/fstab
echo "34"
#STEP 5: copy scripts into chroot
LIST=$(ls /usr/share/system-installer/modules)
LIST=$(echo "$LIST" | grep -v "partitoner")
for each in $LIST; do
	cp "/usr/share/system-installer/modules/$each" "/mnt/$each"
done
echo "35"
#STEP 6: Run Master script inside chroot
#don't run it as a background process so we know when it gets done
mv /mnt/etc/resolv.conf /mnt/etc/resolv.conf.save
cp /etc/resolv.conf /mnt/etc/resolv.conf
echo "36"
#Check to make sure all these vars are set
#if not, set them to some defaults
if [ "$LANG_SET" == "" ]; then
	echo "\$LANG_SET is not set. Defaulting to english" >>/tmp/system-installer.log
	LANG_SET="english"
fi
if [ "$TIME_ZONE" == "" ]; then
	echo "\$TIME_ZONE is not set. Defaulting to EST" >>/tmp/system-installer.log
	TIME_ZONE="EST"
fi
if [ "$USERNAME" == "" ]; then
	echo "\$USERNAME is not set. No default. Prompting user . . ." >>/tmp/system-installer.log
	USERNAME=$(zenity --entry --text="We're sorry. We lost your username somewhere in the chain. What was it again?")
fi
if [ "$COMP_NAME" == "" ]; then
	echo "\$COMP_NAME is not set. Defaulting to drauger-system-installed" >>/tmp/system-installer.log
	COMP_NAME="drauger-system-installed"
fi
if [ "$PASS" == "" ]; then
	echo "\$PASS is not set. No default. Prompting user . . ." >>/tmp/system-installer.log
	PASS=$(zenity --entry --hide-text --text="We're sorry. We lost your password somewhere in the chain. What was it again?")
fi
if [ "$EXTRAS" == "" ]; then
	echo "\$EXTRAS is not set. Defaulting to false." >>/tmp/system-installer.log
	EXTRAS=false
fi
if [ "$UPDATES" == "" ]; then
	echo "\$UPDATES is not set. Defaulting to false." >>/tmp/system-installer.log
	UPDATES=false
fi
# we don't check EFI or ROOT cause if they weren't set the script would have failed.
#cd /mnt
#mount --rbind /dev dev/
#mount --rbind /sys sys/
#mount -t proc proc proc/
arch-chroot /mnt '/MASTER.sh' "$LANG_SET" "$TIME_ZONE" "$USERNAME" "$COMP_NAME" "$PASS" "$EXTRAS" "$UPDATES" "$EFI" $(echo "$ROOT" | awk '{print $1}') 2>>/tmp/system-installer.log
#umount dev/ || echo "Unable to unmount dev. Continuing . . ." 1>>/tmp/system-installer.log
#umount sys/ || echo "Unable to unmount sys. Continuing . . ." 1>>/tmp/system-installer.log
#umount proc/ || echo "Unable to unmount proc. Continuing . . ." 1>>/tmp/system-installer.log
#STEP 7: Clean up
#I know this isn't the best way of doing this, but it is easier than changing each of the file name in $LIST
echo "Removing installation scripts and resetting resolv.conf" 1>&2
for each in $LIST; do
	rm -v "/mnt/$each"
done
echo "89"
rm -v /mnt/etc/resolv.conf
mv -v /mnt/etc/resolv.conf.save /mnt/etc/resolv.conf
echo "100"
echo "	###	$0 CLOSED	###	" 1>&2
