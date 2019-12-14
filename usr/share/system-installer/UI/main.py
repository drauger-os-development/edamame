#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2019 Thomas Castleman <contact@draugeros.org>
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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import re

def hasnumbers(inputString):
	return any(char.isdigit() for char in inputString)

def hasletters(inputString):
	if re.search('[a-zA-Z]', inputString):
		return True
	else:
		return False

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


default = """
	Welcome to the Drauger OS System Installer!

	A few things before we get started:

	<b>PARTITIONING</b>

	The Drauger OS System Installer places all partitons at the beginning of the drive\t
	when doing manual partitoning.
	It is advised to account for this if installing next to another OS.
	If using automatic partitoning, it uses all of the drives in your system
	(up to 2 drives will be used, favoring NVMe drives).

	<b>ALPHA WARNING</b>

	The Drauger OS System Installer is currently in alpha.
	Expect bugs.
	"""
keyboard_completion = "TO DO"
user_completion = "TO DO"
part_completion = "TO DO"
locale_completion = "TO DO"
options_completion = "TO DO"

class main(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)

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
		self.label.set_markup(default)

		self.button3.set_label("Quick Install")
		self.button3.connect("clicked", self.quick_install_warning)

		self.button1.set_label("Next -->")
		self.button1.connect("clicked", self.onnextclicked)

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
		self.completion_label.set_markup("""COMPLETION""")
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
		self.grid.attach(self.username, 2, 3, 1, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("	Computer\'s Name:	")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 1, 4, 1, 1)

		self.compname = Gtk.Entry()
		self.grid.attach(self.compname, 2, 4, 1, 1)

		self.label3 = Gtk.Label()
		self.label3.set_markup("	Password:	")
		self.label3.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label3, 1, 5, 1, 1)

		self.password = Gtk.Entry()
		self.password.set_visibility(False)
		self.grid.attach(self.password, 2, 5, 1, 1)

		self.label4 = Gtk.Label()
		self.label4.set_markup("	Confirm Pasword:	")
		self.label4.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label4, 1, 6, 1, 1)

		self.passconf = Gtk.Entry()
		self.passconf.set_visibility(False)
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
		elif hasnumbers(self.password_setting) != True:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Password contains no numbers")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasletters(self.password_setting) != True:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Password contains no letters")
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
			user_completion = "COMPLETED"
			self.main_menu("clicked")

		self.show_all()

	def partitioning(self,button):
		print("PART")

	def options(self,button):
		self.clear_window()

		self.label.set_markup("""
	<b>Extra Options</b>
	The below options require a network connection.
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
		self.grid.attach(self.extras, 1, 3, 2, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("""
		Update the system during installation""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 2, 4, 1, 1)

		self.updates = Gtk.CheckButton.new_with_label("Update before reboot")
		self.grid.attach(self.updates, 1, 5, 2, 1)

		self.label2 = Gtk.Label()
		self.label2.set_markup("""
		Automaticly login upon boot up""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 2, 6, 1, 1)

		self.login = Gtk.CheckButton.new_with_label("Enable Auto-Login")
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
		options_completion = "COMPLETED"
		self.main_menu("clicked")

	def locale(self,button):
		print("LOCALE AND TIME")

	def keyboard(self,button):
		print("KEYBOARD")

	def done(self,button):
		# Check to see if each segment has been completed
		# If it hasn't, print a warning, else
		# Print out the value of stuffs and exit
		exit(0)

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
