#!/bin/bash
# -*- coding: utf-8 -*-
#
#  set_time.sh
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
settime () {
	ln -sf /usr/share/zoneinfo/Etc/"$1" /etc/localtime
}
echo "37"
TIME_ZONE="$1"
if [ "$TIME_ZONE" == "GMT" ]; then
	settime "GMT"
elif [ "$TIME_ZONE" == "ECT" ]; then
	settime "GMT+1"
elif [ "$TIME_ZONE" == "EET" ] || [ "$TIME_ZONE" == "ART" ]; then
	settime "GMT+2"
elif [ "$TIME_ZONE" == "EAT" ]; then
	settime "GMT+3"
elif [ "$TIME_ZONE" == "NET" ]; then
	settime "GMT+4"
elif [ "$TIME_ZONE" == "PLT" ]; then
	settime "GMT+5"
elif [ "$TIME_ZONE" == "BST" ]; then
	settime "GMT+6"
elif [ "$TIME_ZONE" == "VST" ]; then
	settime "GMT+7"
elif [ "$TIME_ZONE" == "CTT" ]; then
	settime "GMT+8"
elif [ "$TIME_ZONE" == "JST" ]; then
	settime "GMT+9"
elif [ "$TIME_ZONE" == "ACT" ]; then
	ln -sf /usr/share/zoneinfo/Australia/ACT /etc/localtime
elif [ "$TIME_ZONE" == "AET" ]; then
	settime "GMT+10"
elif [ "$TIME_ZONE" == "SST" ]; then
	settime "GMT+11"
elif [ "$TIME_ZONE" == "NST" ]; then
	settime "GMT+12"
elif [ "$TIME_ZONE" == "MIT" ]; then
	settime "GMT-11"
elif [ "$TIME_ZONE" == "HST" ]; then
	settime "GMT-10"
elif [ "$TIME_ZONE" == "AST" ]; then
	settime "GMT-9"
elif [ "$TIME_ZONE" == "PST" ]; then
	settime "GMT-8"
elif [ "$TIME_ZONE" == "MST" ]; then
	settime "GMT-7"
elif [ "$TIME_ZONE" == "CST" ]; then
	settime "GMT-6"
elif [ "$TIME_ZONE" == "EST" ] || [ "$TIME_ZONE" == "IET" ]; then
	settime "GMT-5"
elif [ "$TIME_ZONE" == "PRT" ]; then
	settime "GMT-4"
elif [ "$TIME_ZONE" == "AGT" ] || [ "$TIME_ZONE" == "BET" ]; then
	settime "GMT-3"
elif [ "$TIME_ZONE" == "CAT" ]; then
	settime "GMT-1"
else
	settime "GMT"
fi
echo "38"
hwclock --systohc
