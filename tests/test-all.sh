#!/bin/bash
# -*- coding: utf-8 -*-
#
#  test-all.sh
#
#  Copyright 2022 Thomas Castleman <contact@draugeros.org>
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
#tee all output to a log
R='\033[0;31m'
G='\033[0;32m'
Y='\033[1;33m'
NC='\033[0m'
FILE_LIST=$(ls | grep -v 'test-all.sh' | grep '.sh$')
echo -e "$R ### REMOVING OLD LOGS ### $NC"
rm $(ls | grep '.log$')
for each in $FILE_LIST; do
	echo -e "$Y \bTEST: $each $NC"
	if [ "$each" == "bin.sh" ]; then
		bash -x "$each" 2>&1 | tee "$each"_test.log | grep '^- '
	else
		bash -x "$each" 2>&1 | tee "$each"_test.log | grep -v '^+'
	fi
done
touch tests.log
for each in $FILE_LIST; do
	echo -e " ### $each test.log ### " >> tests.log
	cat "$each"_test.log >> tests.log
	rm "$each"_test.log
done
echo -e "$R ### tests.log created ### $NC"
