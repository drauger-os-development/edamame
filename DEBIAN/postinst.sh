#!/bin/bash
# -*- coding: utf-8 -*-
#
#  postinst.sh
#  
#  Copyright 2023 Thomas Castleman <contact@draugeros.org>
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
users=$(cat /etc/passwd | sed 's/:/ /g' | awk '{print $1}')
if $(echo "$users" | grep -vq "system-installer"); then
	adduser --disabled-password --quiet --system --home /nonexistent --no-create-home --group system-installer --shell /bin/false
	usermod -aG syslog system-installer
fi
