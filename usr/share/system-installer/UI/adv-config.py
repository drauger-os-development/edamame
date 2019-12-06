#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  adv-config.py
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
from os import system
from subprocess import Popen

class main(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)

		self.label = Gtk.Label()
		self.label.set_markup("""\n	The below options are meant exclusivly for advanced users. <b>User discretion is advised.</b>	\n""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.button1 = Gtk.Button.new_with_label("Open Chroot Terminal")
		self.button1.connect("clicked", self.chrootclicked)
		self.grid.attach(self.button1, 3, 6, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Delete Installation")
		self.button2.connect("clicked", self.ondeletewarn)
		self.grid.attach(self.button2, 1, 6, 1, 1)

		self.button3 = Gtk.Button.new_with_label("Add PPA")
		self.button3.connect("clicked", self.addPPA)
		self.grid.attach(self.button3, 2, 6, 1, 1)

		self.button4 = Gtk.Button.new_with_label("Exit")
		self.button4.connect("clicked", self.onexitclicked)
		self.grid.attach(self.button4, 2, 7, 1, 1)

	def onexitclicked(self,button):
		print("EXIT")
		exit(1)

	def ondeletewarn(self,button):
		#warn of rm -rf in chroot
		self.label.set_markup("""\n	Are you sure you wish to delete the new installation? No data will be recoverable.	\n""")

		self.grid.remove(self.button1)
		self.grid.remove(self.button2)
		self.grid.remove(self.button3)

		self.button5 = Gtk.Button.new_with_label("DELETE")
		self.button5.connect("clicked", self.delete_install)
		self.grid.attach(self.button5, 2, 6, 1, 1)

		self.show_all()

	def delete_install(self,button):
		print("rm -rf")
		# This code is dangerous. Be wary
		# Popen(["rm", "-rf", "/mnt/*"])

	def chrootclicked(self,button):
		Popen(["gnome-terminal","-e","\"bash","-c","\\\"echo","When","done,","run","exit;","arch-chroot","/mnt\\\"\""])
		exit(0)

	def addPPA(self,button):
		print("PPA")
		exit(0)


def exit_button(x,y):
	Gtk.main_quit("delete-event")
	exit(1)

def show_main():
	window = main()
	window.set_decorated(True)
	window.set_resizable(False)
	window.set_position(Gtk.WindowPosition.CENTER)
	window.connect("delete-event",exit_button)
	window.show_all()
	Gtk.main()


show_main()
