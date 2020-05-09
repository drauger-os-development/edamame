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
USERNAME="$1"
PASSWORD="$2"
{
    builtin echo "  ### verify_install.sh STARTED ###   "
    home_contents=$(ls /home)
    #remove system-installer
    if $(dpkg -l system-installer | grep -q '^ii'); then
        apt purge -y system-installer
    fi
    #fix home folder location
    if [ -d /home/home/live ]; then
        mv -v /home/home/live /home/"$USERNAME" 1>&2
        rm -vrf /home/home 1>&2
    else
        echo "An error occured setting home directory. Hopefully the user's own files are there?" 1>&2
    fi
    #fix password
    echo -e "root:$PASSWORD\n$USERNAME:$PASSWORD" | chpasswd
    apt autoremove -y --purge
    . /etc/kernel/postinst.d/zz-update-systemd-boot || . /etc/kernel/postrm.d/zz-update-systemd-boot
    if [ -f /home/$USERNAME/Desktop/system-installer.desktop ] || [ -d /home/$USERNAME/.config/xfce4/panel/launcher-3 ]; then
        rm -v /home/$USERNAME/Desktop/system-installer.desktop 1>&2 || rm -rfv /home/$USERNAME/.config/xfce4/panel/launcher-3 1>&2
    fi
    if [ -f /etc/kernel/postinst.d/zz-update-systemd-boot ]; then
        apt purge -y $(dpkg -l *grub* | grep '^ii' | awk '{print $2}')
    fi
    builtin echo "  ### verify_install.sh CLOSED ###    "
} 1>&2
