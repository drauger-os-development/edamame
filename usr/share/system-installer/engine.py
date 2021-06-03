#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  engine.py
#
#  Copyright 2021 Thomas Castleman <contact@draugeros.org>
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
import subprocess
from os import path, listdir, remove, kill
import json
import tarfile as tar
from shutil import copyfile, copytree
import traceback
import psutil
import UI
import installer
import check_internet
import check_kernel_versions
import common
import auto_partitioner
import oem


common.eprint("    ###    %s STARTED    ###    " % (sys.argv[0]))
if len(sys.argv) > 1:
    if sys.argv[1] == "--systemd-launch":
        # OEM post-install configuration, on-boot installation, and more
        # are handled here
        with open("/proc/cmdline", "r") as cmdline_file:
            cmdline = cmdline_file.read()[:-1].split(" ")
        if "system-installer" not in cmdline:
            # Not wanted to be running ootb
            sys.exit(0)
        # Kill Xfce4 Panel, makes this more emersive
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == "xfce4-panel":
                proc.kill()
        if "post-install" in cmdline:
            # OEM post installation configuration
MEMCHECK = psutil.virtual_memory().total
if (MEMCHECK / 1024 ** 2) < 1024:
    UI.error.show_error("\n\tRAM is less than 1 GB.\t\n")
    sys.exit(2)

DISK = auto_partitioner.check_disk_state()
for each in range(len(DISK) - 1, -1, -1):
    if float(DISK[each]["size"]) < auto_partitioner.LIMITER:
        del DISK[each]
if len(DISK) < 1:
    UI.error.show_error("\n\tNo 32 GB or Larger Drives detected\t\n")
    sys.exit(2)
if not check_kernel_versions.check_kernel_versions():
    UI.error.show_error("""
\t<b>Kernel Version Mismatch.</b>\t
\tPlease reboot and retry installation.\t
\tIf your problem persists, please create an issue on our Github.\t
""")
    sys.exit(2)
work_dir = "/tmp/quick-install_working-dir"
SETTINGS = UI.main.show_main()
try:
    if ((SETTINGS == 1) or (len(SETTINGS) == 0)):
        sys.exit(1)
    elif SETTINGS == 2:
        UI.error.show_error("""
\t<b>Unknown Error</b>\t
\tWe're sorry. An unknown error has occured.\t
\tPlease reboot and retry installation.\t
\tIf your problem persists, please create an issue on our Github.\t
""")
        sys.exit(2)
    elif path.exists(SETTINGS):
        if SETTINGS.split("/")[-1][-5:] == ".json":
            with open(SETTINGS, "r") as quick_install_file:
                SETTINGS = json.load(quick_install_file)
        elif SETTINGS.split("/")[-1][-7:] == ".tar.xz":
            tar_file = tar.open(name=SETTINGS)
            tar_file.extractall(path=work_dir)
            tar_file.close()
            if path.exists(work_dir + "/settings/installation-settings.json"):
                with open(work_dir + "/settings/installation-settings.json",
                          "r") as quick_install_file:
                    SETTINGS = json.load(quick_install_file)
            try:
                net_settings = listdir(work_dir + "/settings/network-settings")
                if len(net_settings) > 0:
                    copytree(net_settings + "/settings/network-settings",
                             "/etc/NetworkManager/system-connections")
                    common.eprint("\t###\tNOTE: NETWORK SETTINGS COPIED TO LIVE SYSTEM\t###\t")
            except FileNotFoundError:
                pass
        if "DATA" in SETTINGS:
            # Parse out just the data. Ignore everything else.
            SETTINGS = SETTINGS["DATA"]
        if "OEM" in SETTINGS.values():
            # This is an OEM installation. Parts will be skipped now and handled later.
            # Other parts will be automated
            additional_settings = oem.pre_install.show_main()
            for each in additional_settings:
                SETTINGS[each] = additional_settings[each]

except TypeError:
    pass
# Confirm whether settings are correct or not
INSTALL = UI.confirm.show_confirm(SETTINGS)
if INSTALL:
    try:
        # Run the progress bar in the background
        process = subprocess.Popen("/usr/share/system-installer/progress.py")
        pid = process.pid
        SETTINGS["INTERNET"] = check_internet.has_internet()
        installer.install(SETTINGS)
        file_list = listdir("/mnt")
        for each in file_list:
            if each[-3:] in (".sh", ".py", ".xz"):
                try:
                    remove("/mnt/" + each)
                except FileNotFoundError:
                    pass
        common.eprint("    ###    %s CLOSED    ###    " % (sys.argv[0]))
        try:
            copyfile("/tmp/system-installer.log",
                     "/mnt/var/log/system-installer.log")
        except FileNotFoundError:
            common.eprint("    ###    Log Not Found. Testing?    ###    ")
            with open("/tmp/system-installer.log", "w+") as log:
                log.write("""Log was not created during installation.
This is a stand-in file.
""")
            copyfile("/tmp/system-installer.log",
                     "/mnt/var/log/system-installer.log")
        subprocess.Popen(["su", "live", "-c",
                          "/usr/share/system-installer/success.py \'%s\'" % (json.dumps(SETTINGS))])
        kill(pid, 15)
    except Exception as error:
        kill(pid, 15)
        common.eprint("\nAn Error has occured:\n%s\n" % (error))
        common.eprint(traceback.format_exc())
        print("\nAn Error has occured:\n%s\n" % (error))
        print(traceback.format_exc())
        UI.error.show_error("""\n\tError detected.\t
\tPlease see /tmp/system-installer.log for details.\t\n""")
else:
    sys.exit(1)
