#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  engine.py
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
from sys import argv, stderr
from subprocess import Popen, PIPE, check_output
from psutil import virtual_memory
from os import path
import multiprocessing
import json
import UI
import installer

# Make it easier for us to print to stderr
def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


#get length of argv
argc = len(argv)
eprint("\t###\t%s STARTED\t###\t" % (argv[0]))
memcheck = virtual_memory().total
if (memcheck / 1024 ** 2) < 1024:
    UI.error.show_error("\n\tRAM is less than 1 GB.\t\n")
    exit(2)

disk = json.loads(check_output(["lsblk", "--json"]))
for each in range(len(disk["blockdevices"]) - 1, -1, -1):
    if disk["blockdevices"][each]["type"] == "loop":
        del disk["blockdevices"][each]
for each in disk["blockdevices"]:
    if float(each["size"][0:len(each["size"]) - 1]) < 16:
        UI.error.show_error("\n\tNo Drives Larger than 16 GB detected\t\n")
settings = UI.main.show_main()
try:
    if settings == 1:
        exit(1)
    elif path.exists(settings):
        print("That's odd. Returned settings shouldn't be a file.")
        print("That setting has been disabled.")
        eprint("Exiting not to prevent any bugs")
        exit(2)
except TypeError:
    pass
install = UI.confirm.show_confirm(settings["AUTO_PART"], settings["ROOT"],
    settings["EFI"], settings["HOME"], settings["SWAP"], settings["LANG"],
    settings["TIME_ZONE"], settings["USERNAME"], settings["PASSWORD"],
    settings["COMPUTER_NAME"], settings["EXTRAS"], settings["UPDATES"],
    settings["LOGIN"], settings["MODEL"], settings["LAYOUT"],
    settings["VARIENBT"])
if install:
    settings = list(str(settings))
    del settings[0]
    del settings[len(settings) - 1]
    settings = "".join(settings)
    try:
        progress = Process(target=UI.progress.show_progress())
        progress.start()
        installer.install(settings)
        progress.join()
    except:
        UI.error.show_error("\n\tError detected.\t\n\tPlease see /tmp/system-installer.log for details.\t\n")
else:
    exit(1)
eprint("\t###\t%s CLOSED\t###\t" % (argv[0]))
