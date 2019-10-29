#!/bin/bash
# -*- coding: utf-8 -*-
#
#  install_extras.sh
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
echo "	###	install_extras.sh STARTED	###	" 1>&2
set -e
set -o pipefail
apt update
toinstall=""
toremove=""
if $(lspci | grep -iq "nvidia"); then
	list=$(apt search nvidia-driver 2>/dev/null | grep '^nvidia-driver-*' | sed 's/nvidia-driver-//g' | sed 's/\// /g' | awk '{print $1}')
	greatest=$(echo "${list[*]}" | sort -nr | head -n1)
	toinstall="nvidia-driver-$greatest"
fi
echo "76"
if $(lspci | grep -iq "broadcom"); then
	if [ "$toinstall" == "" ]; then
		toinstall="broadcom-sta"
	else
		toinstall="$toinstall broadcom-sta"
	fi
fi
echo "80"
if [ "$toinstall" == "" ]; then
	toinstall="ubuntu-restricted-extras"
	toremove="gstreamer1.0-fluendo-mp3"
else
	toinstall="$toinstall ubuntu-restricted-extras"
	toremove="gstreamer1.0-fluendo-mp3"
fi
echo "82"
apt install -y $toinstall
echo "83"
if [ "$toremove" != "" ]; then
	apt purge -y $toremove || echo "Package Not Found? Maybe? Double check cause gstreamer1.0-fluendo-mp3 threw an error during removal" 1>&2
	echo "83"
fi
echo "	###	install_extras.sh CLOSED	###	" 1>&2
