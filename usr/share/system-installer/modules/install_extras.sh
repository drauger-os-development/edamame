#!/bin/bash
# -*- coding: utf-8 -*-
#
#  install_extras.sh
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
builtin echo -e "\t###\tinstall_extras.sh STARTED\t###\t" 1>&2
set -o pipefail
set -e
apt update 1>&2
set +e
if $(lspci | grep -iq "nvidia"); then
	list=$(apt search nvidia-driver 2>/dev/null | grep '^nvidia-driver-*' | sed 's/nvidia-driver-//g' | sed 's/\// /g' | awk '{print $1}')
	greatest=$(builtin echo "${list[*]}" | sort -nr | head -n1)
	NVIDIA="nvidia-driver-$greatest"
fi
builtin echo "76"
apt install -y ubuntu-restricted-extras ubuntu-restricted-addons $NVIDIA 1>&2
builtin echo "80"
if $(lspci | grep -iq "broadcom"); then
	if $(lspci |  grep -i "broadcom" | grep -iqE 'BCM43142|BCM4331|BCM4360|BCM4352'); then
		apt install -y broadcom-sta-dkms dkms wireless-tools 1>&2
	elif $(lspci |  grep -i "broadcom" | grep -iqE 'BCM4311|BCM4312|BCM4313|BCM4321|BCM4322|BCM43224|43225|BCM43227|BCM43228'); then
		apt install -y bcmwl-kernel-source 1>&2
	else
		builtin echo -e "# BROADCOM DEVICE DETECTED BUT NO WIFI DRIVER IS FOUND FOR IT #" 1>&2
	fi
fi

builtin echo "82"
apt purge -y gstreamer1.0-fluendo-mp3 1>&2 || builtin echo "Package Not Found? Maybe? Double check cause gstreamer1.0-fluendo-mp3 threw an error during removal" 1>&2
if [ "$NVIDIA" != "" ]; then
	builtin echo -e "\t###\tNVIDIA DRIVERS MAY HAVE BEEN INSTALLED. DISABLING NOUVEAU.\t###\t" 1>&2
	builtin echo -e "blacklist nouveau\noptions nouveau modeset=0" > /etc/modprobe.d/blacklist-nvidia-nouveau.conf
fi 
builtin echo "83"
builtin echo -e "\t###\tinstall_extras.sh CLOSED\t###\t" 1>&2
