#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  user.py
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
from gi.repository import Gtk
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


class main(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)

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
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 2, 8, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.onexitclicked)
		self.grid.attach(self.button2, 1, 8, 1, 1)

		self.label5 = None

	def onnextclicked(self,button):
		pass1 = self.password.get_text()
		pass2 = self.passconf.get_text()
		username = self.username.get_text()
		username = username.lower()
		compname = self.compname.get_text()
		if pass1 != pass2:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Passwords do not match")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasnumbers(pass1) != True:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Password contains no numbers")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasletters(pass1) != True:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Password contains no letters")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif len(pass1) < 4:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Password is less than 4 characters")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasSC(username):
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Username contains special characters")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasspace(username):
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Username contains space")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif len(username) < 1:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Username empty")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasSC(compname):
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Computer Name contains non-hyphen special character")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif hasspace(compname):
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Computer Name contains space")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		elif len(compname) < 1:
			if self.label5 != None:
				self.grid.remove(self.label5)
			self.label5 = Gtk.Label()
			self.label5.set_markup("Computer Name is empty")
			self.label5.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label5, 1, 7, 2, 1)
		else:
			if self.label5 != None:
				self.grid.remove(self.label5)
			print("%s %s %s" % (username, compname, pass1))
			pass2 = None
			pass1 = None
			exit(0)
		self.show_all()

	def onexitclicked(self,button):
			exit(1)

def show_main():
	window = main()
	window.set_decorated(False)
	window.set_resizable(False)
	window.set_position(Gtk.WindowPosition.CENTER)
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	Gtk.main()


show_main()

