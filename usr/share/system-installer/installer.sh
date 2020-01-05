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
SETTINGS="$1"
echo "3"
echo "$SETTINGS" | sed 's/ , /:/g' | mapfile -d ":" SETTINGS
ROOT=${SETTINGS[0]}
EFI=${SETTINGS[1]}
HOME_DATA=${SETTINGS[2]}
SWAP=${SETTINGS[3]}
LANG_SET=${SETTINGS[4]}
TIME_ZONE=${SETTINGS[5]}
USERNAME=${SETTINGS[6]}
COMP_NAME=${SETTINGS[7]}
PASS=${SETTINGS[8]}
EXTRAS=${SETTINGS[9]}
UPDATES=${SETTINGS[10]}
LOGIN=${SETTINGS[11]}
MODEL=${SETTINGS[12]}
LAYOUT=${SETTINGS[13]}
VARIENT=${SETTINGS[14]}
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
set -o pipefail
echo "12"
#STEP 2: Mount the new partitions
mount "$ROOT" /mnt
if [ "$EFI" != "NULL" ]; then
	mkdir -p /mnt/boot/efi
	mount "$EFI" /mnt/boot/efi
fi
echo "$HOME_DATA" | grep -q "NULL" 1>/dev/null 2>/dev/null
TEST="$?"
if [ "$TEST" != "0" ]; then
	mkdir -p /mnt/home
	mount "$HOME_DATA" /mnt/home
fi
if [ "$SWAP" != "FILE" ]; then
	swapon "$SWAP"
else
	echo "SWAP FILE NOT CREATED YET" 1>&2
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
genfstab -U /mnt > /mnt/etc/fstab
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
	echo "\$LANG_SET is not set. Defaulting to english" 1>&2
	LANG_SET="english"
fi
if [ "$TIME_ZONE" == "" ]; then
	echo "\$TIME_ZONE is not set. Defaulting to EST" 1>&2
	TIME_ZONE="EST"
fi
if [ "$USERNAME" == "" ]; then
	echo "\$USERNAME is not set. No default. Prompting user . . ." 1>&2
	USERNAME=$(zenity --entry --text="We're sorry. We lost your username somewhere in the chain. What was it again?")
fi
if [ "$COMP_NAME" == "" ]; then
	echo "\$COMP_NAME is not set. Defaulting to drauger-system-installed" 1>&2
	COMP_NAME="drauger-system-installed"
fi
if [ "$PASS" == "" ]; then
	echo "\$PASS is not set. No default. Prompting user . . ." 1>&2
	PASS=$(zenity --entry --hide-text --text="We're sorry. We lost your password somewhere in the chain. What was it again?")
fi
if [ "$EXTRAS" == "" ]; then
	echo "\$EXTRAS is not set. Defaulting to false." 1>&2
	EXTRAS=false
fi
if [ "$UPDATES" == "" ]; then
	echo "\$UPDATES is not set. Defaulting to false." 1>&2
	UPDATES=false
fi
# we don't check EFI or ROOT cause if they weren't set the script would have failed.
#cd /mnt
#mount --rbind /dev dev/
#mount --rbind /sys sys/
#mount -t proc proc proc/
arch-chroot /mnt '/MASTER.sh' "$LANG_SET , $TIME_ZONE , $USERNAME , $PASS , $COMP_NAME , $EXTRAS , $UPDATES , $EFI , $ROOT , $LOGIN , $MODEL , $LAYOUT , $VARIENT" 1>&2
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
echo "98"
#check to make sure systemd-boot got configured
contents=$(ls /mnt/boot/efi/loader/entries)
if [ "$contents" == "" ]; then
	echo "	### SYSTEMD-BOOT NOT CONFIGURED. CORRECTING . . .	###	" 1>&2
	cp /usr/share/system-installer/modules/systemd-boot-config.sh /mnt
	arch-chroot /mnt '/systemd-boot-config.sh' "$ROOT" 1>&2
	rm /mnt/systemd-boot-config.sh
fi
rm -rf /mnt/home/$USERNAME/.config/xfce4/panel/launcher-20
echo "100"
echo "	###	$0 CLOSED	###	" 1>&2
