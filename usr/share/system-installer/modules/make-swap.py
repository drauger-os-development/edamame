#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  make-swap.py
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
from __future__ import print_function
import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

eprint("	###	make_swap.sh STARTED	###	")

def main(argv):
	# just a convention I like to have just in case. Probably will be removed later
	argc = len(argv)
	# import our tools
	from math import sqrt
	from subprocess import Popen
	from psutil import virtual_memory
	from os import chmod, path
	from multiprocessing import cpu_count
	import threading
	from time import sleep
	mem = virtual_memory()
	# get data we need to get total system memory
	SWAP = mem.total
	# you would think more threads would make it use more CPU time and write faster but testing suggestes otherwise
	# testing says once you hit the same number of threads the CPU has, there's no more you can get
	thread_count = cpu_count()
	SWAP = round((SWAP + sqrt((SWAP / 1024 ** 3)) * 1024 ** 3))
	print(57)
	# you would think having a larger string would help, but past a certain point it does not
	multiplyer = 10000
	load_balancer = 3
	master_string = "\0" * multiplyer
	SWAP = round(SWAP / multiplyer)
	threads_running = []
	with open("/.swapfile","w+") as swapfile:
		for i in range(round(SWAP / (multiplyer * load_balancer))):
			swapfile.write(master_string * (multiplyer * load_balancer))
	print("60")
	chmod("/.swapfile",0o600)
	print("62")
	Popen(["mkswap","/.swapfile"])
	sleep(0.1)
	print("64")
	Popen(["swapon","/.swapfile"])
	eprint("	###	make_swap.sh CLOSED	###	")
	return 0



if __name__ == '__main__':
	sys.exit(main(sys.argv))
