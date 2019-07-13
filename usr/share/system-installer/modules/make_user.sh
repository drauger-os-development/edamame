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
USERNAME="$1"
PASS="$2"
#add new user
useradd "$USERNAME" -s /bin/bash -m -U
usermod -a -G adm "$USERNAME"
usermod -a -G cdrom "$USERNAME"
usermod -a -G sudo "$USERNAME"
usermod -a -G dip "$USERNAME"
usermod -a -G plugdev "$USERNAME"
usermod -a -G lpadmin "$USERNAME"
usermod -a -g sambashare "$USERNAME"
echo "$USERNAME:$PASS" | chpasswd
cp -R /home/live/* /home/$USERNAME
chown -R "$USERNAME:$USERNAME" /home/$USERNAME/*
#remove live user
deluser live --remove-home

