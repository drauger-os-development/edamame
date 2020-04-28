#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  MASTER.py
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
from sys import argv, stderr, version_info
from subprocess import Popen, PIPE, check_output
import multiprocessing
from os import remove, mkdir, environ, symlink
from shutil import rmtree
import urllib3

# import our own programs
import auto_login_set
import make_swap
import set_time
import systemd_boot_config
import set_locale

# Make it easier for us to print to stderr
def eprint(*args, **kwargs):
	print(*args, file=stderr, **kwargs)

# define this later
def check_internet():
	try:
		urllib3.urlopen('http://draugeros.org', timeout=1)
		return True
	except:
		return False

# get length of argv
argc = len(argv)
# set vars
# for security reasons, these are no longer environmental variables
LANG_SET = argv[1]
TIME_ZONE = argv[2]
USERNAME = argv[3]
PASSWORD = argv[4]
COMP_NAME = argv[5]
EXTRAS = bool(int(argv[6]))
UPDATES = bool(int(argv[7]))
EFI = argv[8]
ROOT = argv[9]
LOGIN = argv[10]
MODEL = argv[11]
LAYOUT = argv[12]
VARIENT = argv[13]
if (argc == 15):
	SWAP = argv[14]
else:
	SWAP = None
internet = check_internet()

print(39)

class main_installation():

	def time_set(self):
		global TIME_ZONE
		set_time.set_time(TIME_ZONE)

	def locale_set(self):
		global LANG_SET
		set_locale.set_locale(LANG_SET)

	def set_networking(self):
		global COMP_NAME
		eprint("Setting hostname to %s" % (COMP_NAME))
		try:
			remove("/etc/hostname")
		except FileNotFoundError:
			pass
		with open("/etc/hostname", "w+") as hostname:
			hostname.write(COMP_NAME)
		try:
			remove("/etc/hosts")
		except FileNotFoundError:
			pass
		with open("/etc/hosts", "w+") as hosts:
			hosts.write("127.0.0.1 %s" % (COMP_NAME))
		print(48)

	def make_user(self):
		# This needs to be set up in Python. Leave it in shell for now
		Popen("/make_user.sh")

	def mk_swap(self):
		global SWAP
		if (SWAP == "FILE"):
			try:
				make_swap.make_swap()
				with open("/etc/fstab", "a") as fstab:
					fstab.write("/.swapfile	swap	swap	defaults	0	0")
			except:
				eprint("Adding swap failed. Must manually add later")
		print(66)

	def install_updates(self):
		global UPDATES
		global internet
		if ((UPDATES) and (internet)):
			Popen("/install_updates.sh")
		elif (not internet):
			eprint("Cannot install updates. No internet.")

	def install_extras(self):
		global EXTRAS
		global internet
		if ((EXTRAS) and (internet)):
			Popen("/install_extras.sh")
		elif (not internet):
			eprint("Cannot install extras. No internet.")

	def set_passwd(self):
		print(84)
		global PASSWORD
		process = Popen("chpasswd", stdout=stderr.buffer, stdin=PIPE, stderr=PIPE)
		process.communicate(input=bytes(r"root:%s" % (PASSWORD), "utf-8"))
		print(85)

	def lightdm_config(self):
		global LOGIN
		global USERNAME
		auto_login_set.auto_login_set(LOGIN, USERNAME)

	def set_keyboard(self):
		global MODEL
		global LAYOUT
		global VARIENT
		with open("/usr/share/X11/xkb/rules/base.lst", "r") as xkb_conf:
			KEYBOARD_CONFIG_DATA = xkb_conf.read()
		KEYBOARD_CONFIG_DATA = KEYBOARD_CONFIG_DATA.split("\n")
		for each in range(len(KEYBOARD_CONFIG_DATA)):
			KEYBOARD_CONFIG_DATA[each] = KEYBOARD_CONFIG_DATA[each].split()
		try:
			remove("/etc/default/keyboard")
		except FileNotFoundError:
			pass
		XKBMODEL = ""
		XKBLAYOUT = ""
		XKBVARIENT = ""
		for each in KEYBOARD_CONFIG_DATA:
			if (" ".join(each[1:]) == MODEL):
				XKBMODEL = each[0]
			elif (" ".join(each[1:]) == LAYOUT):
				XKBLAYOUT = each[0]
			elif (" ".join(each[1:]) == VARIENT):
				XKBVARIENT = each[0]
		with open("/etc/default/keyboard", "w+") as xkb_default:
			xkb_default.write("XKBMODEL=\"%s\"\nXKBLAYOUT=\"%s\"\nXKBVARIANT=\"%s\"\nXKBOPTIONS=\"\"\n\nBACKSPACE=\"guess\"\n" % (XKBMODEL, XKBLAYOUT, XKBVARIENT))
		print(90)
		Popen(["udevadm", "trigger", "--subsystem-match=input", "--action=change"], stdout=stderr.buffer)

	def set_plymouth_theme(self):
		Popen(["update-alternatives", "--install", "/usr/share/plymouth/themes/default.plymouth", "default.plymouth", "/usr/share/plymouth/themes/drauger-theme/drauger-theme.plymouth", "100", "--slave", "/usr/share/plymouth/themes/default.grub", "default.plymouth.grub", "/usr/share/plymouth/themes/drauger-theme/drauger-theme.grub"], stdout=stderr.buffer)
		process = Popen(["update-alternatives", "--config", "default.plymouth"], stdout=stderr.buffer, stdin=PIPE, stderr=PIPE)
		process.communicate(input=bytes("2\n", "utf-8"))
		print(86)

	def remove_launcher(self):
		global USERNAME
		try:
			remove("/home/%s/Desktop/system-installer.desktop" % (USERNAME))
		except FileNotFoundError:
			try:
				rmtree("/home/%sE/.config/xfce4/panel/launcher-3" % (USERNAME))
			except FileNotFoundError:
				eprint("Cannot find launcher for system-installer. User will need to remove manually.")

def install_kernel():
	# we are going to do offline kernel installation from now on.
	# it's just easier and more reliable
	Popen(["7z", "x", "/kernel.7z"], stdout=stderr.buffer)
	Popen(["apt", "purge", "-y", "linux-headers-drauger", "linux-image-drauger"], stdout=stderr.buffer)
	Popen(["apt", "autoremove", "-y", "--purge"], stdout=stderr.buffer)
	Popen(["dpkg", "-R", "--install", "kernel/"], stdout=stderr.buffer)
	rmtree("/kernel")


def install_bootloader():
	global EFI
	if (EFI != "NULL"):
		_install_systemd_boot()
	else:
		_install_GRUB()

def _install_GRUB():
	global ROOT
	ROOT = list(ROOT)
	for each in range(len(ROOT) - 1, -1, -1):
		try:
			int(ROOT[each])
			del(ROOT[each])
		except ValueError:
			break
	if (ROOT[len(ROOT) - 1] == "p"):
		del(ROOT[len(ROOT) - 1])
	ROOT = "".join(ROOT)
	Popen(["grub-mkdevicemap", "--verbose"], stdout=stderr.buffer)
	Popen(["grub-install", "--verbose", "--force", "--target=i386-pc", ROOT], stdout=stderr.buffer)
	Popen(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"], stdout=stderr.buffer)

def _install_systemd_boot():
	global ROOT
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
	Popen(["bootctl", "--path=/boot/efi", "install"], stdout=stderr.buffer)
	with open("/boot/efi/loader/loader.conf", "w+") as loader_conf:
		loader_conf.write("default Drauger_OS\ntimeout 5\neditor 1")
	Popen(["chattr", "-i", "/boot/efi/loader/loader.conf"], stdout=stderr.buffer)
	systemd_boot_config.systemd_boot_config(ROOT)
	Popen("/etc/kernel/postinst.d/zz-update-systemd-boot", stdout=stderr.buffer)


def setup_lowlevel():
	install_kernel()
	install_bootloader()
	release = list(str(check_output(["uname", "--release"])))
	del(release[0:2])
	del(release[len(release) - 3:])
	release = "".join(release)
	symlink("/boot/initrd.img-" + release, "/boot/initrd.img")
	symlink("/boot/vmlinuz-" + release, "/boot/vmlinuz")

def verify_install():
	Popen(["/verify_install.sh"], stdout=stderr.buffer)


