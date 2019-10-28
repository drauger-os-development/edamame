#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  partition-type.py
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
		self.label.set_markup("""
	<b> PLEASE READ </b>

	When you are ready, click the "Open Gparted" button to open Gparted and partiton your drive how you wish it to be.
	This is done while bugs are worked out of the partioning system inside the Drauger OS installer.

	Please make note of the mount point for the partions you wish to install to. Individual partions are supported for:
		* /
		* /boot/efi
		* /home
		* Swap

	Furthermore, please ensure you apply the changes to the partiton table when you are done.

	If you are not familiar with partitioning drives or the above was gibberish to you, please exit this installer NOW.
	Partioning drives risks a loss in data if you are inexperienced.

	The user assumes fault and all liability for all loss of data which may occur due to repartioning any drive.

	Once you are done with your changes, please click "Okay -->".
	""")
		self.label.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label, 1, 1, 5, 1)

		self.link = Gtk.Button.new_with_label("Open Gparted")
		self.link.connect("clicked", self.opengparted)
		self.grid.attach(self.link, 3, 5, 1, 1)

		# self.label = Gtk.Label()
		# self.label.set_markup("""
	# Please select how you would like your system to be partioned:
	# """)
		# self.label.set_justify(Gtk.Justification.LEFT)
		# self.grid.attach(self.label, 1, 1, 5, 1)

		# self.link = Gtk.Button.new_with_label("Open Gparted")
		# self.link.connect("clicked", self.opengparted)
		# self.grid.attach(self.link, 3, 5, 1, 1)


		# # a new radiobutton with a label
		# button1 = Gtk.RadioButton(label="Use Entire Disk")
		# # connect the signal "toggled" emitted by the radiobutton
		# # with the callback function toggled_cb
		# button1.connect("toggled", self.toggled_cb)
		# self.grid.attach(button1, 1, 3, 1, 1)

		# # another radiobutton, in the same group as button1
		# button2 = Gtk.RadioButton.new_from_widget(button1)
		# # with label "Button 2"
		# button2.set_label("Manually Set Up Partitions")
		# # connect the signal "toggled" emitted by the radiobutton
		# # with the callback function toggled_cb
		# button2.connect("toggled", self.toggled_cb)
		# # set button2 not active by default
		# button2.set_active(False)
		# self.grid.attach(button2, 1, 4, 1, 1)

		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 5, 5, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.onexitclicked)
		self.grid.attach(self.button2, 1, 5, 1, 1)

		# self.SETTING = "on"

	def onnextclicked(self,button):
			exit(0)
	def onexitclicked(self,button):
			print("EXIT")
			exit(1)
	def opengparted(self,button):
		Popen("gparted")

	# # callback function
	# def toggled_cb(self, button):
		# # whenever the button is turned on, state is on
		# if button.get_label() == "Use Entire Disk":
			# self.SETTING = "on"
		# # else state is off
		# else:
			# self.SETTING = "off"


def show_main():
	window = main()
	window.set_decorated(False)
	window.set_resizable(False)
	window.set_position(Gtk.WindowPosition.CENTER)
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	Gtk.main()


show_main()
