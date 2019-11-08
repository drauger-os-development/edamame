#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  partition-mapper.py
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
		self.grid.attach(self.root, 2, 2, 1, 1)

		self.root_type = Gtk.ComboBoxText.new()
		self.root_type.append("ext4","ext4")
		self.root_type.append("ext3","ext3")
		self.root_type.append("ext2","ext2")
		self.root_type.append("btrfs","btrfs")
		self.grid.attach(self.root_type, 3, 2, 1, 1)

		self.label3 = Gtk.Label()
		self.label3.set_markup("/boot/efi")
		self.label3.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label3, 1, 3, 1, 1)

		self.efi = Gtk.Entry()
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
		self.grid.attach(self.home, 2, 4, 1, 1)

		self.home_type = Gtk.ComboBoxText.new()
		self.home_type.append("(blank)","(no /home)")
		self.home_type.append("ext4","ext4")
		self.home_type.append("ext3","ext3")
		self.home_type.append("ext2","ext2")
		self.home_type.append("btrfs","btrfs")
		self.home_type.append("xfs","xfs")
		self.home_type.append("zfs","zfs")
		self.grid.attach(self.home_type, 3, 4, 1, 1)

		self.label4 = Gtk.Label()
		self.label4.set_markup("SWAP")
		self.label4.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label4, 1, 5, 1, 1)

		self.swap = Gtk.Entry()
		self.grid.attach(self.swap, 2, 5, 1, 1)

		self.label5 = Gtk.Label()
		self.label5.set_markup("Must be linux-swap or file")
		self.label5.set_justify(Gtk.Justification.RIGHT)
		self.grid.attach(self.label5, 3, 5, 1, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 3, 6, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.onexitclicked)
		self.grid.attach(self.button2, 1, 6, 1, 1)

	def onexitclicked(self,button):
			print("EXIT")
			exit(1)

	def onnextclicked(self,button):
			if (self.root.get_text() == ""):
				self.label.set_markup("""
	What are the mount points for the partions you wish to be used?
	Leave empty the partions you don't want.
	<b> / MUST BE USED </b>

	/ NOT SET
	""")
				self.label.set_justify(Gtk.Justification.LEFT)
				self.grid.attach(self.label, 1, 1, 2, 1)
			else:
				self.label.set_markup("""
	What are the mount points for the partions you wish to be used?
	Leave empty the partions you don't want.
	<b> / MUST BE USED </b>
	""")
				self.label.set_justify(Gtk.Justification.LEFT)
				self.grid.attach(self.label, 1, 1, 2, 1)
				root = self.root.get_text()
				root_type = self.root_type.get_active_text()
			if (self.efi.get_text() == ""):
				efi = "NULL"
			else:
				efi = self.efi.get_text()
			if (self.home.get_text() == ""):
				home = "NULL"
			else:
				home = self.home.get_text()
				home_type = self.home_type.get_active_text()
			if (self.swap.get_text() == ""):
				swap = "FILE"
			else:
				swap = self.swap.get_text()

			print("ROOT:%s:%s,EFI:%s,HOME:%s:%s,SWAP:%s" % (root,root_type,efi,home,home_type,swap))
			exit(0)


def show_main():
	window = main()
	window.set_decorated(False)
	window.set_resizable(False)
	window.set_position(Gtk.WindowPosition.CENTER)
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	Gtk.main()


show_main()
