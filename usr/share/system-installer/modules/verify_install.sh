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
	builtin echo "### verify_install.sh STARTED ### "
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
	chpasswd root:$PASSWORD $USERNAME:$PASSWORD
	apt autoremove -y --purge
	. /etc/kernel/postinst.d/zz-update-systemd-boot || . /etc/kernel/postrm.d/zz-update-systemd-boot
	rm -v /home/$USERNAME/Desktop/system-installer.desktop 1>&2 || rm -rfv /home/$USERNAME/.config/xfce4/panel/launcher-3 1>&2
	if [-f /etc/kernel/postinst.d/zz-update-systemd-boot ]; then
		apt purge -y $(dpkg -l *grub* | grep '^ii' | awk '{print $2}')
	fi
	builtin echo "### verify_install.sh CLOSED ### "
} 1>&2
