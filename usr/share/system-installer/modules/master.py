#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  master.py
#
#  Copyright 2023 Thomas Castleman <batcastle@draugeros.org>
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
import subprocess as subproc
import multiprocessing
import os
from shutil import rmtree, copyfile
from inspect import getfullargspec
from time import sleep
import json
import warnings
import tarfile as tar
import traceback
import de_control.modify as de_modify


# import our own programs
import modules.auto_login_set as auto_login_set
import modules.make_swap as make_swap
import modules.set_time as set_time
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
        # We COULD set point equal to iterator, but we don't want the iterator
        # to change, so re-doing the math is safer, albiet slower.
        point = round(ending / len(processes_to_do))
        while len(processes_to_do) > 0:
            for each in range(len(processes_to_do) - 1, -1, -1):
                if not globals()[processes_to_do[each]].is_alive():
                    globals()[processes_to_do[each]].join()
                    del processes_to_do[each]
                    __update__(point + offset)
                    point += iterator

    def time_set(TIME_ZONE):
        """Set system time"""
        if TIME_ZONE != "OEM":
            set_time.set_time(TIME_ZONE)

    def locale_set(LANG):
        """Set system locale"""
        if LANG != "OEM":
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

    def apt(UPDATES, EXTRAS):
        """Run commands for apt sequentially to avoid front-end lock"""
        # MainInstallation.__install_updates__(UPDATES, INTERNET)
        if UPDATES:
            install_updates.update_system()
        if EXTRAS:
            install_extras.install_extras()

    def set_passwd(USERNAME, PASSWORD):
        """Set password for Root and User"""
        if PASSWORD == "OEM":
            PASSWORD = "toor"
        if USERNAME != "drauger-user":
            process = subproc.Popen("chpasswd",
                                       stdout=stderr.buffer,
                                       stdin=subproc.PIPE,
                                       stderr=subproc.PIPE)
            process.communicate(input=bytes(r"root:%s" % (PASSWORD), "utf-8"))

        process = subproc.Popen("chpasswd",
                                   stdout=stderr.buffer,
                                   stdin=subproc.PIPE,
                                   stderr=subproc.PIPE)
        process.communicate(input=bytes(r"%s:%s" % (USERNAME, PASSWORD),
                                        "utf-8"))

    def lightdm_config(LOGIN, USERNAME):
        """Set autologin setting for lightdm"""
        auto_login_set.auto_login_set(LOGIN, USERNAME)

    def set_keyboard(MODEL, LAYOUT, VARIENT):
        """Set keyboard model, layout, and varient"""
        if MODEL != "OEM":
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
                if len(each1) < 1:
                    continue
                if each1[0] == MODEL:
                    xkbm = MODEL
                elif each1[0] == LAYOUT:
                    xkbl = LAYOUT
                elif each1[0] == VARIENT:
                    xkbv = VARIENT
            if "" == xkbm:
                print(f"{MODEL} not in XKeyboard Rules List. Invalid.")
            if "" == xkbl:
                print(f"{LAYOUT} not in XKeyboard Rules List. Invalid.")
            if "" == xkbv:
                print(f"{VARIENT} not in XKeyboard Rules List. Invalid.")
            xkb_file = f"""XKBMODEL=\"{xkbm}\"
XKBLAYOUT=\"{xkbl}\"
XKBVARIANT=\"{xkbv}\"
XKBOPTIONS=\"\"

BACKSPACE=\"guess\"
"""
            with open("/etc/default/keyboard", "w+") as xkb_default:
                xkb_default.write(xkb_file)
            subproc.Popen(["udevadm", "trigger", "--subsystem-match=input",
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
    data = subproc.check_output(["update-alternatives","--query",
                                 "default.plymouth"]).decode().split("\n")
    data = [each for each in data if "Value:" in each][0].split()[1]
    if "drauger-theme.plymouth" != data.split("/")[-1]:
        subproc.Popen(["update-alternatives", "--install",
                       "/usr/share/plymouth/themes/default.plymouth",
                       "default.plymouth",
                       "/usr/share/plymouth/themes/drauger-theme/drauger-theme.plymouth",
                       "100", "--slave",
                       "/usr/share/plymouth/themes/default.grub",
                       "default.plymouth.grub",
                       "/usr/share/plymouth/themes/drauger-theme/drauger-theme.grub"],
                      stdout=stderr.buffer)
        process = subproc.Popen(["update-alternatives", "--config",
                                 "default.plymouth"],
                                stdout=stderr.buffer,
                                stdin=subproc.PIPE,
                                stderr=subproc.PIPE)
        process.communicate(input=bytes("2\n", "utf-8"))


def install_kernel(release):
    """Install kernel from kernel.tar.xz"""
    # we are going to do offline kernel installation from now on.
    # it's just easier and more reliable
    packages = ["linux-headers-" + release, "linux-image-" + release]
    install_command = ["dpkg", "--install"]
    subproc.check_call(["dpkg", "-P", "--force-all"] + packages,
                       stdout=stderr.buffer)
    packages = [each for each in os.listdir("/repo") if "linux-" in each]
    os.chdir("/repo")
    subproc.check_call(install_command + packages, stdout=stderr.buffer)
    os.chdir("/")
    try:
        subproc.check_call(["apt-get", "autopurge", "-y"],
                           stdout=stderr.buffer)
    except subproc.CalledProcessError:
        eprint("WARNING: Clean up post-kernel install failed. This will likely be fixed later.")


def install_bootloader(efi, root, release, distro, compat_mode):
    """Determine whether bootloader needs to be systemd-boot (for UEFI)
    or GRUB (for BIOS)
    and install the correct one."""
    if efi not in ("NULL", None, "", False):
        _install_systemd_boot(release, root, distro, compat_mode)
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
    redo = False
    os.mkdir("/boot/grub")
    try:
        subproc.check_call(["grub-mkdevicemap", "--verbose"],
                              stdout=stderr.buffer)
    except subproc.CalledProcessError:
        redo = True
    subproc.check_call(["grub-install", "--verbose", "--force",
                           "--target=i386-pc", root], stdout=stderr.buffer)
    if redo:
        try:
            subproc.check_call(["grub-mkdevicemap", "--verbose"],
                                  stdout=stderr.buffer)
        except subproc.CalledProcessError as e:
            eprint("WARNING: GRUB device map failed to generate")
            eprint("The error was as follows:")
            eprint(traceback.format_exeception())
    subproc.check_call(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"],
                          stdout=stderr.buffer)


def _install_systemd_boot(release, root, distro, compat_mode):
    """set up and install systemd-boot"""
    install_command = ["dpkg", "--install"]
    try:
        os.makedirs("/boot/efi/loader/entries", exist_ok=True)
    except FileExistsError:
        pass
    try:
        os.mkdir(f"/boot/efi/{distro}")
    except FileExistsError:
        pass
    os.environ["SYSTEMD_RELAX_ESP_CHECKS"] = "1"
    with open("/etc/environment", "a") as envi:
        envi.write("export SYSTEMD_RELAX_ESP_CHECKS=1")
    try:
        subproc.check_call(["bootctl", "--path=/boot/efi", "install"],
                              stdout=stderr.buffer)
    except subproc.CalledProcessError as e:
        eprint("WARNING: bootctl issued CalledProcessError:")
        eprint(e)
        eprint("Performing manual installation of systemd-boot.")
        try:
            os.makedirs("/boot/efi/EFI/systemd", exist_ok=True)
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
    except FileNotFoundError:
        # using new installation method
        packages = [each for each in os.listdir("/repo") if ("systemd-boot" in each) and ("manager" not in each)]
        os.chdir("/repo")
        depends = subproc.check_output(["dpkg", "-f"] + packages + ["depends"])
        depends = depends.decode()[:-1].split(", ")
        depends = [depends[each[0]].split(" ")[0] for each in enumerate(depends)]
        for each in os.listdir():
            for each1 in depends:
                if ((each1 in each) and (each not in packages)):
                    packages.append(each)
                    break
        subproc.check_call(install_command + packages,
                           stdout=stderr.buffer)
    packages = [each for each in os.listdir("/repo") if "systemd-boot-manager" in each]
    os.chdir("/repo")
    depends = subproc.check_output(["dpkg", "-f"] + packages + ["depends"])
    depends = depends.decode()[:-1].split(", ")
    # List of dependencies
    depends = [depends[each[0]].split(" ")[0] for each in enumerate(depends)]
    # depends is just a list of package names. We now need to go through the list
    # of files in this folder, and if the package name is in the file name, add
    # it to the list `packages`
    for each in os.listdir():
        for each1 in depends:
            if ((each1 in each) and (each not in packages)):
                packages.append(each)
                break
    subproc.check_call(install_command + packages,
                          stdout=stderr.buffer)
    os.chdir("/")
    if compat_mode:
        subproc.check_call(["systemd-boot-manager", "--compat-mode=enable"],
                              stdout=stderr.buffer)
    subproc.check_call(["systemd-boot-manager", "-e"],
                          stdout=stderr.buffer)
    subproc.check_call(["systemd-boot-manager", "--apply-loader-config"],
                          stdout=stderr.buffer)
    subproc.check_call(["systemd-boot-manager", "-r"],
                          stdout=stderr.buffer)
    subproc.check_call(["systemd-boot-manager",
                           "--enforce-default-entry=enable"],
                          stdout=stderr.buffer)
    # This lib didn't exist before we installed this package.
    # So we can only now import it
    import systemd_boot_manager
    systemd_boot_manager.update_defaults_file(distro + ".conf")
    subproc.check_call(["systemd-boot-manager", "-u"],
                          stdout=stderr.buffer)
    check_systemd_boot(release, root, distro)


def setup_lowlevel(efi, root, distro, compat_mode):
    """Set up kernel and bootloader"""
    release = subproc.check_output(["uname", "--release"]).decode()[0:-1]
    eprint(f"Running kernel: { release }")
    install_kernel(release)
    set_plymouth_theme()
    __update__(91)
    eprint("\n    ###    MAKING INITRAMFS    ###    ")
    subproc.check_call(["mkinitramfs", "-o", "/boot/initrd.img-" + release],
                          stdout=stderr.buffer)
    install_bootloader(efi, root, release, distro, compat_mode)
    sleep(0.5)
    os.symlink("/boot/initrd.img-" + release, "/boot/initrd.img")
    os.symlink("/boot/vmlinuz-" + release, "/boot/vmlinuz")


def check_systemd_boot(release, root, distro):
    """Ensure systemd-boot was configured correctly"""
    # Initialize variables
    root_flags = "quiet splash"
    recovery_flags = "ro recovery nomodeset"
    # Get Root UUID
    uuid = subproc.check_output(["blkid", "-s", "PARTUUID",
                                    "-o", "value", root]).decode()[0:-1]

    # Check for standard boot config
    if not os.path.exists(f"/boot/efi/loader/entries/{distro}.conf"):
        # Write standard boot conf if it doesn't exist
        eprint("Standard Systemd-boot entry non-existant")
        try:
            with open(f"/boot/efi/loader/entries/{distro}.conf",
                      "w+") as main_conf:
                main_conf.write(f"""title   {distro}
linux   /{distro}/vmlinuz
initrd  /{distro}/initrd.img
options root=PARTUUID=%s %s""" % (uuid, root_flags))
            eprint("Made standard systemd-boot entry")
        # Raise an exception if we cannot write the entry
        except (PermissionError, IOError):
            eprint("    ###    ERROR    ###    CANNOT MAKE STANDARD SYSTEMD-BOOT ENTRY CONFIG FILE    ###    ERROR    ###    ")
            raise IOError("Cannot make standard systemd-boot entry config file. Installation will not boot.")
    else:
        eprint("Standard systemd-boot entry checks out")
    # Check for recovery boot config
    if not os.path.exists(f"/boot/efi/loader/entries/{distro}_Recovery.conf"):
        eprint("Recovery Systemd-boot entry non-existant")
        try:
            # Write recovery boot conf if it doesn't exist
            with open(f"/boot/efi/loader/entries/{distro}_Recovery.conf",
                      "w+") as main_conf:
                main_conf.write(f"""title   {distro}_Recovery
linux   /{distro}/vmlinuz
initrd  /{distro}/initrd.img
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
    if not os.path.exists(f"/boot/efi/{distro}/vmlinuz"):
        eprint("vmlinuz non-existant")
        copyfile("/boot/" + vmlinuz, f"/boot/efi/{distro}/vmlinuz")
        eprint("vmlinuz copied")
    else:
        eprint("vmlinuz checks out")
    if not os.path.exists(f"/boot/efi/{distro}/config"):
        eprint("config non-existant")
        copyfile("/boot/" + config, f"/boot/efi/{distro}/config")
        eprint("config copied")
    else:
        eprint("Config checks out")
    if not os.path.exists(f"/boot/efi/{distro}/initrd.img"):
        eprint("initrd.img non-existant")
        copyfile("/boot/" + initrd, f"/boot/efi/{distro}/initrd.img")
        eprint("initrd.img copied")
    else:
        eprint("initrd.img checks out")
    if not os.path.exists(f"/boot/efi/{distro}/System.map"):
        eprint("System.map non-existant")
        copyfile("/boot/" + sysmap, f"/boot/efi/{distro}/System.map")
        eprint("System.map copied")
    else:
        eprint("System.map checks out")


def _check_for_laptop():
    """Check if the device we are installing is a laptop.
    Returns True if it is a laptop, returns False otherwise.
    """
    try:
        subproc.check_call(["/usr/bin/laptop-detect"])
    except subproc.CalledProcessError:
        return False
    except FileNotFoundError:
        eprint("WARNING: Cannot determine if machine is laptop or desktop. Assuming Desktop...")
        return False
    return True


def handle_laptops(username):
    """Remove the battery icon from the panel on desktops"""
    if not _check_for_laptop():
        de_modify.for_desktop(username)
    else:
        de_modify.for_laptop()


def install(settings, distro):
    """Entry point for installation procedure"""
    processes_to_do = dir(MainInstallation)
    for each in range(len(processes_to_do) - 1, -1, -1):
        if processes_to_do[each][0] == "_":
            del processes_to_do[each]
    MainInstallation(processes_to_do, settings)
    handle_laptops(settings["USERNAME"])
    setup_lowlevel(settings["EFI"], settings["ROOT"], distro,
                   settings["COMPAT_MODE"])
    verify(settings["USERNAME"], settings["ROOT"], distro)
    if "PURGE" in settings:
        purge_package(settings["PURGE"])
    # Mark a system as an OEM installation if necessary
    if "OEM" in settings.values():
        with open("/etc/system-installer/oem-post-install.flag", "w") as file:
            file.write("")


if __name__ == "__main__":
    # get length of argv
    ARGC = len(argv)
    # set vars
    # for security reasons, these are no longer environmental variables
    SETTINGS = json.loads(argv[1])

    install(SETTINGS)
