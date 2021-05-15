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
import subprocess
import multiprocessing
import os
from shutil import rmtree, copyfile
from inspect import getfullargspec
from time import sleep
import json
import warnings
import tarfile as tar



# import our own programs
import modules.auto_login_set as auto_login_set
import modules.make_swap as make_swap
import modules.set_time as set_time
import modules.systemd_boot_config as systemd_boot_config
import modules.set_locale as set_locale
import modules.install_updates as install_updates
import modules.make_user as mkuser
import modules.install_extras as install_extras
from modules.verify_install import verify
from modules.purge import purge_package

def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def __update__(percentage):
    try:
        with open("/tmp/system-installer-progress.log", "w+") as progress:
            progress.write(str(percentage))
    except PermissionError:
        os.chmod("/tmp/system-installer-progress.log", 0o666)
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
            globals()[each1] = multiprocessing.Process(target=process_new,
                                                       args=args)
            globals()[each1].start()
        offset = 39
        ending = 51
        iterator = round(ending / len(processes_to_do))
        # We COULD set point equal to iterator, but we don't want the iterator to change,
        # so re-doing the math is safer, albiet slower.
        point = round(ending / len(processes_to_do))
        while len(processes_to_do) > 0:
            for each in range(len(processes_to_do) - 1, -1, -1):
                if not globals()[processes_to_do[each]].is_alive():
                    globals()[processes_to_do[each]].join()
                    del processes_to_do[each]
                    __update__(point + offset)
                    point += offset

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
            os.remove("/etc/hostname")
        except FileNotFoundError:
            pass
        with open("/etc/hostname", "w+") as hostname:
            hostname.write(COMPUTER_NAME)
        try:
            os.remove("/etc/hosts")
        except FileNotFoundError:
            pass
        with open("/etc/hosts", "w+") as hosts:
            hosts.write("127.0.0.1 %s" % (COMPUTER_NAME))

    def make_user(USERNAME):
        """Set up main user"""
        mkuser.make_user(USERNAME)

    def mk_swap(SWAP):
        """Make swap file"""
        if SWAP == "FILE":
            try:
                make_swap.make_swap()
                with open("/etc/fstab", "a") as fstab:
                    fstab.write("/.swapfile\tswap\tswap\tdefaults\t0\t0")
            except IOError:
                eprint("Adding swap failed. Must manually add later")

    def apt(UPDATES, EXTRAS, INTERNET):
        """Run commands for apt sequentially to avoid front-end lock"""
        # MainInstallation.__install_updates__(UPDATES, INTERNET)
        if ((UPDATES) and (INTERNET)):
            install_updates.update_system()
        if ((EXTRAS) and (INTERNET)):
            install_extras.install_extras()

    def set_passwd(USERNAME, PASSWORD):
        """Set Root password"""
        process = subprocess.Popen("chpasswd",
                                   stdout=stderr.buffer,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate(input=bytes(r"root:%s" % (PASSWORD), "utf-8"))
        process = subprocess.Popen("chpasswd",
                                   stdout=stderr.buffer,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate(input=bytes(r"%s:%s" % (USERNAME, PASSWORD),
                                        "utf-8"))

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
            os.remove("/etc/default/keyboard")
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
        subprocess.Popen(["udevadm", "trigger", "--subsystem-match=input",
                          "--action=change"], stdout=stderr.buffer)

    def remove_launcher(USERNAME):
        """Remove system installer desktop launcher"""
        try:
            os.remove("/home/live/Desktop/system-installer.desktop")
        except FileNotFoundError:
            try:
                os.remove("/home/%s/Desktop/system-installer.desktop" % (USERNAME))
            except FileNotFoundError:
                try:
                    rmtree("/home/%s/.config/xfce4/panel/launcher-3" % (USERNAME))
                except FileNotFoundError:
                    eprint("""Cannot find launcher for system-installer.
User will need to remove manually.""")

def set_plymouth_theme():
    """Ensure the plymouth theme is set correctly"""
    subprocess.Popen(["update-alternatives", "--install",
                      "/usr/share/plymouth/themes/default.plymouth",
                      "default.plymouth",
                      "/usr/share/plymouth/themes/drauger-theme/drauger-theme.plymouth",
                      "100", "--slave",
                      "/usr/share/plymouth/themes/default.grub", "default.plymouth.grub",
                      "/usr/share/plymouth/themes/drauger-theme/drauger-theme.grub"],
                     stdout=stderr.buffer)
    process = subprocess.Popen(["update-alternatives", "--config",
                                "default.plymouth"],
                               stdout=stderr.buffer,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.communicate(input=bytes("2\n", "utf-8"))

def install_kernel(release):
    """Install kernel from kernel.tar.xz"""
    # we are going to do offline kernel installation from now on.
    # it's just easier and more reliable
    eprint("EXTRACTING KERNEL.TAR.XZ")
    tar_file = tar.open("kernel.tar.xz")
    tar_file.extractall()
    tar_file.close()
    eprint("EXTRACTION COMPLETE")
    subprocess.check_call(["apt", "purge", "-y", "linux-headers-" + release,
                           "linux-image-" + release], stdout=stderr.buffer)
    subprocess.check_call(["apt", "autoremove", "-y", "--purge"],
                          stdout=stderr.buffer)
    subprocess.check_call(["dpkg", "-R", "--install", "kernel/"],
                          stdout=stderr.buffer)
    rmtree("/kernel")


def install_bootloader(efi, root, release):
    """Determine whether bootloader needs to be systemd-boot (for UEFI)
    or GRUB (for BIOS)
    and install the correct one."""
    if efi not in ("NULL", None, "", False):
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
    subprocess.check_call(["grub-mkdevicemap", "--verbose"],
                          stdout=stderr.buffer)
    subprocess.check_call(["grub-install", "--verbose", "--force",
                           "--target=i386-pc", root], stdout=stderr.buffer)
    subprocess.check_call(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"],
                          stdout=stderr.buffer)

def _install_systemd_boot(release, root):
    """set up and install systemd-boot"""
    try:
        os.mkdir("/boot/efi")
    except FileExistsError:
        pass
    os.mkdir("/boot/efi/loader")
    os.mkdir("/boot/efi/loader/entries")
    os.mkdir("/boot/efi/Drauger_OS")
    os.environ["SYSTEMD_RELAX_ESP_CHECKS"] = "1"
    with open("/etc/environment", "a") as envi:
        envi.write("export SYSTEMD_RELAX_ESP_CHECKS=1")
    try:
        subprocess.check_call(["bootctl", "--path=/boot/efi", "install"],
                              stdout=stderr.buffer)
    except subprocess.CalledProcessError as e:
        eprint("WARNING: bootctl issued CalledProcessError:")
        eprint(e)
        eprint("Performing manual installation of systemd-boot.")
        try:
            os.mkdir("/boot/efi/EFI")
        except FileExistsError:
            pass
        try:
            os.mkdir("/boot/efi/EFI/systemd")
        except FileExistsError:
            pass
        try:
            os.mkdir("/boot/efi/EFI/BOOT")
        except FileExistsError:
            pass
        try:
            os.mkdir("/boot/efi/EFI/Linux")
        except FileExistsError:
            pass
        try:
            copyfile("/usr/lib/systemd/boot/efi/systemd-bootx64.efi",
                     "/boot/efi/EFI/BOOT/BOOTX64.EFI")
        except FileExistsError:
            pass
        try:
            copyfile("/usr/lib/systemd/boot/efi/systemd-bootx64.efi",
                     "/boot/efi/EFI/systemd/systemd-bootx64.efi")
        except FileExistsError:
            pass
    with open("/boot/efi/loader/loader.conf", "w+") as loader_conf:
        loader_conf.write("default Drauger_OS\ntimeout 5\neditor 1")
    try:
        subprocess.check_call(["chattr", "-i", "/boot/efi/loader/loader.conf"],
                              stdout=stderr.buffer)
    except subprocess.CalledProcessError:
        eprint("CHATTR FAILED ON loader.conf, setting octal permissions to 444")
        os.chmod("/boot/efi/loader/loader.conf", 0o444)
    systemd_boot_config.systemd_boot_config(root)
    subprocess.check_call("/etc/kernel/postinst.d/zz-update-systemd-boot",
                          stdout=stderr.buffer)
    check_systemd_boot(release, root)


def setup_lowlevel(efi, root):
    """Set up kernel and bootloader"""
    release = subprocess.check_output(["uname", "--release"]).decode()[0:-1]
    install_kernel(release)
    set_plymouth_theme()
    __update__(91)
    eprint("\n    ###    MAKING INITRAMFS    ###    ")
    subprocess.check_call(["mkinitramfs", "-o", "/boot/initrd.img-" + release],
                          stdout=stderr.buffer)
    install_bootloader(efi, root, release)
    sleep(0.5)
    os.symlink("/boot/initrd.img-" + release, "/boot/initrd.img")
    os.symlink("/boot/vmlinuz-" + release, "/boot/vmlinuz")

def check_systemd_boot(release, root):
    """Ensure systemd-boot was configured correctly"""
    # Initialize variables
    root_flags = "quiet splash"
    recovery_flags = "ro recovery nomodeset"
    # Get Root UUID
    uuid = subprocess.check_output(["blkid", "-s", "PARTUUID",
                                    "-o", "value", root]).decode()[0:-1]

    # Check for standard boot config
    if not os.path.exists("/boot/efi/loader/entries/Drauger_OS.conf"):
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
            eprint("    ###    ERROR    ###    CANNOT MAKE STANDARD SYSTEMD-BOOT ENTRY CONFIG FILE    ###    ERROR    ###    ")
            raise IOError("Cannot make standard systemd-boot entry config file. Installation will not boot.")
    else:
        eprint("Standard systemd-boot entry checks out")
    # Check for recovery boot config
    if not os.path.exists("/boot/efi/loader/entries/Drauger_OS_Recovery.conf"):
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
            eprint("    ###    WARNING    ###    CANNOT MAKE RECOVERY SYSTEMD-BOOT ENTRY CONFIG FILE    ###    WARNING    ###    ")
            warnings.warn("Cannot make recovery systemd-boot entry config file. Installation will not be recoverable.")
    else:
        eprint("Recovery systemd-boot entry checks out")

    # Make sure we have our kernel image, config file, initrd, and System map
    files = os.listdir("/boot")
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
    if not os.path.exists("/boot/efi/Drauger_OS/vmlinuz"):
        eprint("vmlinuz non-existant")
        copyfile("/boot/" + vmlinuz, "/boot/efi/Drauger_OS/vmlinuz")
        eprint("vmlinuz copied")
    else:
        eprint("vmlinuz checks out")
    if not os.path.exists("/boot/efi/Drauger_OS/config"):
        eprint("config non-existant")
        copyfile("/boot/" + config, "/boot/efi/Drauger_OS/config")
        eprint("config copied")
    else:
        eprint("Config checks out")
    if not os.path.exists("/boot/efi/Drauger_OS/initrd.img"):
        eprint("initrd.img non-existant")
        copyfile("/boot/" + initrd, "/boot/efi/Drauger_OS/initrd.img")
        eprint("initrd.img copied")
    else:
        eprint("initrd.img checks out")
    if not os.path.exists("/boot/efi/Drauger_OS/System.map"):
        eprint("System.map non-existant")
        copyfile("/boot/" + sysmap, "/boot/efi/Drauger_OS/System.map")
        eprint("System.map copied")
    else:
        eprint("System.map checks out")

def _check_for_laptop():
    """Check if the device we are installing is a laptop.
    Returns True if it is a laptop, returns False otherwise.
    """
    try:
        subprocess.check_call(["laptop-detect"])
    except subprocess.CalledProcessError:
        return False
    return True


def handle_laptops(username):
    """Remove the battery icon from the panel on desktops"""
    if not _check_for_laptop():
        eprint("DESKTOP DETECTED. EDITING PANEL ACCORDINGLY.")
        try:
            os.remove("/home/" + username + "/.config/xfce4/panel/battery-12.rc")
        except FileNotFoundError:
            pass
        with open("/home/" + username + "/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml", "r") as file:
            xml = file.read().split("\n")
        for each in range(len(xml) - 1, -1, -1):
            if "battery" in xml[each]:
                del xml[each]
        xml = "\n".join(xml)
        with open("/home/" + username + "/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml", "w") as file:
            file.write(xml)


def install(settings):
    """Entry point for installation procedure"""
    processes_to_do = dir(MainInstallation)
    for each in range(len(processes_to_do) - 1, -1, -1):
        if processes_to_do[each][0] == "_":
            del processes_to_do[each]
    MainInstallation(processes_to_do, settings)
    handle_laptops(settings["USERNAME"])
    setup_lowlevel(settings["EFI"], settings["ROOT"])
    verify(settings["USERNAME"], settings["PASSWORD"])
    if "PURGE" in settings:
        purge_package(settings["PURGE"])

if __name__ == "__main__":
    # get length of argv
    ARGC = len(argv)
    # set vars
    # for security reasons, these are no longer environmental variables
    SETTINGS = json.loads(argv[1])

    install(SETTINGS)
