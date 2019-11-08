#!/bin/bash
# -*- coding: utf-8 -*-
#
#  make_user.sh
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
echo "	###	make_user.sh STARTED	###	" 1>&2
USERNAME="$1"
PASS="$2"
echo "49"
#add new user
useradd "$USERNAME" -s /bin/bash -m -U
echo "50"
usermod -a -G adm "$USERNAME"
usermod -a -G cdrom "$USERNAME"
usermod -a -G sudo "$USERNAME"
usermod -a -G dip "$USERNAME"
usermod -a -G plugdev "$USERNAME"
usermod -a -G lpadmin "$USERNAME"
usermod -a -g sambashare "$USERNAME" 2>/dev/null || echo "samabashare group does not exist. Cannot add $USERNAME" 1>&2
echo "51"
echo "$USERNAME:$PASS" | chpasswd
echo "52"
list=$(ls /home/live)
for each in $live; do
	cp -Rv /home/live/$each /home/$USERNAME 1>&2
done
chown -R "$USERNAME:$USERNAME" /home/$USERNAME/*
chmod 755 -R /home/$USERNAME/*
cd /home/$USERNAME
list=$(ls -a)
for each in $list; do
	if [ "$each" == ".bashrc" ]; then
		chmod 777 $each
	elif [ "$each" == ".gnome" ]  || [ "$each" == ".gnome2" ] || [ "$each" == ".gnome2_private" ] || [ "$each" == ".gvfs" ] || [ "$each" == ".synaptic" ]; then
		chmod 700 $each
	elif [ "$each" == ".cache" ] || [ "$each" == ".mozilla" ] || [ "$each" == ".thumbnails" ]; then
		chmod -R 775 .cache
		chmod -R 775 .cache/*
	elif [ "$each" == ".config" ] || [ "$each" == "Desktop" ] || [ "$each" == "Documents" ] || [ "$each" == "Downloads" ] || [ "$each" == "Pictures" ] || [ "$each" == "Music" ] || [ "$each" == "Public" ] || [ "$each" == "Templates" ] || [ "$each" == "Videos" ] || [ "$each" == ".local" ] || [ "$each" == ".gconf" ] || [ "$each" == ".dbus" ]; then
		chmod -R 755 $each
	elif [ "$each" == ".bash_logout" ] || [ "$each" == ".profile" ] || [ "$each" == ".dmrc" ]; then
		chmod -R 644 "$each"
	fi
done
echo "54"
#remove live user
deluser live --remove-home || rm -rfv /home/live 1>&2
echo "55"
echo "	###	make_user.sh CLOSED	###	" 1>&2

