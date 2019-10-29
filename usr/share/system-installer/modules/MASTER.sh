#!/bin/bash
# -*- coding: utf-8 -*-
#
#  MASTER.sh
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
#This file handles most of the installation INSIDE the chroot
echo "	###	$0 STARTED	###	" 1>&2
echo "37"
#set -e
#set -o pipefail
LANG_SET="$1"
TIME_ZONE="$2"
USERNAME="$3"
COMP_NAME="$4"
PASS="$5"
EXTRAS="$6"
UPDATES="$7"
EFI="$8"
ROOT="$9"
#Variable Verification
echo "LANG_SET = $LANG_SET
TIME_ZONE = $TIME_ZONE
USERNAME = $USERNAME
COMP_NAME = $COMP_NAME
PASS = $PASS
EXTRAS = $EXTRAS
UPDATES = $UPDATES
EFI = $EFI
ROOT = $ROOT" 1>&2
echo "39"
#STEP 1: Set the time
. /set_time.sh "$TIME_ZONE"
echo "42"
#STEP 2: Generate locales
. /set_locale.sh "$LANG_SET"
echo "47"
#STEP 3: Set Computer name
echo "Setting hostname to \"$COMP_NAME\"" 1>&2
hostnamectl set-hostname "$COMP_NAME"
echo "48"
#STEP 4: Make user account
. /make_user.sh "$USERNAME" "$PASS"
echo "56"
#STEP 5: Make swap file
#if [ "$SWAP" == "FILE" ]; then
#	{
#		. /make-swap.sh
#		echo "/.swapfile	swap	swap	defaults	0	0" >> /etc/fstab
#	} || { 
#		echo "Adding swap failed. Must manually add later" 1>&2
#	}
#fi
#echo "64"

echo "66"
#STEP 6: install updates
if [ "$UPDATES" == "1" ]; then
	. /install_updates.sh
fi
echo "75"
#STEP 7: install extras
if [ "$EXTRAS" == "1" ]; then
	. /install_extras.sh
fi
echo "84"
#STEP 8: Set new root password
echo "root:$PASS" | chpasswd
echo "85"
#STEP 9: Initramfs
echo "DOING SOME QUICK CLEAN UP BEFORE SETTING UP INITRAMFS AND GRUB" 1>&2
apt-cache depends linux-headers-drauger linux-image-drauger | grep '[ |]Depends: [^<]' | cut -d: -f2 | tr -d ' ' | xargs apt install --reinstall -y 2>/dev/null 1>>/tmp/system-installer.log
apt purge -y system-installer 2>/dev/null 1>>/tmp/system-installer.log
apt -y autoremove 2>/dev/null 1>>/tmp/system-installer.log
apt clean 2>/dev/null 1>>/tmp/system-installer.log
mkinitramfs -o /boot/initrd.img-$(uname --release) 2>/dev/null 1>>/tmp/system-installer.log
echo "87"
#STEP 10: GRUB
if [ "$EFI" != "NULL" ]; then
	grub-install --force --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id="Drauger OS" 1>>/tmp/system-installer.log
	echo "88"
else
	grub-install --force --target=i386-pc "$ROOT" 1>>/tmp/system-installer.log
	echo "88"
fi
echo "	###	$0 CLOSED	###	" 1>&2


