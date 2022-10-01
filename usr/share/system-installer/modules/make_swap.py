#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  make_swap.py
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
"""Make swap File"""
from __future__ import print_function
from sys import stderr
import subprocess
from os import chmod
from time import sleep
from psutil import virtual_memory

def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def make_swap():
    """Make swap File"""
    eprint("    ###    make_swap.py STARTED    ###    ")
    mem = virtual_memory()
    # get data we need to get total system memory
    swap = mem.total
    # you would think more threads would make it use more
    # CPU time and write faster but testing suggestes otherwise
    # testing says once you hit the same number of threads
    # the CPU has, there's no more you can get
    swap = round((swap + ((swap / 1024 ** 3) ** 0.5) * 1024 ** 3))
    # you would think having a larger string would help,
    # but past a certain point it does not
    multiplyer = 10000
    load_balancer = 3
    master_string = "\0" * multiplyer
    swap = round(swap / multiplyer)
    loop_count = round(swap / (multiplyer * load_balancer))
    print_point = round(loop_count / 20)
    perc = 5
    with open("/.swapfile", "w+") as swapfile:
        swapfile.write("")
        swapfile.flush()
        subprocess.check_call(["chattr", "+C", "swapfile"])
        for i in range(loop_count):
            swapfile.write(master_string * (multiplyer * load_balancer))
            swapfile.flush()
            if (i % print_point) == 0:
                if perc <= 100:
                    eprint(f"SWAP FILE { perc }% complete")
                    perc += 5
    chmod("/.swapfile", 0o600)
    subprocess.check_call(["mkswap", "/.swapfile"], stdout=stderr.buffer)
    sleep(0.1)
    subprocess.Popen(["swapon", "/.swapfile"])
    eprint("    ###    make_swap.py CLOSED    ###    ")

if __name__ == '__main__':
    make_swap()
