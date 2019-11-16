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
set -o pipefail
LANG_SET="$1"
TIME_ZONE="$2"
USERNAME="$3"
COMP_NAME="$4"
PASS="$5"
EXTRAS="$6"
UPDATES="$7"
EFI="$8"
ROOT="$9"
echo "39"
#STEP 1: Check for internet
function check_internet ()
{
	case "$(curl -s --max-time 2 -I https://draugeros.org | sed 's/^[^ ]*  *\([0-9]\).*/\1/; 1q')" in
		[23]) echo "0";;
		5) echo "1";;
		*) echo "1";;
	esac
}

internet=$(check_internet)
#STEP 1: Set the time
. /set_time.sh "$TIME_ZONE"
echo "42"
#STEP 2: Generate locales
. /set_locale.sh "$LANG_SET"
echo "47"
#STEP 3: Set Computer name
echo "Setting hostname to \"$COMP_NAME\"" 1>&2
echo "$COMP_NAME" > /etc/hostname
echo "127.0.1.1	$COMP_NAME" >> /etc/hosts
echo "48"
#STEP 4: Make user account
. /make_user.sh "$USERNAME" "$PASS"
echo "56"
#STEP 5: Make swap file
if [ "$SWAP" == "FILE" ]; then
	{
		. /make-swap.sh
		echo "/.swapfile	swap	swap	defaults	0	0" >> /etc/fstab
	} || { 
		echo "Adding swap failed. Must manually add later" 1>&2
	}
fi
echo "66"
#STEP 6: install updates
if [ "$UPDATES" == "1" ] && [ "$internet" == "0" ]; then
	. /install_updates.sh
elif [ "$internet" == "1" ]; then
	echo "Cannot install updates. No internet." 1>&2
fi
echo "75"
#STEP 7: install extras
if [ "$EXTRAS" == "1" ] && [ "$internet" == "0" ]; then
	. /install_extras.sh
elif [ "$internet" == "1" ]; then
	echo "Cannot install extras. No internet." 1>&2
fi
echo "84"
#STEP 8: Set new root password
echo "root:$PASS" | chpasswd
echo "85"
#STEP 9: Kernel, Plymouth, Initramfs
echo "DOING SOME QUICK CLEAN UP BEFORE SETTING UP INITRAMFS AND GRUB" 1>&2
update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/drauger-theme/drauger-theme.plymouth 100 --slave /usr/share/plymouth/themes/default.grub default.plymouth.grub /usr/share/plymouth/themes/drauger-theme/drauger-theme.grub
echo -e "2\n" | update-alternatives --config default.plymouth
echo "86"
{
	if [ "$internet" == "0" ]; then
		install=$(apt-cache depends linux-headers-drauger linux-image-drauger | grep '[ |]Depends: [^<]' | cut -d: -f2 | tr -d ' ')
		apt install -y --reinstall linux-headers-drauger linux-image-drauger $install
	else
		7z x kernel.7z
		apt purge -y linux-headers-drauger linux-image-drauger
		apt autoremove -y
		apt purge $(dpkg -l | grep '^rc' | awk '{print $2}')
		#dpkg installs packages whether it's already installed or not. So we don't need some sort of --reinstall flag
		#that's an apt thing, I'd assume. For security and stability.
		dpkg -R --install -y kernel/
		rm -rf kernel
	fi
	apt purge -y system-installer
	apt autoremove -y
	apt clean
	#mkinitramfs -o /boot/initrd.img-$(uname --release)
} 1>&2
echo "87"
#STEP 10: Bootloader
{
	
	mkinitramfs -o /boot/initrd.img-$(uname --release)
	if [ "$EFI" != "NULL" ]; then
		#grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id="Drauger OS" "$(echo $EFI | sed 's/[0-9]//')"
		#systemd-boot
		if [ -d /sys/firmware/efi/efivars ]; then
			mkdir -p /boot/efi/loader/entries /boot/efi/Drauger_OS
			export SYSTEMD_RELAX_ESP_CHECKS=1
			echo "export SYSTEMD_RELAX_ESP_CHECKS=1" >> /etc/environment
			bootctl --path=/boot/efi install
			echo -e "default Drauger_OS\ntimeout 5\neditor 0" > /boot/efi/loader/loader.conf
			chattr -i /boot/efi/loader/loader.conf
			#set up kernel version hook
			. /systemd-boot-config.sh "$ROOT"
			cp /boot/vmlinuz-$(uname --release) /boot/efi/vmlinuz
			cp /boot/initrd.img-$(uname --release) /boot/efi/initrd.img
			
		else
			echo "### WARNING: CANNOT INSTALL systemd-boot. USER MUST MANUALLY INSTALL BOOTLOADER. ###"
		fi
	else
		grub-mkdevicemap
		grub-install --force --target=i386-pc "$ROOT"
		grub-mkconfig -o /boot/grub/grub.cfg
	fi
	sleep 1s
	ln /boot/initrd.img-$(uname --release) /boot/initrd.img
	ln /boot/vmlinuz-$(uname --release) /boot/vmlinuz
} 1>&2
echo "88"
echo "	###	$0 CLOSED	###	" 1>&2


