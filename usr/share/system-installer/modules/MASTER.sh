#!/bin/bash
# -*- coding: utf-8 -*-
#
#  MASTER.sh
#
#  Copyright 2020 Thomas Castleman <contact@draugeros.org>
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
SETTINGS="$1"
SETTINGS=$(echo "$SETTINGS" | sed 's/ , /:/g')
IFS=":"
SETTINGS=($SETTINGS)
IFS="$GLOBAL_IFS"
LANG_SET=${SETTINGS[0]}
TIME_ZONE=${SETTINGS[1]}
USERNAME=${SETTINGS[2]}
PASSWORD=${SETTINGS[3]}
COMP_NAME=${SETTINGS[4]}
EXTRAS=${SETTINGS[5]}
UPDATES=${SETTINGS[6]}
EFI=${SETTINGS[7]}
ROOT=${SETTINGS[8]}
LOGIN=${SETTINGS[9]}
MODEL=${SETTINGS[10]}
LAYOUT=${SETTINGS[11]}
VARIENT=${SETTINGS[12]}
echo "39"
#STEP 0: Export global variables
# this will be useful as system-installer becomes more modular
export LANG_SET="$LANG_SET"
export TIME_ZONE="$TIME_ZONE"
export USERNAME="$USERNAME"
# I would love to encrypt this somehow, but the program would have to auto-decrypt this for any hackers so we kinda screwed for  now
export PASSWORD="$PASSWORD"
export COMP_NAME="$COMP_NAME"
export EXTRAS="$EXTRAS"
export UPDATES="$UPDATES"
export EFI="$EFI"
export ROOT="$ROOT"
export LOGIN="$LOGIN"
export MODEL="$MODEL"
export LAYOUT="$LAYOUT"
export VARIENT="$VARIENT"
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
python3 /set_time.py "$TIME_ZONE" 1>&2
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
. /make_user.sh
echo "56"
#STEP 5: Make swap file
if [ "$SWAP" == "FILE" ]; then
	{
		python3 /make_swap.py
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
echo "root:$PASSWORD" | chpasswd
echo "85"
#STEP 9: Set auto-login
if [ "$LOGIN" == "0" ]; then
	python3 /auto_login_off.py 1>&2
fi
#STEP 10: Kernel, Plymouth, Initramfs
echo "DOING SOME QUICK CLEAN UP BEFORE SETTING UP INITRAMFS AND GRUB" 1>&2
update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/drauger-theme/drauger-theme.plymouth 100 --slave /usr/share/plymouth/themes/default.grub default.plymouth.grub /usr/share/plymouth/themes/drauger-theme/drauger-theme.grub 1>&2
echo -e "2\n" | update-alternatives --config default.plymouth 1>&2
echo "86"
remove=""
if [ "$EFI" != "NULL" ]; then
	remove=$(dpkg -l grub* | grep '^ii' | awk '{print $2}')
fi
{
	if [ "$internet" == "0" ]; then
		# if the online method fails, attempt the offline method
		apt update
		{
			install=$(apt-cache depends linux-headers-drauger linux-image-drauger | grep '[ |]Depends: [^<]' | cut -d: -f2 | tr -d ' ')
			apt install -y --reinstall linux-headers-drauger linux-image-drauger $install
		} || {
			7z x kernel.7z
			apt purge -y linux-headers-drauger linux-image-drauger
			apt autoremove -y --purge
			#dpkg installs packages whether it's already installed or not. So we don't need some sort of --reinstall flag
			#that's an apt thing, I'd assume. For security and stability.
			dpkg -R --install kernel/
			rm -rf kernel
		}
	else
		7z x kernel.7z
		apt purge -y linux-headers-drauger linux-image-drauger
		apt autoremove -y --purge
		#dpkg installs packages whether it's already installed or not. So we don't need some sort of --reinstall flag
		#that's an apt thing, I'd assume. For security and stability.
		dpkg -R --install kernel/
		rm -rf kernel
	fi
	# I am not happy about the way this works, but in order to work around some security changes in apt version 1.9.10, we have to do this
	# purge system-installer itself
	apt purge -y system-installer
	# check to see if we need to remove GRUB.
	# The list of packages we need to remove was set earlier
	if [ "$remove" != "" ]; then
		# iterate over $remove and remove each package.
		# This is WAY more verbose than I like but it should work
		for each in $remove; do
			apt purge -y $each
		done
	fi
	apt autoremove -y --purge
	apt clean
} 1>&2
echo "89"
#STEP 11: KEYBOARD
# God fucking damn it humanity. Why are there so many keyboard layouts?
# I hope I only REALLY need to support one of these for each major language
KEYBOARD_CONFIG_DATA=$(</usr/share/X11/xkb/rules/base.lst)
rm /etc/default/keyboard 1>&2
XKBMODEL=$(echo "$KEYBOARD_CONFIG_DATA" | grep "$MODEL" | awk '{print $1}')
XKBLAYOUT=$(echo "$KEYBOARD_CONFIG_DATA" | grep "$LAYOUT" | awk '{print $1}')
XKBVARIENT=$(echo "$KEYBOARD_CONFIG_DATA" | grep "$VARIENT" | awk '{print $1}')
echo "XKBMODEL=\"$XKBMODEL\"
XKBLAYOUT=\"$XKBLAYOUT\"
XKBVARIANT=\"$XKBVARIENT\"
XKBOPTIONS=\"\"

BACKSPACE=\"guess\"
" > /etc/default/keyboard
echo "90"
# This is the final step to get shit to be seen by X, not really necessary, but imma do it just in case
udevadm trigger --subsystem-match=input --action=change 1>&2
# And lets hope to god all that worked
#STEP 12: Bootloader
{

	mkinitramfs -o /boot/initrd.img-"$(uname --release)"
	if [ "$EFI" != "NULL" ]; then
		#systemd-boot
		mkdir -p /boot/efi/loader/entries /boot/efi/Drauger_OS 1>&2
		export SYSTEMD_RELAX_ESP_CHECKS=1
		echo "export SYSTEMD_RELAX_ESP_CHECKS=1" >> /etc/environment
		bootctl --path=/boot/efi install 1>&2
		echo -e "default Drauger_OS\ntimeout 5\neditor 1" > /boot/efi/loader/loader.conf
		chattr -i /boot/efi/loader/loader.conf
		#set up kernel version hook
		python3 /systemd_boot_config.py "$ROOT" && . /etc/kernel/postinst.d/zz-update-systemd-boot
		#Update the initramfs? At this point we get dropped at an initramfs prompt so it's something wrong there.
		mkinitramfs -o /boot/initrd.img-"$(uname --release)" 1>&2
		#copy over the kernel and initramfs
		cp /boot/vmlinuz-"$(uname --release)" /boot/efi/vmlinuz 1>&2
		cp /boot/initrd.img-"$(uname --release)" /boot/efi/initrd.img 1>&2
	else
		ROOT=$(echo "$ROOT" | sed 's/[0-9]$//')
		ROOT=$(echo "$ROOT" | sed 's/p$//') #This WILL cause bugs in systems with more than 16 drives if ROOT is on the 16th drives
		grub-mkdevicemap --verbose 1>&2
		grub-install --verbose --force --target=i386-pc "$ROOT" 1>&2
		grub-mkconfig -o /boot/grub/grub.cfg 1>&2
	fi
	sleep 0.5s
	ln /boot/initrd.img-"$(uname --release)" /boot/initrd.img 1>&2
	ln /boot/vmlinuz-"$(uname --release)" /boot/vmlinuz 1>&2
} 1>&2
#STEP 13: remove launcher icon
rm -rfv /home/$USERNAME/.config/xfce4/panel/launcher-3 1>&2
echo "93"
#STEP 14: Fix common problems post-install
. /verify_install.sh
echo "95"
echo "	###	$0 CLOSED	###	" 1>&2


