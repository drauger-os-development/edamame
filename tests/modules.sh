#!/bin/bash
# -*- coding: utf-8 -*-
#
#  modules.sh
#
#  Copyright 2023 Thomas Castleman <batcastle@draugeros.org>
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
cd ../usr/share/edamame/modules
MODSH_LIST=$(ls *.sh)
MODPY_LIST=$(ls *.py)
for each in $MODSH_LIST; do
	echo -e "- $Y \bSHELLCHECK: $each $NC"
	shellcheck --exclude=SC2206 --shell=bash --severity=warning "$each" --color=never 2>&1
done
for each in $MODPY_LIST; do
	echo -e "- $Y \bPYLINT: $each $NC"
	pylint "$each"
done
