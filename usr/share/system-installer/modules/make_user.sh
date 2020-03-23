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

function fix_home () 
{
	{
		USERNAME="$1"
		if [ -f /home/home/live ]; then
			mv -v /home/home/live /home/"$USERNAME"
			rm -vrf /home/home
		else
			echo "An error occured setting home directory. Hopefully the user's own files are there?"
		fi
	} 1>&2
}

#change live user to $USERNAME
usermod -l "$USERNAME" live 1>&2
groupmod -n "$USERNAME" live 1>&2
echo "50"
if $(ls /home | grep -q "$USERNAME"); then
	#check to see if the user has a home folder already. 
	echo "Original home folder found. Substituting it in . . ." 1>&2
	rm -rfv /home/live 1>&2
else
	#change refrences from old home to new
	# echo "Fixing refrences to old home . . ." 1>&2
	# list=$(grep -IRFl /home/live 2>/dev/null)
	# for each in $list; do
	# 	echo "$each" 1>&2
	# 	sed -i "s:/home/live:/home/$USERNAME:g" "$each"
	# done
	sed -i "s:/home/live:/home/$USERNAME:g" /home/live/.config/gtk-3.0/bookmarks
	#rename home directory
	mv -v /home/live /home/"$USERNAME" || fix_home "$USERNAME"
fi
echo "51"
sed -i "s/live/$USERNAME/g" /etc/passwd
echo "54"
#change password
chpasswd "$USERNAME:$PASSWORD" 1>&2
echo "55"
echo "	###	make_user.sh CLOSED	###	" 1>&2

