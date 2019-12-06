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
from time import sleep

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
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 3, 2, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.onexitclicked)
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

	def onnextclicked(self,button):
		exit(2)

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
