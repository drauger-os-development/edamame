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
"""Main installation Engine"""
from __future__ import print_function
import sys
from subprocess import check_output, Popen
from os import path, listdir, remove, fork, kill
import json
# import threading
import multiprocessing
from psutil import virtual_memory
from shutil import copyfile
import UI
import installer


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)



eprint("\t###\t%s STARTED\t###\t" % (sys.argv[0]))
MEMCHECK = virtual_memory().total
if (MEMCHECK / 1024 ** 2) < 1024:
    UI.error.show_error("\n\tRAM is less than 1 GB.\t\n")
    sys.exit(2)

DISK = json.loads(check_output(["lsblk", "--json"]))
for each in range(len(DISK["blockdevices"]) - 1, -1, -1):
    if DISK["blockdevices"][each]["type"] == "loop":
        del DISK["blockdevices"][each]
for each in range(len(DISK["blockdevices"]) - 1, -1, -1):
    if float(DISK["blockdevices"][each]["size"][0:len(DISK["blockdevices"]
                                                      [each]["size"]) - 1]) < 16:
        del DISK["blockdevices"][each]
if len(DISK["blockdevices"]) < 1:
    UI.error.show_error("\n\tNo Drives Larger than 16 GB detected\t\n")
    sys.exit(2)
SETTINGS = UI.main.show_main()
try:
    if ((SETTINGS == 1) or (len(SETTINGS) == 0)):
        sys.exit(1)
    elif path.exists(SETTINGS):
        with open(SETTINGS, "r") as quick_install_file:
            try:
                SETTINGS = json.loads(quick_install_file.read())["DATA"]
            except KeyError:
                SETTINGS = json.loads(quick_install_file.read())
except TypeError:
    pass
INSTALL = UI.confirm.show_confirm(SETTINGS["AUTO_PART"], SETTINGS["ROOT"],
                                  SETTINGS["EFI"], SETTINGS["HOME"],
                                  SETTINGS["SWAP"], SETTINGS["LANG"],
                                  SETTINGS["TIME_ZONE"], SETTINGS["USERNAME"],
                                  SETTINGS["PASSWORD"],
                                  SETTINGS["COMPUTER_NAME"],
                                  SETTINGS["EXTRAS"], SETTINGS["UPDATES"],
                                  SETTINGS["LOGIN"], SETTINGS["MODEL"],
                                  SETTINGS["LAYOUT"],
                                  SETTINGS["VARIENT"])
if INSTALL:
    try:
        # fork() to get proper multi-threading needs
        PROGRESS = multithreading.Process(target=UI.progress.show_progress)
        # PROGRESS = threading.Thread(target=UI.progress.show_progress)
        PROGRESS.start()
        # otherwise, we are parent and should continue
        installer.install(SETTINGS)
        file_list = listdir("/mnt")
        for each in file_list:
            if each[-3:] in (".sh", ".py", ".7z"):
                try:
                    remove("/mnt/" + each)
                except FileNotFoundError:
                    pass
        eprint("\t###\t%s CLOSED\t###\t" % (sys.argv[0]))
        try:
            copyfile("/tmp/system-installer.log", "/mnt/var/log/system-installer.log")
        except FileNotFoundError:
            eprint("\t###\tLog Not Found. Testing?\t###\t")
            with open("/tmp/system-installer.log", "w+") as log:
                log.write("""Log was not created during installation.
This is a stand-in file.
""")
            copyfile("/tmp/system-installer.log", "/mnt/var/log/system-installer.log")
        Popen(["/usr/share/system-installer/success.py", json.dumps(SETTINGS)])
        PROGRESS.terminate()
        PROGRESS.join()
    except Exception as error:
        eprint("\nAn Error has occured:\n%s\n" % (error))
        print("\nAn Error has occured:\n%s\n" % (error))
        UI.error.show_error("""\n\tError detected.\t
\tPlease see /tmp/system-installer.log for details.\t\n""")
else:
    sys.exit(1)
