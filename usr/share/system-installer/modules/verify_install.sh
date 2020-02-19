#!/bin/bash
# -*- coding: utf-8 -*-
#
#  verify_install.sh
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
{
	builtin echo "### verify_installer.sh STARTED ### "
	home_contents=$(ls /home)
	#remove system-installer
	if $(dpkg -l system-installer | grep -q '^ii'); then
		apt purge -y system-installer
	fi
	#fix home folder location
	if $(builtin echo "$home_contents" | grep -q 'home'); then
		if $(ls /home/home/* 1>/dev/null 2>/dev/null); then
			new_home=$(ls /home/home)
			for each in $new_home; do
				mv /home/home/$each /home/$each
			done
			rm -rf /home/home
		fi
	fi
	#fix password
	builtin echo "$USERNAME:$PASSWORD" | chpasswd
	apt autoremove -y --purge
	builtin echo "### verify_installer.sh CLOSED ### "
} 1>&2
