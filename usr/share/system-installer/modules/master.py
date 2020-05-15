#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  master.py
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
"""
Configure newly installed system from within a chroot
"""
from __future__ import print_function
from sys import argv, stderr
from subprocess import Popen, PIPE, check_output, check_call, CalledProcessError
import multiprocessing
from os import remove, mkdir, environ, symlink, chmod, listdir, path
from shutil import rmtree, copyfile
from inspect import getfullargspec
from time import sleep
import json
import urllib3
import warnings


# import our own programs
import modules.auto_login_set as auto_login_set
import modules.make_swap as make_swap
import modules.set_time as set_time
import modules.systemd_boot_config as systemd_boot_config
import modules.set_locale as set_locale

def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)

def check_internet():
    """Check Internet Connectivity"""
    try:
        urllib3.connection_from_url('http://draugeros.org', timeout=1)
        return True
    except urllib3.exceptions.ConnectTimeoutError:
        return False
    except urllib3.exceptions.ConnectionError:
        return False
    except urllib3.exceptions.TimeoutError:
        return False
    except urllib3.exceptions.HTTPError:
        return False

def __update__(percentage):
    value = ""
    try:
        with open("/tmp/system-installer-progress.log", "r") as progress:
            value = int(progress.read())
        if int(percentage) > value:
            with open("/tmp/system-installer-progress.log", "w+") as progress:
                progress.write(str(percentage))
    except PermissionError:
        chmod("/tmp/system-installer-progress.log", 0o666)
        with open("/tmp/system-installer-progress.log", "r") as progress:
            value = int(progress.read())
        if int(percentage) > value:
            with open("/tmp/system-installer-progress.log", "w+") as progress:
                progress.write(str(percentage))
    except FileNotFoundError:
        with open("/tmp/system-installer-progress.log", "w+") as progress:
            progress.write(str(percentage))

class MainInstallation():
    """Main Installation Procedure, minus low-level stuff"""
    def __init__(self, processes_to_do, settings):
        for each1 in processes_to_do:
            process_new = getattr(MainInstallation, each1, self)
            args_list = getfullargspec(process_new)[0]
            args = []
            for each in args_list:
                args.append(settings[each])
            globals()[each1] = multiprocessing.Process(target=process_new, args=args)
            globals()[each1].start()
        while len(processes_to_do) > 0:
            for each in range(len(processes_to_do) - 1, -1, -1):
                if not globals()[processes_to_do[each]].is_alive():
                    globals()[processes_to_do[each]].join()
                    del processes_to_do[each]

    def time_set(TIME_ZONE):
        """Set system time"""
        set_time.set_time(TIME_ZONE)

    def locale_set(LANG):
        """Set system locale"""
        set_locale.set_locale(LANG)

    def set_networking(COMPUTER_NAME):
        """Set system hostname"""
        eprint("Setting hostname to %s" % (COMPUTER_NAME))
        try:
            remove("/etc/hostname")
        except FileNotFoundError:
            pass
        with open("/etc/hostname", "w+") as hostname:
            hostname.write(COMPUTER_NAME)
        try:
            remove("/etc/hosts")
        except FileNotFoundError:
            pass
        with open("/etc/hosts", "w+") as hosts:
            hosts.write("127.0.0.1 %s" % (COMPUTER_NAME))
        __update__(48)

    def make_user(USERNAME, PASSWORD):
        """Set up main user"""
        # This needs to be set up in Python. Leave it in shell for now
        try:
            Popen(["/make_user.sh", USERNAME, PASSWORD])
        except PermissionError:
            chmod("/make_user.sh", 0o777)
            Popen(["/make_user.sh", USERNAME, PASSWORD])

    def mk_swap(SWAP):
        """Make swap file"""
        if SWAP == "FILE":
            try:
                make_swap.make_swap()
                with open("/etc/fstab", "a") as fstab:
                    fstab.write("/.swapfile swap    swap    defaults    0   0")
            except IOError:
                eprint("Adding swap failed. Must manually add later")
        __update__(66)

    def __install_updates__(UPDATES, INTERNET):
        """Install updates"""
        if ((UPDATES) and (INTERNET)):
            try:
                check_call("/install_updates.sh")
            except PermissionError:
                chmod("/install_updates.sh", 0o777)
                check_call("/install_updates.sh")
        elif not INTERNET:
            eprint("Cannot install updates. No internet.")

    def __install_extras__(EXTRAS, INTERNET):
        """Install Restricted Extras and Drivers"""
        if ((EXTRAS) and (INTERNET)):
            try:
                check_call("/install_extras.sh")
            except PermissionError:
                chmod("/install_extras.sh", 0o777)
                check_call("/install_extras.sh")
        elif not INTERNET:
            eprint("Cannot install extras. No internet.")

    def apt(UPDATES, EXTRAS, INTERNET):
        """Run commands for apt sequentially to avoid front-end lock"""
        MainInstallation.__install_updates__(UPDATES, INTERNET)
        MainInstallation.__install_extras__(EXTRAS, INTERNET)

    def set_passwd(PASSWORD):
        """Set Root password"""
        __update__(84)
        process = Popen("chpasswd", stdout=stderr.buffer, stdin=PIPE, stderr=PIPE)
        process.communicate(input=bytes(r"root:%s" % (PASSWORD), "utf-8"))
        __update__(85)

    def lightdm_config(LOGIN, USERNAME):
        """Set autologin setting for lightdm"""
        auto_login_set.auto_login_set(LOGIN, USERNAME)

    def set_keyboard(MODEL, LAYOUT, VARIENT):
        """Set keyboard model, layout, and varient"""
        with open("/usr/share/X11/xkb/rules/base.lst", "r") as xkb_conf:
            kcd = xkb_conf.read()
        kcd = kcd.split("\n")
        for each1 in enumerate(kcd):
            kcd[each1[0]] = kcd[each1[0]].split()
        try:
            remove("/etc/default/keyboard")
        except FileNotFoundError:
            pass
        xkbm = ""
        xkbl = ""
        xkbv = ""
        for each1 in kcd:
            if " ".join(each1[1:]) == MODEL:
                xkbm = each1[0]
            elif " ".join(each1[1:]) == LAYOUT:
                xkbl = each1[0]
            elif " ".join(each1[1:]) == VARIENT:
                xkbv = each1[0]
        with open("/etc/default/keyboard", "w+") as xkb_default:
            xkb_default.write("""XKBMODEL=\"%s\"
XKBLAYOUT=\"%s\"
XKBVARIANT=\"%s\"
XKBOPTIONS=\"\"

BACKSPACE=\"guess\"
""" % (xkbm, xkbl, xkbv))
        __update__(90)
        Popen(["udevadm", "trigger", "--subsystem-match=input",
               "--action=change"], stdout=stderr.buffer)

    def remove_launcher(USERNAME):
        """Remove system installer desktop launcher"""
        try:
            remove("/home/%s/Desktop/system-installer.desktop" % (USERNAME))
        except FileNotFoundError:
            try:
                rmtree("/home/%sE/.config/xfce4/panel/launcher-3" % (USERNAME))
            except FileNotFoundError:
                eprint("Cannot find launcher for system-installer. User will need to remove manually.")

def set_plymouth_theme():
    """Ensure the plymouth theme is set correctly"""
    Popen(["update-alternatives", "--install",
           "/usr/share/plymouth/themes/default.plymouth",
           "default.plymouth",
           "/usr/share/plymouth/themes/drauger-theme/drauger-theme.plymouth",
           "100", "--slave",
           "/usr/share/plymouth/themes/default.grub", "default.plymouth.grub",
           "/usr/share/plymouth/themes/drauger-theme/drauger-theme.grub"],
          stdout=stderr.buffer)
    process = Popen(["update-alternatives", "--config",
                     "default.plymouth"], stdout=stderr.buffer, stdin=PIPE,
                    stderr=PIPE)
    process.communicate(input=bytes("2\n", "utf-8"))
    __update__(86)

def install_kernel():
    """Install kernel from kernel.7z"""
    # we are going to do offline kernel installation from now on.
    # it's just easier and more reliable
    check_call(["7z", "x", "/kernel.7z"], stdout=stderr.buffer)
    check_call(["apt", "purge", "-y", "linux-headers-drauger",
                "linux-image-drauger"], stdout=stderr.buffer)
    check_call(["apt", "autoremove", "-y", "--purge"], stdout=stderr.buffer)
    check_call(["dpkg", "-R", "--install", "kernel/"], stdout=stderr.buffer)
    rmtree("/kernel")


def install_bootloader(efi, root, release):
    """Determine whether bootloader needs to be systemd-boot (for UEFI) or GRUB (for BIOS)
    and install the correct one."""
    if efi not in ("NULL", None, ""):
        _install_systemd_boot(release, root)
    else:
        _install_grub(root)

def _install_grub(root):
    """set up and install GRUB.
    This function is only retained for BIOS systems."""
    root = list(root)
    for each1 in range(len(root) - 1, -1, -1):
        try:
            int(root[each1])
            del root[each1]
        except ValueError:
            break
    if root[-1] == "p":
        del root[-1]
    root = "".join(root)
    check_call(["grub-mkdevicemap", "--verbose"], stdout=stderr.buffer)
    check_call(["grub-install", "--verbose", "--force", "--target=i386-pc",
                root], stdout=stderr.buffer)
    check_call(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"],
               stdout=stderr.buffer)

def _install_systemd_boot(release, root):
    """set up and install systemd-boot"""
    try:
        mkdir("/boot/efi")
    except FileExistsError:
        pass
    mkdir("/boot/efi/loader")
    mkdir("/boot/efi/loader/entries")
    mkdir("/boot/efi/Drauger_OS")
    environ["SYSTEMD_RELAX_ESP_CHECKS"] = "1"
    with open("/etc/environment", "a") as envi:
        envi.write("export SYSTEMD_RELAX_ESP_CHECKS=1")
    check_call(["bootctl", "--path=/boot/efi", "install"], stdout=stderr.buffer)
    with open("/boot/efi/loader/loader.conf", "w+") as loader_conf:
        loader_conf.write("default Drauger_OS\ntimeout 5\neditor 1")
    try:
        check_call(["chattr", "-i", "/boot/efi/loader/loader.conf"], stdout=stderr.buffer)
    except CalledProcessError:
        eprint("CHATTR FAILED ON loader.conf, setting octal permissions to 444")
        chmod("/boot/efi/loader/loader.conf", 0o444)
    systemd_boot_config.systemd_boot_config(root)
    check_call("/etc/kernel/postinst.d/zz-update-systemd-boot", stdout=stderr.buffer)
    check_systemd_boot(release, root)


def setup_lowlevel(efi, root):
    """Set up kernel and bootloader"""
    install_kernel()
    set_plymouth_theme()
    release = check_output(["uname", "--release"]).decode()[0:-1]
    eprint("\t###\tMAKING INITRAMFS\t###\t")
    check_call(["mkinitramfs", "-o", "/boot/initrd.img-" + release], stdout=stderr.buffer)
    install_bootloader(efi, root, release)
    sleep(0.5)
    symlink("/boot/initrd.img-" + release, "/boot/initrd.img")
    symlink("/boot/vmlinuz-" + release, "/boot/vmlinuz")

def check_systemd_boot(release, root):
    """Ensure systemd-boot was configured correctly"""
    # Initialize variables
    root_flags = "quiet splash"
    recovery_flags = "ro recovery nomodeset"
    # Get Root UUID
    uuid = check_output(["blkid", "-s", "PARTUUID", "-o", "value", root]).decode()[0:-1]

    # Check for standard boot config
    if not path.exists("/boot/efi/loader/entries/Drauger_OS.conf"):
        # Write standard boot conf if it doesn't exist
        eprint("Standard Systemd-boot entry non-existant")
        try:
            with open("/boot/efi/loader/entries/Drauger_OS.conf", "w+") as main_conf:
                main_conf.write("""title   Drauger OS
linux   /Drauger_OS/vmlinuz
initrd  /Drauger_OS/initrd.img
options root=PARTUUID=%s %s""" % (uuid, root_flags))
            eprint("Made standard systemd-boot entry")
        # Raise an exception if we cannot write the entry
        except (PermissionError, IOError):
            eprint("\t###\tERROR\t###\tCANNOT MAKE STANDARD SYSTEMD-BOOT ENTRY CONFIG FILE\t###ERROR\t###\t")
            raise IOError("Cannot make standard systemd-boot entry config file. Installation will not boot.")
    else:
        eprint("Standard systemd-boot entry checks out")
    # Check for recovery boot config
    if not path.exists("/boot/efi/loader/entries/Drauger_OS_Recovery.conf"):
        eprint("Recovery Systemd-boot entry non-existant")
        try:
            # Write recovery boot conf if it doesn't exist
            with open("/boot/efi/loader/entries/Drauger_OS_Recovery.conf", "w+") as main_conf:
                main_conf.write("""title   Drauger OS Recovery
linux   /Drauger_OS/vmlinuz
initrd  /Drauger_OS/initrd.img
options root=PARTUUID=%s %s""" % (uuid, recovery_flags))
            eprint("Made recovery systemd-boot entry")
        # Raise a warning if we cannot write the entry
        except (PermissionError, IOError):
            eprint("\t###\WARNING\t###\tCANNOT MAKE RECOVERY SYSTEMD-BOOT ENTRY CONFIG FILE\t###WARNING\t###\t")
            warnings.warn("Cannot make recovery systemd-boot entry config file. Installation will not be recoverable.")
    else:
        eprint("Recovery systemd-boot entry checks out")

    # Make sure we have our kernel image, config file, initrd, and System map
    files = listdir("/boot")
    vmlinuz = []
    config = []
    initrd = []
    sysmap = []
    # Sort the files by name
    for each in files:
        if "vmlinuz-" in each:
            vmlinuz.append(each)
        elif "config-" in each:
            config.append(each)
        elif "initrd.img-" in each:
            initrd.append(each)
        elif "System.map-" in each:
            sysmap.append(each)

    # Sort the file names by version number.
    # The file with the highest index in the list is the latest version
    vmlinuz = sorted(vmlinuz)[-1]
    config = sorted(config)[-1]
    initrd = sorted(initrd)[-1]
    sysmap = sorted(sysmap)[-1]
    # Copy the latest files into place
    # Also, rename them so that systemd-boot can find them
    if not path.exists("/boot/efi/Drauger_OS/vmlinuz"):
        eprint("vmlinuz non-existant")
        copyfile("/boot/" + vmlinuz, "/boot/efi/Drauger_OS/vmlinuz")
        eprint("vmlinuz copied")
    else:
        eprint("vmlinuz checks out")
    if not path.exists("/boot/efi/Drauger_OS/config"):
        eprint("config non-existant")
        copyfile("/boot/" + config, "/boot/efi/Drauger_OS/config")
        eprint("config copied")
    else:
        eprint("Config checks out")
    if not path.exists("/boot/efi/Drauger_OS/initrd.img"):
        eprint("initrd.img non-existant")
        copyfile("/boot/" + initrd, "/boot/efi/Drauger_OS/initrd.img")
        eprint("initrd.img copied")
    else:
        eprint("initrd.img checks out")
    if not path.exists("/boot/efi/Drauger_OS/System.map"):
        eprint("System.map non-existant")
        copyfile("/boot/" + sysmap, "/boot/efi/Drauger_OS/System.map")
        eprint("System.map copied")
    else:
        eprint("System.map checks out")




def make_num(string):
    try:
        return int(string)
    except ValueError:
        return float(string)

def verify_install(username, password):
    """Fix possible bugs post-installation"""
    try:
        check_call(["/verify_install.sh", username, password], stdout=stderr.buffer)
    except PermissionError:
        chmod("/verify_install.sh", 0o777)
        check_call(["/verify_install.sh", username, password], stdout=stderr.buffer)

def install(settings, internet):
    """Entry point for installation procedure"""
    __update__(39)
    processes_to_do = dir(MainInstallation)
    for each in range(len(processes_to_do) - 1, -1, -1):
        if processes_to_do[each][0] == "_":
            del processes_to_do[each]
    settings["INTERNET"] = internet
    MainInstallation(processes_to_do, settings)
    setup_lowlevel(settings["EFI"], settings["ROOT"])
    verify_install(settings["USERNAME"], settings["PASSWORD"])

if __name__ == "__main__":
    # get length of argv
    ARGC = len(argv)
    # set vars
    # for security reasons, these are no longer environmental variables
    SETTINGS = json.loads(argv[1])
    # settings["LANG"] = argv[1]
    # settings["TIME_ZONE"] = argv[2]
    # settings["USERNAME"] = argv[3]
    # settings["PASSWORD"] = argv[4]
    # settings["COMPUTER_NAME"] = argv[5]
    # settings["EXTRAS"] = bool(int(argv[6]))
    # settings["UPDATES"] = bool(int(argv[7]))
    # settings["EFI"] = argv[8]
    # settings["ROOT"] = argv[9]
    # settings["LOGIN"] = bool(int(argv[10]))
    # settings["MODEL"] = argv[11]
    # settings["LAYOUT"] = argv[12]
    # settings["VARIENT"] = argv[13]
    # if ARGC == 15:
        # settings["SWAP"] = argv[14]
    # else:
        # settings["SWAP"] = None
    INTERNET = check_internet()

    install(SETTINGS, INTERNET)
