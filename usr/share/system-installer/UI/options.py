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

class main(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)

		self.label = Gtk.Label()
		self.label.set_markup("""
	<b>Extra Options</b>
	The below options require a network connection.
	Please ensure you are connected before selecting any of these options.
		""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 2, 1)

		self.label1 = Gtk.Label()
		self.label1.set_markup("""
		Install third-party packages such as NVIDIA drivers if necessary""")
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
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 2, 8, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.onexitclicked)
		self.grid.attach(self.button2, 1, 8, 1, 1)

	def onnextclicked(self,button):
		if self.extras.get_active():
			extras = 1
		else:
			extras = 0
		if self.updates.get_active():
			updates = 1
		else:
			updates = 0
		if self.login.get_active():
			login = 1
		else:
			login = 0
		print("%s %s %s" % (extras, updates, login))
		exit(0)
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
