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
"""Make swap File"""
from __future__ import print_function
from sys import stderr
from math import sqrt
from subprocess import Popen, check_call
from os import chmod
from time import sleep
from psutil import virtual_memory

def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def make_swap():
    """Make swap File"""
    eprint("\t###\tmake_swap.py STARTED\t###\t")
    mem = virtual_memory()
    # get data we need to get total system memory
    swap = mem.total
    # you would think more threads would make it use more
    # CPU time and write faster but testing suggestes otherwise
    # testing says once you hit the same number of threads
    # the CPU has, there's no more you can get
    swap = round((swap + sqrt((swap / 1024 ** 3)) * 1024 ** 3))
    print(57)
    # you would think having a larger string would help,
    # but past a certain point it does not
    multiplyer = 10000
    load_balancer = 3
    master_string = "\0" * multiplyer
    swap = round(swap / multiplyer)
    i = 0
    with open("/.swapfile", "w+") as swapfile:
        while i < range(round(swap / (multiplyer * load_balancer))):
            swapfile.write(master_string * (multiplyer * load_balancer))
            swapfile.flush()
            i = i + 1
    print("60")
    chmod("/.swapfile", 0o600)
    print("62")
    check_call(["mkswap", "/.swapfile"])
    sleep(0.1)
    print("64")
    Popen(["swapon", "/.swapfile"])
    eprint("\t###\tmake_swap.py CLOSED\t###\t")

if __name__ == '__main__':
    make_swap()
