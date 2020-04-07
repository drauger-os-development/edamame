#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  set_time.py
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
from os import symlink, system, remove
from sys import stderr, argv


def eprint(*args, **kwargs):
	print(*args, file=stderr, **kwargs)


def _link(location):
	remove("/etc/localtime")
	symlink("/usr/share/zoneinfo/%s" % (location), "/etc/localtime")


def set_time(TIME_ZONE):
	eprint("	###	set_time.py STARTED	###	")
	# if (TIME_ZONE == "GMT"):
		# _link("GMT")
	# elif (TIME_ZONE == "ECT"):
		# _link("GMT+1")
	# elif ((TIME_ZONE == "EET") or (TIME_ZONE == "ART")):
		# _link("GMT+2")
	# elif (TIME_ZONE == "EAT"):
		# _link("GMT+3")
	# elif (TIME_ZONE == "NET"):
		# _link("GMT+4")
	# elif (TIME_ZONE == "PLT"):
		# _link("GMT+5")
	# elif (TIME_ZONE == "BST"):
		# _link("GMT+6")
	# elif (TIME_ZONE == "VST"):
		# _link("GMT+7")
	# elif (TIME_ZONE == "CTT"):
		# _link("GMT+8")
	# elif (TIME_ZONE == "JST"):
		# _link("GMT+9")
	# elif (TIME_ZONE == "ACT"):
		# symlink("/usr/share/zoneinfo/Australia/ACT", "/etc/localtime")
	# elif (TIME_ZONE == "AET"):
		# _link("GMT+10")
	# elif (TIME_ZONE == "SST"):
		# _link("GMT+11")
	# elif (TIME_ZONE == "NST"):
		# _link("GMT+12")
	# elif (TIME_ZONE == "MIT"):
		# _link("GMT-11")
	# elif (TIME_ZONE == "HST"):
		# _link("GMT-10")
	# elif (TIME_ZONE == "AST"):
		# _link("GMT-9")
	# elif (TIME_ZONE == "PST"):
		# _link("GMT-8")
	# elif (TIME_ZONE == "MST"):
		# _link("GMT-7")
	# elif (TIME_ZONE == "CST"):
		# _link("GMT-6")
	# elif ((TIME_ZONE == "EST") or (TIME_ZONE == "IET")):
		# _link("GMT-5")
	# elif (TIME_ZONE == "PRT"):
		# _link("GMT-4")
	# elif ((TIME_ZONE == "AGT") or (TIME_ZONE == "BET")):
		# _link("GMT-3")
	# elif (TIME_ZONE == "CAT"):
		# _link("GMT-1")
	# else:
		# _link("GMT")
	_link(TIME_ZONE)
	system("hwclock --systohc")
	eprint("	###	set_time.py CLOSED	###	")


if __name__ == '__main__':
	set_time(argv[1])
