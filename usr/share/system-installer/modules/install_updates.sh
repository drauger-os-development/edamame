#!/bin/bash
# -*- coding: utf-8 -*-
#
#  install_updates.sh
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
echo "	###	install_updates.sh STARTED	###	" 1>&2
set -e
set -o pipefail
apt update
echo "67"
apt -y dist-upgrade
echo "70"
apt -y autoremove
echo "72"
apt clean
echo "74"
echo "	###	install_updates.sh CLOSED	###	" 1>&2
