#!/bin/bash
# -*- coding: utf-8 -*-
#
#  make_user.sh
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
echo "	###	make_user.sh STARTED	###	" 1>&2
echo "49"
#change live user to $USERNAME
usermod -l "$USERNAME" live 1>&2
groupmod -n "$USERNAME" live 1>&2
echo "50"
if $(ls /home | grep -q "$USERNAME");
	#check to see if the user has a home folder already. 
	echo "Original home folder found. Substituting it in . . ." 1>&2
	rm -rfv /home/live 1>&2
else
	#change refrences from old home to new
	echo "Fixing refrences to old home . . ." 1>&2
	list=$(grep -IRFl /home/live 2>/dev/null)
	for each in $list; do
		echo "$each" 1>&2
		sed -i "s:/home/live:/home/$USERNAME:g" "$each"
	done
	cd /
	#rename home directory
	mv /home/live /home/"$USERNAME"
fi
echo "51"
sed -i "s/live/$USERNAME/g" /etc/passwd
echo "54"
#change password
echo "$USERNAME:$PASSWORD" | chpasswd
echo "55"
echo "	###	make_user.sh CLOSED	###	" 1>&2

