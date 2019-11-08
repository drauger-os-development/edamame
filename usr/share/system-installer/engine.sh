#!/bin/bash
# -*- coding: utf-8 -*-
#
#  engine.sh
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
#STEP 1: Figure out if we have enough space to install
#get list of mounted file systems
echo "	###	$0 STARTED	###	" 1>&2
list=$(lsblk | grep "disk" | awk '{print $4}')
#remove all the fs in the megabyte range
removeM=$(echo "$list" | grep 'M')
#remove all the fs in the kilobyte range
removeK=$(echo "$list" | grep 'K')
for each in $removeM; do
	list=$(echo "$list" | sed s/$each//)
done
for each in $removeK; do
	list=$(echo "$list" | sed s/$each//)
done
#remove the rest of the garbage
list=$(echo "$list" | sed 's/SIZE//')
list=$(echo "$list" | sed 's/G//g')
allowable=""
#check to make sure there are drives over 16 GB
for each in $list; do
	if (( $(echo "$each >= 16" | bc -l) )); then
		if [ "$allowable" == "" ]; then
			allowable="$each"
		else
			allowable="$allowable $each"
		fi
	fi
done
#this if statment will halt the entire process if no drives larger than
#16 GB are found
if [ "$allowable" == "" ]; then
	#/usr/share/system-installer/UI/error.py "No Drives Larger than 16 GB detected"
	echo "No Drives Larger than 16 GB detected"
	exit 2
fi
#STEP 2: checking for minumim memory
memcheck=$(free -m | awk '{print $2}')
set -- $memcheck
#get the second word in the string
memcheck="$2"
#make sure memory is equal to or greater than 1024 MB, or 1 GB
if (( $(echo "$memcheck < 1024" | bc -l) )); then
	#/usr/share/system-installer/UI/error.py "RAM is less than 1 GB"
	echo "RAM is less than 1 GB"
	exit 2
fi
#if the code is down to here and has not had some sort of bug, then we are good to go.
#for now, the installer will be in english only
# STEP 3: Show splash screen
#start up main.py
#	main.py has some important info the user will need while installing. Such as warnings and instructions.
set -Ee
continue=$(/usr/share/system-installer/UI/main.py 2>&1 2>>/tmp/system-installer.log)
if [ "$continue" == "1" ]; then
	exit 0
fi
#STEP 4: Select partioning method
#	Due to some issues with partitoning, the below code is commented out for now.
#	Do not use unless testing.
#set -Ee
continue=$(/usr/share/system-installer/UI/partion-type.py 2>>/tmp/system-installer.log)
if [ "$continue" == "EXIT" ]; then
	exit 1
fi
partitoner=$(/usr/share/system-installer/UI/partition-mapper.py 2>>/tmp/system-installer.log)
#if [ "$continue" == "on" ]; then
	#partitoner="auto"
	#if [ -d /sys/firmware/efi ]; then
		##EFI var will be used to set UEFI partiton size when the time comes
		#EFI=200
	#else
		##but if it's -1 you can't have a partition so it's also working as a
		##flag variable
		#EFI="-1"
	#fi
#elif $(echo "$continue" | grep -q "Manually"); then
	##check to see if we are booted using UEFI.
	##WE NEED TO MAKE SURE WE SUPPORT UEFI
	#if [ -d /sys/firmware/efi ]; then
		##EFI var will be used to set UEFI partiton size when the time comes
		#EFI=200
	#else
		##but if it's -1 you can't have a partition so it's also working as a
		##flag variable
		#EFI="-1"
	#fi
	##see if there is an NVMe drive.
	##that is where we want to install after all since they are faster
	#SIZE=$(lsblk -o name,type,label,size | grep "disk" | grep "nvme0" | awk '{print $3}' | sed "s/G//")
	#TYPE="NVMe"
	#if [ "$SIZE" == "" ] || [ "$SIZE" == " " ]; then
		##if there are none check for another drive to install to.
		##but, filter out the Live USB
		##can't install there XD
		#SIZE=$(lsblk -o name,type,label,size | grep "disk" | grep -v "Drauger OS" | grep "sd" | awk '{print $3}' | sed "s/G//")
		#SIZE=$(echo "${SIZE[*]}" | sort -nr | head -n1)
		#TYPE="sd"
	#fi
	##make the partitons for this drive
	##we warned them it favors NVMe drives. \_(*_*)_/
	##don't worry tho, we will be allowing this drive to be changed at a later release
	#set -Ee
	#partioner=$(/usr/share/system-installer/UI/partiton-maker.py "$EFI" "$SIZE" 2>/tmp/system-installer.log)
	#set +Ee
#else
	##if this is running we have a SERIOUS ISSUE
	##and I have no idea how it would have happened
	#/usr/share/system-installer/UI/error.py "An unknown error has occured" 2
	#exit 2
#fi
#STEP 5: figure out their Locale
LOCALE=$(/usr/share/system-installer/UI/get_locale.py 2>>/tmp/system-installer.log)
set -- $LOCALE
#if this is anything OTHER than English we gonna have to install the locale
LANG_SET="$1"
#time zone for later
TIME_ZONE="$2"
#STEP 6: Keyboard Layout
#setting keyboard layout is not supported for now. But we are getting the stdout of
#keyboard.py anyways to make our lives easier when it IS supported. We will probably be
#ripping off Ubiquity for this one.
KEYBOARD=$(/usr/share/system-installer/UI/keyboard.py 2>>/tmp/system-installer.log)
#STEP 7: Get user configuration
USER=$(/usr/share/system-installer/UI/user.py 2>>/tmp/system-installer.log)
#STEP 8: check for extra options
OPTIONS=$(/usr/share/system-installer/UI/options.py 2>>/tmp/system-installer.log)
set +Ee
#parse the info from the user config step
NAME=$(echo $USER | grep -o -P '(?<=").*(?=")')
USER=$(echo "$USER" | sed "s/\"$NAME\" //")
set -- $USER
USERNAME="$1"
COMPNAME="$2"
PASS="$3"
#parse the info from the options stage
set -- $OPTIONS
EXTRAS="$1"
UPDATES="$2"
set -Ee
/usr/share/system-installer/UI/confirm.py "$partitoner" $LANG_SET $TIME_ZONE $USERNAME $COMPNAME $PASS $EXTRAS $UPDATES 2>>/tmp/system-installer.log
set +Ee
## STEP 9: INSTALL THE SYSTEM
/usr/share/system-installer/installer.sh "$partitoner" $LANG_SET $TIME_ZONE $USERNAME $COMPNAME $PASS $EXTRAS $UPDATES 2>>/tmp/system-installer.log | zenity --progress --text="Installing Drauger OS to your internal hard drive.\nThis may take some time. If you have an error, please send\nthe log file (located at /tmp/system-installer.log) to: contact@draugeros.org" --time-remaining --no-cancel --auto-close || /usr/share/system-installer/UI/error.py  "Error detected. Error Code: $?\nPlease see /tmp/system-installer.log for details."
test="$?"
if [ "$test" == "0" ]; then
	/usr/share/system-installer/UI/success.py
else
	/usr/share/system-installer/UI/error.py "Installation has failed. Please send the log file at /tmp/system-installer.log to contact@draugeros.org along with a discription of the issue you experienced. Or, submit an issue on our GitHub at https://github.com/drauger-os-development/system-installer"
fi
echo "	###	$0 CLOSED	###	" 1>&2
exit "$test"
