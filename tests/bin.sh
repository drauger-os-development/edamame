#!/bin/bash
# -*- coding: utf-8 -*-
#
#  bin.sh
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
R='\033[0;31m'
G='\033[0;32m'
Y='\033[1;33m'
NC='\033[0m'
#test all programs accessable from the shell
list=$(ls ../usr/bin)
#list of arguments that must be tested
options="-v -h --version --help"
echo -e "\n- $Y \bCHECKING usr/bin FILES$NC"
for each in $list; do
	echo -e "\n- $Y \b$each$NC"
	for args in $options; do
		#retreive output
		output=$(../usr/bin/$each $args)
		#check if output is correct for each argument
		if [ "$args" == "-v" ]; then
			VERSION="$output"
			output=$(echo "$output" | sed 's/-alpha[0-9]$//' | sed 's/-beta[0-9]$//')
			if $(echo "$output" | grep -q "^[0-9].[0-9].[0-9]$"); then
				echo -e "\n- $G \bVERSION: CORRECT$NC"
			else
				echo -e "\n- $R \bVERSION: INCORRECT$NC - $output must match [0-9].[0-9].[0-9] with an optional -alpha[0-9] or -beta[0-9] suffix"
			fi
		elif [ "$args" == "--version" ]; then
			if [ "$output" == "$VERSION" ]; then
				echo -e "\n- $G \bVERSION EXTENDED FLAG: CORRECT$NC"
			else
				echo -e "\n- $R \bVERSION	EXTENDED FLAG: INCORRECT$NC - $output does not equal $VERSION"
			fi
		elif [ "$args" == "-h" ]; then
			HELP="$output"
			if $(echo "$output" | egrep -q "^[0-9].[0-9].[0-9](-alpha[0-9])|(-beta[0-9])|()"); then
				echo -e "\n- $G \bHELP DIALOG: PRESENT$NC"
			elif [ "$output" == "" ] || [ "$output" == " " ]; then
				echo -e "\n- $R \bHELP DIALOG: NOT PRESENT$NC"
			else
				echo -e "\n- $Y \bHELP DIALOG: DOES NOT CONTAIN VERSION$NC"
			fi
		elif [ "$args" == "--help" ]; then
			if [ "$output" == "$HELP" ]; then
				echo -e "\n- $G \bHELP DIALOG EXTENDED FLAG: CORRECT$NC"
			else
				echo -e "\n- $R \bHELP DIALOG	EXTENDED FLAG: INCORRECT$NC - $output does not equal $VERSION"
			fi
		fi
	done
	if [ "$each" == "system-installer" ]; then
		echo -e "\n- $Y \bTESTING INSTALLATION MODE$NC"
		output=$(python3 -I ../usr/bin/$each)
		stdin="localuser:root being added to access control list
RUNNING LOG LOCATED AT /tmp/system-installer.log
localuser:root being removed from access control list"
		if [ "$output" == "$stdin" ]; then
			echo -e "\n- $G \bINSTALL MODE STDOUT: GOOD$NC"
		else
			echo -e "\n- $Y \bINSTALL MODE STDOUT: UNEXPECTED OUTPUT:$NC\n$output"
		fi
		if [ -f /tmp/system-installer.log ]; then
			echo -e "\n- $G \bLOG FILE: EXISTS$NC"
		else
			echo -e "\n- $R \bLOG FILE: MISSING /tmp/system-installer.log$NC"
			exit 1
		fi
		log_output=$(</tmp/system-installer.log)
		stdin="Error accessing /usr/share/system-installer/engine.py: No such file or directory"
		if [ "$log_output" == "$stdin" ]; then
			echo -e "\n- $G \bATTEMPTED TO CALL engine.py: TRUE$NC"
		else
			echo -e "\n- $R \bATTEMPTED TO CALL engine.py: FALSE$NC"
		fi
	fi
done
for each in $list; do
	echo -e "- $Y \bPYLINT: $each $NC"
	pylint ../usr/bin/"$each"
done
