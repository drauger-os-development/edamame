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
set -e
set -o pipefail
LANG="$1"
TIME_ZONE="$2"
USERNAME="$3"
COMP_NAME="$4"
PASS="$5"
EXTRAS="$6"
UPDATES="$7"
SWAP="$8"
EFI="$9"
#STEP 1: Set the time
. /set_time.sh "$TIME_ZONE"
#STEP 2: Generate locales
. /set_locale.sh "$LANG"
#STEP 3: Set Computer name
hostnamectl set-hostname "$COMP_NAME"
#STEP 4: Make user account
. /make_user.sh "$USERNAME" "$PASS"
#STEP 5: Make swap file
. /make-swap.sh $SWAP
echo "/.swapfile	swap	swap	defaults	0	0" >> /etc/fstab || echo "Adding swap failed. Must manually add later" 1>&2
#STEP 6: install updates
if $UPDATES; then
	. /install_updates.sh
fi
#STEP 7: install extras
if $EXTRAS; then
	. /install_extras.sh
fi
#STEP 8: Set new root password
echo "root:$PASS" | chpasswd
#STEP 9: Initramfs
update-initramfs -u
#STEP 10: GRUB
if [ "$EFI" == 200 ]; then
	grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id="Drauger OS"
else
	if $(echo "$MOUNT" | grep -q "nvme"); then
		grub-install --target=i386-pc "$MOUNT"p1
	else
		grub-install --target=i386-pc "$MOUNT"1
	fi
fi

