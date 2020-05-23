#!/bin/bash
# -*- coding: utf-8 -*-
#
#  installer.sh
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
R='\033[0;31m'
G='\033[0;32m'
Y='\033[1;33m'
NC='\033[0m'
echo -e "$Y \PYLINT: installer.py $NC"
{
	pylint ../usr/share/system-installer/installer.py 2>&1
} && {
	echo -e "-$G INSTALLER.PY: GOOD"
} || {
	echo -e "-$R INSTALLER.PY: NEEDS CORRECTIONS"
}
