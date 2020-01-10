#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  success.py
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
from subprocess import Popen
class main(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)

		self.label = Gtk.Label()
		self.label.set_markup("""\n	Drauger OS has been successfully installed to your designated partitions!	\n""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.button1 = Gtk.Button.new_with_label("Shut Down System")
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 3, 6, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.exit)
		self.grid.attach(self.button2, 1, 6, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Advanced")
		self.button2.connect("clicked", self.onadvclicked)
		self.grid.attach(self.button2, 2, 6, 1, 1)

	def onnextclicked(self,button):
		system("poweroff")
		exit(0)

	def onadvclicked(self,button):
		self.clear_window()

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
		self.button4.connect("clicked", self.exit)
		self.grid.attach(self.button4, 2, 7, 1, 1)

		self.show_all()

	def ondeletewarn(self,button):
		self.clear_window()

		self.label.set_markup("""\n\tAre you sure you wish to delete the new installation? No data will be recoverable.\t\n""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.button5 = Gtk.Button.new_with_label("DELETE")
		self.button5.connect("clicked", self.delete_install)
		self.grid.attach(self.button5,2, 2, 1, 1)

		self.button4 = Gtk.Button.new_with_label("Exit")
		self.button4.connect("clicked", self.exit)
		self.grid.attach(self.button4, 3, 2, 1, 1)

		self.button5 = Gtk.Button.new_with_label("<-- Back")
		self.button5.connect("clicked",self.onadvclicked)
		self.grid.attach(self.button5, 1, 2, 1, 1)

		self.show_all()

	def delete_install(self,button):
		# This code is dangerous. Be wary
		Popen(["rm", "-rf", "/mnt/*"])
		Popen(["notify-send","Deleting installed system. Check /mnt to make sure eveything was deleted."])
		self.exit("clicked")


	def chrootclicked(self,button):
		Popen(["gnome-terminal","-e","\"bash","-c","\\\"echo","When","done,","run","exit;","arch-chroot","/mnt\\\"\""])
		exit(0)

	def addPPA(self,button):
		self.clear_window()

		self.label = Gtk.Label()
		self.label.set_markup("""\n\tWhat PPAs would you like to add?\t\n""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.label1 = Gtk.Label()
		self.label1.set_markup("""\tPPA:""")
		self.label1.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label1, 1, 2, 1, 1)

		self.PPAentry = Gtk.Entry()
		self.PPAentry.set_visibility(True)
		self.grid.attach(self.PPAentry, 2, 2, 1, 1)

		self.button4 = Gtk.Button.new_with_label("Add PPA")
		self.button4.connect("clicked", self.addPPA_backend)
		self.grid.attach(self.button4, 2, 3, 1, 1)

		self.button4 = Gtk.Button.new_with_label("Exit")
		self.button4.connect("clicked", self.exit)
		self.grid.attach(self.button4, 3, 3, 1, 1)

		self.button5 = Gtk.Button.new_with_label("<-- Back")
		self.button5.connect("clicked",self.onadvclicked)
		self.grid.attach(self.button5, 1, 3, 1, 1)

		self.show_all()

	def addPPA_backend(self,button):
		self.grid.remove(self.label)
		try:
			Popen(["add-apt-repository","--yes","PPA:%s" % ((self.PPAentry.get_text()).lower())])

			self.label = Gtk.Label()
			self.label.set_markup("""\n\tWhat PPAs would you like to add?\t\n\t<b>%s added successfully!</b>\t\n""" % (self.PPAentry.get_text()))
			self.label.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label, 1, 1, 2, 1)
		except:
			self.label = Gtk.Label()
			self.label.set_markup("""\n\tWhat PPAs would you like to add?\t\n\t<b>adding %s failed.</b>\t\n""" % (self.PPAentry.get_text()))
			self.label.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label, 1, 1, 2, 1)

		self.PPAentry.set_text("")

		self.show_all()

	def exit(self,button):
		Gtk.main_quit("delete-event")
		exit(0)

	def clear_window(self):
		children = self.grid.get_children()
		for each in children:
			self.grid.remove(each)


def exit_button(x,y):
	Gtk.main_quit("delete-event")
	exit(1)

def show_main():
	window = main()
	window.set_decorated(True)
	window.set_resizable(False)
	window.set_position(Gtk.WindowPosition.CENTER)
	window.connect("delete-event",main.exit)
	window.show_all()
	Gtk.main()


show_main()
