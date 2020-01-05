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
	/usr/share/system-installer/UI/error.py "No Drives Larger than 16 GB detected"
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
	/usr/share/system-installer/UI/error.py "RAM is less than 1 GB"
	exit 2
fi
#if the code is down to here and has not had some sort of bug, then we are good to go.
#for now, the installer will be in english only
# STEP 3: Show splash screen
#start up main.py
#	main.py has some important info the user will need while installing. Such as warnings and instructions.
set -Ee
# WITH SYSTEM-INSTALLER 0.5.4-ALPHA6, MAIN.PY OBTAINS ALL USER SETTINGS
continue=$(/usr/share/system-installer/UI/main.py)
if [ "$continue" == "1" ]; then
	exit 0
elif [ -f "$continue" ]; then
	# QUICK INSTALL MODE
	CONFIG=$(<"$continue")
	CONFIG=$(echo "$CONFIG" | grep -v "^#" | grep "=" | sed 's/=/ /g')
	USERNAME=$(echo "$CONFIG" | grep "^username" | awk '{print $2}')
	PASS=$(echo "$CONFIG" | grep "^password" | awk '{print $2}')
	COMPNAME=$(echo "$CONFIG" | grep "^hostname" | awk '{print $2}')
	partitoner=$(echo "$CONFIG" | grep "^paritioner" | awk '{print $2}')
	LANG_SET=$(echo "$CONFIG" | grep "^locale" | awk '{print $2}')
	TIME_ZONE=$(echo "$CONFIG" | grep "^timezone" | awk '{print $2}')
	LOGIN=$(echo "$CONFIG" | grep "^auto-login" | awk '{print $2}')
	if [ "$LOGIN" == "True" ] || [ "$LOGIN" == "true" ]; then
		LOGIN="1"
	else
		LOGIN="0"
	fi
	UPDATES=$(echo "$CONFIG" | grep "^updates" | awk '{print $2}')
	if [ "$UPDATES" == "True" ] || [ "$UPDATES" == "true" ]; then
		UPDATES="1"
	else
		UPDATES="0"
	fi
	EXTRAS=$(echo "$CONFIG" | grep "^thirdparty" | awk '{print $2}')
	if [ "$EXTRAS" == "True" ] || [ "$EXTRAS" == "true" ]; then
		EXTRAS="1"
	else
		EXTRAS="0"
	fi
	set -Ee
	/usr/share/system-installer/UI/confirm.py "$partitoner" $LANG_SET $TIME_ZONE $USERNAME $COMPNAME $PASS $EXTRAS $UPDATES $LOGIN
	set +Ee
	## INSTALL THE SYSTEM
	/usr/share/system-installer/installer.sh "$partitoner" $LANG_SET $TIME_ZONE $USERNAME $COMPNAME $PASS $EXTRAS $UPDATES $LOGIN | zenity --progress --text="Installing Drauger OS to your internal hard drive.\nThis may take 	some time. If you have an error, please send\nthe log file (located at /tmp/system-installer.log) to: contact@draugeros.org" --time-remaining --no-cancel --auto-close || /usr/share/system-installer/UI/error.py  "Error detected. Error Code: $?\nPlease see /tmp/system-installer.log for details."
	test="$?"
	if [ "$test" == "0" ]; then
		/usr/share/system-installer/UI/success.py
	else
		/usr/share/system-installer/UI/error.py "Installation has failed. Please send the log file at /tmp/system-installer.log to contact@draugeros.org along with a discription of the issue you experienced. Or, submit an issue on our GitHub at https://github.com/drauger-os-development/system-installer"
	fi
	echo "	###	$0 CLOSED	###	" 1>&2
	exit "$test"
fi
#set -Ee
# Instead of parsing everything out here, just pass the data and let the parts that need it parse it
# If a part doesn't need as much data, the parent process will parse it down to the bare necessities before passing
/usr/share/system-installer/UI/confirm.py "$continue"
set +Ee
## STEP 9: INSTALL THE SYSTEM
{
	/usr/share/system-installer/installer.sh "$continue" | zenity --progress --text="Installing Drauger OS to your internal hard drive.\nThis may take some time. If you have an error, please send\nthe log file (located at /tmp/system-installer.log) to: contact@draugeros.org" --time-remaining --no-cancel --auto-close || /usr/share/system-installer/UI/error.py  "Error detected. Error Code: $?\nPlease see /tmp/system-installer.log for details."
} && {
	/usr/share/system-installer/UI/success.py
} || {
	/usr/share/system-installer/UI/error.py "Installation has failed. Please send the log file at /tmp/system-installer.log to contact@draugeros.org along with a discription of the issue you experienced. Or, submit an issue on our GitHub at https://github.com/drauger-os-development/system-installer"
}
echo "	###	$0 CLOSED	###	" 1>&2
exit "$test"
