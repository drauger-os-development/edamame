#!/bin/bash
# -*- coding: utf-8 -*-
#
#  install_updates.sh
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
builtin echo -e "\t###\tinstall_updates.sh STARTED\t###\t" 1>&2
set -e
set -o pipefail
apt update 2>/dev/null 1>>/tmp/system-installer.log
builtin echo "67"
apt -y dist-upgrade 2>/dev/null 1>>/tmp/system-installer.log
builtin echo "70"
apt -y autoremove 2>/dev/null 1>>/tmp/system-installer.log
builtin echo "72"
apt clean 2>/dev/null 1>>/tmp/system-installer.log
set +e
builtin echo "74"
builtin echo -e "\t###\tinstall_updates.sh CLOSED\t###\t" 1>&2
