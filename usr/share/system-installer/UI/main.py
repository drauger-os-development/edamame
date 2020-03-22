#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import re
from subprocess import Popen, check_output, DEVNULL
from os import getcwd, chdir, path, listdir
from sys import stderr

def eprint(*args, **kwargs):
	print(*args, file=stderr, **kwargs)

def hasSC(inputString):
	regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
	if regex.search(inputString) == None:
		return False
	else:
		return True

def hasspace(inputString):
	x=0
	for a in inputString:
		if (a.isspace()) == True:
			x=1
			break
		else:
			x=0
	if x == 1:
		return True
	else:
		return False


try:
	config_dir = listdir("/etc/system-installer")
	for each in range(len(config_dir)):
		if (config_dir[each] == "quick-install-template.config"):
			del(config_dir[each])
			if (len(config_dir) == 1):
				break
			else:
				for each1 in range(len(config_dir)):
					if (config_dir[each1] == "default.config"):
						del(config_dir[each])
						if (len(config_dir) != 1):
							eprint("More than one custom config file in /etc/system-installer is not supported.")
							eprint("Please remove all but one and try again.")
							eprint("'default.config' and 'quick-install-template.config' may remain though.")
							exit(2)
						else:
							break
				break
	with open("/etc/system-installer/%s" % (config_dir[0])) as config_file:
		config = config_file.read()

	config = config.split("\n")
	while("" in config) :
		config.remove("")
	for each in range(len(config)):
		config[each] = config[each].split("=")
	for each in config:
		if ((each[0] == "distro") or (each[0] == "Distro") or (each[0] == "DISTRO")):
			DISTRO = each[1]

	DISTRO = DISTRO.split("_")
	DISTRO = " ".join(DISTRO)
except:
	eprint("/etc/system-installer does not exist. In testing?")
	DISTRO = "Drauger OS"




default = """
	Welcome to the %s System Installer!

	A few things before we get started:

	<b>PARTITIONING</b>

	The %s System Installer uses Gparted to allow the user to set up their partitions
	It is advised to account for this if installing next to another OS.
	If using automatic partitoning, it will take up the entirety of the drive told to use.
	Loss of data from usage of this tool is entirely at the fault of the user.
	You have been warned.

	<b>ALPHA WARNING</b>

	The %s System Installer is currently in alpha.
	Expect bugs.
	""" % (DISTRO, DISTRO, DISTRO)

keyboard_completion = "TO DO"
user_completion = "TO DO"
part_completion = "TO DO"
locale_completion = "TO DO"
options_completion = "TO DO"

class main(Gtk.Window):
	def __init__(self):
		# Initialize the Window
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)
		self.set_icon_from_file("/usr/share/icons/Drauger/720x720/Menus/install-drauger.png")

		# Initialize setting values
		self.root_setting = ""
		self.efi_setting = ""
		self.home_setting = ""
		self.swap_setting = ""
		self.auto_part_setting = ""
		self.lang_setting = ""
		self.time_zone = ""
		self.username_setting = ""
		self.compname_setting = ""
		self.password_setting = ""
		self.extras_setting = ""
		self.updates_setting = ""
		self.login_setting = ""
		self.model_setting = ""
		self.layout_setting = ""
		self.varient_setting = ""

		# Open initial window
		self.reset("clicked")

	def quick_install_warning(self,button):
		self.label.set_markup("""
	<b>QUICK INSTALL MODE INITIATED</b>

	You have activated Quick Install mode.

	This mode allows users to provide the system installation utility with
	a config file containing their prefrences for installation and set up.

	An example of one of these can be found at /etc/system-installer/quick-install-template.conf\t
	""")

		self.grid.remove(self.button1)

		self.button4 = Gtk.Button.new_with_label("Select Config File")
		self.button4.connect("clicked", self.select_config)
		self.grid.attach(self.button4, 3, 2, 1, 1)

		self.button3.set_label("<-- Back")
		self.button3.connect("clicked", self.reset)

		self.show_all()

	def reset(self,button):
		self.clear_window()

		self.label = Gtk.Label()
		self.label.set_markup(default)
		self.label.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.main_menu)
		self.grid.attach(self.button1, 3, 2, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.exit)
		self.grid.attach(self.button2, 1, 2, 1, 1)

		self.button3 = Gtk.Button.new_with_label("Quick Install")
		self.button3.connect("clicked", self.quick_install_warning)
		self.grid.attach(self.button3, 2, 2, 1, 1)

		self.show_all()

	def select_config(self,widget):
		dialog = Gtk.FileChooserDialog("System Installer", self,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		self.add_filters(dialog)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print(dialog.get_filename())
			exit(0)
		elif response == Gtk.ResponseType.CANCEL:
			exit(2)

		dialog.destroy()

	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Test")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)

		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)

	def main_menu(self,button):
		self.clear_window()

		self.label.set_markup("""
		Feel free to complete any of the below segments in any order.\t
		However, all segments must be completed.\n""")
		self.grid.attach(self.label, 2, 1, 2, 1)

		self.completion_label = Gtk.Label()
		self.completion_label.set_markup("""<b>COMPLETION</b>""")
		self.grid.attach(self.completion_label, 2, 2, 1, 1)

		self.button8 = Gtk.Button.new_with_label("Keyboard")
		self.button8.connect("clicked",self.keyboard)
		self.grid.attach(self.button8, 3, 3, 1, 1)

		self.label_keyboard = Gtk.Label()
		self.label_keyboard.set_markup(keyboard_completion)
		self.grid.attach(self.label_keyboard, 2, 3, 1, 1)

		self.button4 = Gtk.Button.new_with_label("Locale and Time")
		self.button4.connect("clicked",self.locale)
		self.grid.attach(self.button4, 3, 4, 1, 1)

		self.label_locale = Gtk.Label()
		self.label_locale.set_markup(locale_completion)
		self.grid.attach(self.label_locale, 2, 4, 1, 1)

		self.button5 = Gtk.Button.new_with_label("Options")
		self.button5.connect("clicked",self.options)
		self.grid.attach(self.button5, 3, 5, 1, 1)

		self.label_options = Gtk.Label()
		self.label_options.set_markup(options_completion)
		self.grid.attach(self.label_options, 2, 5, 1, 1)

		self.button6 = Gtk.Button.new_with_label("Partitioning")
		self.button6.connect("clicked",self.partitioning)
		self.grid.attach(self.button6, 3, 6, 1, 1)

		self.label_part = Gtk.Label()
		self.label_part.set_markup(part_completion)
		self.grid.attach(self.label_part, 2, 6, 1, 1)

		self.button7 = Gtk.Button.new_with_label("User Settings")
		self.button7.connect("clicked",self.user)
		self.grid.attach(self.button7, 3, 7, 1, 1)

		self.label_user = Gtk.Label()
		self.label_user.set_markup(user_completion)
		self.grid.attach(self.label_user, 2, 7, 1, 1)

		self.button1.set_label("DONE")
		self.button1.connect("clicked",self.done)
		self.grid.attach(self.button1, 4, 8, 1, 1)

		self.grid.attach(self.button2, 1, 8, 1, 1)

		self.show_all()

	def user(self,button):
		self.clear_window()

		self.label = Gtk.Label()
		self.label.set_markup("""
	<b>Set Up Main User</b>
		""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 2, 1)

		self.label1 = Gtk.Label()
		self.label1.set_markup("	Username:	")
		self.label1.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label1, 1, 3, 1, 1)

		self.username = Gtk.Entry()
		self.username.set_text(self.username_setting)
		self.grid.attach(self.username, 2, 3, 1, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("	Computer\'s Name:	")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 1, 4, 1, 1)

		self.compname = Gtk.Entry()
		self.compname.set_text(self.compname_setting)
		self.grid.attach(self.compname, 2, 4, 1, 1)

		self.label3 = Gtk.Label()
		self.label3.set_markup("	Password:	")
		self.label3.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label3, 1, 5, 1, 1)

		self.password = Gtk.Entry()
		self.password.set_visibility(False)
		self.password.set_text(self.password_setting)
		self.grid.attach(self.password, 2, 5, 1, 1)

		self.label4 = Gtk.Label()
		self.label4.set_markup("	Confirm Pasword:	")
		self.label4.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label4, 1, 6, 1, 1)

		self.passconf = Gtk.Entry()
		self.passconf.set_visibility(False)
		self.passconf.set_text(self.password_setting)
		self.grid.attach(self.passconf, 2, 6, 1, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnext2clicked)
		self.grid.attach(self.button1, 2, 8, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.exit)
		self.grid.attach(self.button2, 1, 8, 1, 1)

		self.label5 = None

		self.show_all()

	def onnext2clicked(self,button):
		self.password_setting = self.password.get_text()
		pass2 = self.passconf.get_text()
		self.username_setting = self.username.get_text()
		self.username_setting = self.username_setting.lower()
		self.compname_setting = self.compname.get_text()
		if self.password_setting != pass2:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Passwords do not match")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif len(self.password_setting) < 4:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Password is less than 4 characters")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasSC(self.username_setting):
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Username contains special characters")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasspace(self.username_setting):
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Username contains space")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif len(self.username_setting) < 1:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Username empty")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasSC(self.compname_setting):
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Computer Name contains non-hyphen special character")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasspace(self.compname_setting):
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Computer Name contains space")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif len(self.compname_setting) < 1:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Computer Name is empty")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		else:
			global user_completion
			user_completion = "COMPLETED"
			self.main_menu("clicked")

		self.show_all()

	def partitioning(self,button):
		self.clear_window()

		self.label = Gtk.Label()
		self.label.set_markup("""
	Would you like to let %s automaticly partition a drive for installation?\t
	Or, would you like to manually partition space for it?\t

	<b>NOTE</b>
	Auto partitioning takes up an entire drive. If you are uncomfortable with this,\t
	please either manually partition your drive, or abort installation now.\t
	""" % (DISTRO))
		self.label.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label, 1, 1, 5, 1)

		self.link = Gtk.Button.new_with_label("Manual Partitioning")
		self.link.connect("clicked", self.opengparted)
		self.grid.attach(self.link, 3, 5, 1, 1)

		self.button1 = Gtk.Button.new_with_label("Automatic Partitioning")
		self.button1.connect("clicked", self.auto_partition)
		self.grid.attach(self.button1, 5, 5, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.exit)
		self.grid.attach(self.button2, 1, 5, 1, 1)

		self.show_all()

	def auto_partition(self,button):
		self.clear_window()
		self.auto_part_setting = True

		# Get a list of disks and their capacity
		self.DEVICES = str(check_output(["lsblk","-n","-i","-o","NAME,SIZE,TYPE"]))
		self.DEVICES = list(self.DEVICES)
		del(self.DEVICES[1])
		del(self.DEVICES[0])
		del(self.DEVICES[len(self.DEVICES) - 1])
		self.DEVICES = "".join(self.DEVICES)
		self.DEVICES = self.DEVICES.split("\\n")
		DEV = []
		for each in range(len(self.DEVICES)):
			if ("loop" in self.DEVICES[each]):
				continue
			elif ("part" in self.DEVICES[each]):
				continue
			else:
				DEV.append(self.DEVICES[each])
		DEVICES = []
		for each in DEV:
			DEVICES.append(each.split())
		DEVICES = [x for x in DEVICES if x != []]
		for each in DEVICES:
			if (each[0] == "sr0"):
				DEVICES.remove(each)
		for each in range(len(DEVICES)):
			DEVICES[each].remove(DEVICES[each][2])
		for each in range(len(DEVICES)):
			DEVICES[each][0] = "/dev/%s" % (DEVICES[each][0])

		# Jesus Christ that's a lot of parsing and formatting.
		# At least it's done.
		# Now we have to make a GUI using them . . .

		self.label = Gtk.Label()
		self.label.set_markup("""
	Which drive would you like to install to?\t
	""")
		self.label.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.disks = Gtk.ComboBoxText.new()
		for each in range(len(DEVICES)):
			self.disks.append("%s" % (DEVICES[each][0]), "%s	Size: %s" % (DEVICES[each][0], DEVICES[each][1]))
		if (self.root_setting != ""):
			self.disks.set_active_id(self.root_setting)
		self.grid.attach(self.disks, 1, 2, 2, 1)

		self.home_part = Gtk.CheckButton.new_with_label("Seperate home partition")
		if ((self.home_setting != "") and (self.home_setting != "NULL")):
			self.home_part.set_active(True)
		self.home_part.connect("toggled",self.auto_home_setup)
		self.grid.attach(self.home_part, 1, 3, 2, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnext6clicked)
		self.grid.attach(self.button1, 3, 6, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.exit)
		self.grid.attach(self.button2, 2, 6, 1, 1)

		self.button3 = Gtk.Button.new_with_label("<-- Back")
		self.button3.connect("clicked", self.partitioning)
		self.grid.attach(self.button3, 1, 6, 1, 1)

		self.show_all()

	def auto_home_setup(self,widget):
		if (self.home_part.get_active() == 1):
			self.pre_exist = Gtk.CheckButton.new_with_label("Pre-existing")
			self.pre_exist.connect("toggled",self.auto_home_setup2)
			self.grid.attach(self.pre_exist, 1, 4, 2, 1)

			self.home_setting = "MAKE"
		else:
			self.grid.remove(self.pre_exist)
			self.home_setting = ""

		self.show_all()

	def auto_home_setup2(self,widget):

		if (self.pre_exist.get_active() == 1):
			DEV = []
			for each in range(len(self.DEVICES)):
				if ("loop" in self.DEVICES[each]):
					continue
				elif ("disk" in self.DEVICES[each]):
					continue
				else:
					DEV.append(self.DEVICES[each])
			DEVICES = []
			for each in DEV:
				DEVICES.append(each.split())
			DEVICES = [x for x in DEVICES if x != []]
			for each in DEVICES:
				if (each[0] == "sr0"):
					DEVICES.remove(each)
			for each in range(len(DEVICES)):
				DEVICES[each].remove(DEVICES[each][2])
			for each in range(len(DEVICES)):
				DEVICES[each][0] = list(DEVICES[each][0])
				del(DEVICES[each][0][0])
				del(DEVICES[each][0][0])
				DEVICES[each][0] = "".join(DEVICES[each][0])
			for each in range(len(DEVICES)):
				DEVICES[each][0] = "/dev/%s" % (DEVICES[each][0])

			self.parts = Gtk.ComboBoxText.new()
			for each in range(len(DEVICES)):
				self.parts.append("%s" % (DEVICES[each][0]), "%s	Size: %s" % (DEVICES[each][0], DEVICES[each][1]))
			if (self.home_setting != ""):
				self.parts.set_active_id(self.home_setting)
			self.grid.attach(self.parts, 1, 5, 2, 1)
		else:
			self.grid.remove(self.parts)
			self.home_setting ="MAKE"

		self.show_all()

	def onnext6clicked(self,button):
		if path.isdir("/sys/firmware/efi"):
			self.efi_setting = True
		else:
			self.efi_setting = False
		self.home_setting = "NULL"
		self.swap_setting = "FILE"
		if (self.disks.get_active_id() == None):
			self.label.set_markup("""
	Which drive would you like to install to?\t

	<b>You must pick a drive to install to or abort installation.</b>\t
	""")
			self.show_all()
		else:
			self.root_setting = self.disks.get_active_id()
			global part_completion
			part_completion = "COMPLETED"
			self.main_menu("clicked")



	def input_part(self,button):
		self.clear_window()

		self.label = Gtk.Label()
		self.label.set_markup("""
	What are the mount points for the partions you wish to be used?
	Leave empty the partions you don't want.
	<b> / MUST BE USED </b>
	""")
		self.label.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("/")
		self.label2.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label2, 1, 2, 1, 1)

		self.root = Gtk.Entry()
		self.root.set_text(self.root_setting)
		self.grid.attach(self.root, 2, 2, 1, 1)

		self.label3 = Gtk.Label()
		self.label3.set_markup("/boot/efi")
		self.label3.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label3, 1, 3, 1, 1)

		self.efi = Gtk.Entry()
		self.efi.set_text(self.efi_setting)
		self.grid.attach(self.efi, 2, 3, 1, 1)

		self.label5 = Gtk.Label()
		self.label5.set_markup("Must be fat32")
		self.label5.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label5, 3, 3, 1, 1)

		self.label4 = Gtk.Label()
		self.label4.set_markup("/home")
		self.label4.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label4, 1, 4, 1, 1)

		self.home = Gtk.Entry()
		self.home.set_text(self.home_setting)
		self.grid.attach(self.home, 2, 4, 1, 1)

		self.label4 = Gtk.Label()
		self.label4.set_markup("SWAP")
		self.label4.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label4, 1, 5, 1, 1)

		self.swap = Gtk.Entry()
		self.swap.set_text(self.swap_setting)
		self.grid.attach(self.swap, 2, 5, 1, 1)

		self.label5 = Gtk.Label()
		self.label5.set_markup("Must be linux-swap or file")
		self.label5.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label5, 3, 5, 1, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnext4clicked)
		self.grid.attach(self.button1, 3, 6, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.exit)
		self.grid.attach(self.button2, 1, 6, 1, 1)

		self.show_all()

	def onnext4clicked(self,button):
		if (self.root.get_text() == ""):
			self.label.set_markup("""
	What are the mount points for the partions you wish to be used?
	Leave empty the partions you don't want.
	<b> / MUST BE USED </b>

	/ NOT SET
	""")
			self.label.set_justify(Gtk.Justification.LEFT)
			self.grid.attach(self.label, 1, 1, 2, 1)

			self.show_all()

		elif ((self.efi.get_text() == "") and path.isdir("/sys/firmware/efi")):
			self.label.set_markup("""
	What are the mount points for the partions you wish to be used?
	Leave empty the partions you don't want.
	<b> / MUST BE USED </b>

	You are using EFI, therefore an EFI partition
	must be set.
	""")
			self.label.set_justify(Gtk.Justification.LEFT)
			self.grid.attach(self.label, 1, 1, 2, 1)

			self.show_all()
		else:
			self.label.set_markup("""
	What are the mount points for the partions you wish to be used?
	Leave empty the partions you don't want.
	<b> / MUST BE USED </b>
	""")
			self.label.set_justify(Gtk.Justification.LEFT)
			self.grid.attach(self.label, 1, 1, 2, 1)
			self.root_setting = self.root.get_text()

			self.show_all()
			if (self.efi.get_text() == ""):
				self.efi_setting = "NULL"
			else:
				self.efi_setting = self.efi.get_text()
			if (self.home.get_text() == ""):
				self.home_setting = "NULL"
			else:
				self.home_setting = self.home.get_text()
			if (self.swap.get_text() == ""):
				self.swap_setting = "FILE"
			else:
				self.swap_setting = self.swap.get_text()
			global part_completion
			part_completion = "COMPLETED"
			self.main_menu("clicked")



	def opengparted(self,button):
		Popen("gparted", stdout=DEVNULL, stderr=DEVNULL)
		self.auto_part_setting = False
		self.input_part("clicked")

	def options(self,button):
		self.clear_window()

		self.label.set_markup("""
	<b>Extra Options</b>
	The below options require a network connection, unless otherwise stated.\t
	Please ensure you are connected before selecting any of these options.
		""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 2, 1)

		self.label1 = Gtk.Label()
		self.label1.set_markup("""
		Install third-party packages such as NVIDIA drivers if necessary\t\t""")
		self.label1.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label1, 2, 2, 1, 1)

		self.extras = Gtk.CheckButton.new_with_label("Install Restricted Extras")
		if (self.extras_setting == 1):
			self.extras.set_active(True)
		self.grid.attach(self.extras, 1, 3, 2, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("""
		Update the system during installation""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 2, 4, 1, 1)

		self.updates = Gtk.CheckButton.new_with_label("Update before reboot")
		if (self.updates_setting == 1):
			self.updates.set_active(True)
		self.grid.attach(self.updates, 1, 5, 2, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("""
		Automaticly login upon boot up. Does <b>NOT</b> require internet.""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 2, 6, 1, 1)

		self.login = Gtk.CheckButton.new_with_label("Enable Auto-Login")
		if (self.login_setting == 1):
			self.login.set_active(True)
		self.grid.attach(self.login, 1, 7, 2, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.options_next)
		self.grid.attach(self.button1, 2, 8, 1, 1)

		self.grid.attach(self.button2, 1, 8, 1, 1)

		self.show_all()

	def options_next(self,button):
		if self.extras.get_active():
			self.extras_setting = 1
		else:
			self.extras_setting = 0
		if self.updates.get_active():
			self.updates_setting = 1
		else:
			self.updates_setting = 0
		if self.login.get_active():
			self.login_setting = 1
		else:
			self.login_setting = 0
		global options_completion
		options_completion = "COMPLETED"
		self.main_menu("clicked")

	def locale(self,button):
		self.clear_window()

		self.label = Gtk.Label()
		self.label.set_markup("""
<b>Choose your Language and Time Zone</b>""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("""

Langauge""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 1, 2, 1, 1)

		self.lang_menu = Gtk.ComboBoxText.new()
		self.lang_menu.append("english", "English")
		self.lang_menu.append("chinese", "Chinese")
		self.lang_menu.append("japanese", "Japanese")
		self.lang_menu.append("spanish", "Spanish")
		self.lang_menu.append("hindi", "Hindi")
		self.lang_menu.append("german", "German")
		self.lang_menu.append("french", "French")
		self.lang_menu.append("italian", "Italian")
		self.lang_menu.append("korean", "Korean")
		self.lang_menu.append("russian", "Russian")
		self.lang_menu.append("other", "Other, User will need to set up manually.")
		if (self.lang_setting != ""):
			self.lang_menu.set_active_id(self.lang_setting)
		self.grid.attach(self.lang_menu, 1, 3, 1, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("""

Time Zone""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 1, 4, 1, 1)

		self.time_menu = Gtk.ComboBoxText.new()
		self.time_menu.append("EST", "Eastern Standard Time")
		self.time_menu.append("CST", "Central Standard Time")
		self.time_menu.append("MST", "Mountain Standard Time")
		self.time_menu.append("PST", "Pacific Standard Time")
		self.time_menu.append("AST", "Alaska Standard Time")
		self.time_menu.append("HST", "Hawaii Standard Time")
		self.time_menu.append("MIT", "Midway Islands Time")
		self.time_menu.append("NST", "New Zealand Standard Time")
		self.time_menu.append("SST", "Soloman Standard Time")
		self.time_menu.append("AET", "Austrailia Eastern Time")
		self.time_menu.append("ACT", "Austrailia Central Time")
		self.time_menu.append("JST", "Japan Standard Time")
		self.time_menu.append("CTT", "China Taiwan Time")
		self.time_menu.append("VST", "Vietnam Standard Time")
		self.time_menu.append("BST", "Bangladesh Standard Time")
		self.time_menu.append("PLT", "Pakistan Lahore Time")
		self.time_menu.append("NET", "Near East Time")
		self.time_menu.append("EAT", "East Africa Time")
		self.time_menu.append("ART", "(Arabic) Egypt Standard Time")
		self.time_menu.append("EET", "Eastern European Time")
		self.time_menu.append("ECT", "European Central Time")
		self.time_menu.append("GMT", "Greenwich Mean Time")
		self.time_menu.append("CAT", "Central African Time")
		self.time_menu.append("BET", "Brazil Eastern Time")
		self.time_menu.append("AGT", "Argentina Standard Time")
		self.time_menu.append("PRT", "Puerto Rico and US Virgin Islands Time")
		self.time_menu.append("IET", "Indiana Eastern Standard Time")
		if (self.time_zone != ""):
			self.time_menu.set_active_id(self.time_zone)
		self.grid.attach(self.time_menu, 1, 5, 1, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnext3clicked)
		self.grid.attach(self.button1, 3, 6, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.exit)
		self.grid.attach(self.button2, 2, 6, 1, 1)

		self.show_all()

	def onnext3clicked(self,button):
		try:
			self.lang_setting = self.lang_menu.get_active_id()
		except:
			self.lang_setting = "english"

		try:
			self.time_zone = self.time_menu.get_active_id()
		except:
			self.time_zone = "EST"

		global locale_completion
		locale_completion = "COMPLETED"
		self.main_menu("clicked")

	def keyboard(self,button):
		self.clear_window()

		self.label = Gtk.Label()
		self.label.set_markup("""
	<b>Choose your Keyboard layout</b>\t
	""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.model_label = Gtk.Label()
		self.model_label.set_markup("""Model: """)
		self.model_label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.model_label, 1, 2, 1, 1)

		self.model_menu = Gtk.ComboBoxText.new()
		PWD = getcwd()
		chdir("/usr/share/console-setup")
		layouts = check_output(["./kbdnames-maker"], stderr=DEVNULL)
		chdir(PWD)
		layouts = str(layouts)
		layouts = layouts.split("\\n")
		layout_list = []
		for each in layouts:
			layout_list.append(each.split("*"))
		for each in range(len(layout_list)):
			del(layout_list[each][0])
		model = []
		for each in range(len(layout_list) - 1):
			if (layout_list[each][0] == "model"):
				model.append(layout_list[each][len(layout_list[each]) - 1])
		for each in model:
			self.model_menu.append(each, each)
		if (self.model_setting != ""):
			self.model_menu.set_active_id(self.model_setting)
		self.grid.attach(self.model_menu, 2, 2, 2, 1)

		self.layout_label = Gtk.Label()
		self.layout_label.set_markup("""Layout: """)
		self.layout_label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.layout_label, 1, 3, 1, 1)

		self.layout_menu = Gtk.ComboBoxText.new()
		layouts = []
		for each in range(len(layout_list) - 1):
			if (layout_list[each][0] == "layout"):
				layouts.append(layout_list[each][len(layout_list[each]) - 1])
		for each in layouts:
			self.layout_menu.append(each, each)
		if (self.layout_setting != ""):
			self.layout_menu.set_active_id(self.layout_setting)
		self.grid.attach(self.layout_menu, 2, 3, 2, 1)

		self.varient_label = Gtk.Label()
		self.varient_label.set_markup("""Varient: """)
		self.varient_label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.varient_label, 1, 4, 1, 1)

		self.varient_menu = Gtk.ComboBoxText.new()
		varients = []
		for each in range(len(layout_list) - 1):
			if (layout_list[each][0] == "variant"):
				varients.append(layout_list[each][len(layout_list[each]) - 1])
		for each in varients:
			self.varient_menu.append(each, each)
		if (self.varient_setting != ""):
			self.varient_menu.set_active_id(self.varient_setting)
		self.grid.attach(self.varient_menu, 2, 4, 2, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnext5clicked)
		self.grid.attach(self.button1, 3, 6, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.exit)
		self.grid.attach(self.button2, 1, 6, 1, 1)

		self.show_all()

	def onnext5clicked(self,button):
		try:
			self.model_setting = self.model_menu.get_active_id()
		except:
			self.model_setting = "Generic 105-key PC (intl.)"
		try:
			self.layout_setting = self.layout_menu.get_active_id()
		except:
			self.layout_setting = "English (US)"
		try:
			self.varient_setting = self.varient_menu.get_active_id()
		except:
			self.varient_setting = "euro"
		global keyboard_completion
		keyboard_completion = "COMPLETED"

		self.main_menu("clicked")

	def done(self,button):
		# Check to see if each segment has been completed
		# If it hasn't, print a warning, else
		# Print out the value of stuffs and exit
		global keyboard_completion
		global locale_completion
		global options_completion
		global part_completion
		global user_completion
		if (( keyboard_completion != "COMPLETED" ) or ( locale_completion != "COMPLETED" ) or ( options_completion != "COMPLETED" ) or ( part_completion != "COMPLETED" ) or ( user_completion != "COMPLETED" )):
			self.label.set_markup("""
		Feel free to complete any of the below segments in any order.\t
		However, all segments must be completed.

		<b>One or more segments have not been completed</b>
		Please complete these segments, then try again.
		Or, exit installation.\n""")
		else:
			# Vars to print:
			#	1  * self.auto_part_setting
			#	2  * self.password_setting
			#	3  * self.username_setting
			#	4  * self.compname_setting
			#	5  * self.root_setting
			#	6  * self.efi_setting
			#	7  * self.home_setting
			#	8  * self.swap_setting
			#	9  * self.extras_setting
			#	10  * self.updates_setting
			#	11 * self.login_setting
			#	12 * self.model_setting
			#	13 * self.layout_setting
			#	14 * self.lang_setting
			#	15 * self.time_zone
			#	16 * self.varient_setting
			print("%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s" % (self.auto_part_setting, self.root_setting, self.efi_setting, self.home_setting, self.swap_setting, self.lang_setting, self.time_zone, self.username_setting, self.compname_setting, self.password_setting, self.extras_setting, self.updates_setting, self.login_setting, self.model_setting, self.layout_setting,self.varient_setting))
			exit(0)
		self.show_all()

	def exit(self,button):
		Gtk.main_quit("delete-event")
		print(1)
		exit(1)

	def clear_window(self):
		children = self.grid.get_children()
		for each in children:
			self.grid.remove(each)


def show_main():
	window = main()
	window.set_decorated(True)
	window.set_resizable(False)
	window.set_position(Gtk.WindowPosition.CENTER)
	window.connect("delete-event", main.exit)
	window.show_all()
	Gtk.main()


show_main()
