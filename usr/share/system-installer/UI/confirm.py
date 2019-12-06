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
from sys import argv
partitioner=argv[1]
LANG=argv[2]
TIME_ZONE=argv[3]
USERNAME=argv[4]
COMPNAME=argv[5]
PASS=argv[6]
try:
	EXTRAS=argv[7]
except:
	EXTRAS=None
try:
	UPDATES=argv[8]
except:
	UPDATES=None
try:
	LOGIN=argv[9]
except:
	LOGIN=None
if EXTRAS != "0" and EXTRAS != None:
	EXTRAS = "Yes"
else:
	EXTRAS = "No"
if UPDATES != "0" and UPDATES != None:
	UPDATES = "Yes"
else:
	UPDATES = "No"
# if EFI == "200":
	# EFI = "Yes, 200MB at drive start"
# else:
	# EFI = "No"

partitioner = partitioner.split(",")
ROOT_LIST = partitioner[0]
EFI_LIST = partitioner[1]
HOME_LIST = partitioner[2]
SWAP_LIST = partitioner[3]
partitioner = {}
ROOT_LIST = ROOT_LIST.split(":")
EFI_LIST = EFI_LIST.split(":")
HOME_LIST = HOME_LIST.split(":")
SWAP_LIST = SWAP_LIST.split(":")
partitioner.update( {"ROOT":[ROOT_LIST[1]]} )
partitioner.update( {"EFI":[EFI_LIST[1]]} )
partitioner.update( {"HOME":[HOME_LIST[1]]} )
partitioner.update( {"SWAP":[SWAP_LIST[1]]} )


# count = 0
# for each in partitioner:
	# if (each == ","):
		# partitioner[count] = """
# """
	# count = count + 1
# partitioner = "".join(partitioner)

class main(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)

		self.label = Gtk.Label()
		self.label.set_markup("""
	<b>FINAL CONFIRMATION</b>
	Please read the below summary carefully.
	This is your final chance to cancel installation.
		""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 3, 1)

		self.label1 = Gtk.Label()
		self.label1.set_markup("""
	<b>PARTITIONS</b>
		""")
		self.label1.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label1, 1, 2, 3, 1)

		# self.label2 = Gtk.Label()
		# self.label2.set_markup("""	UEFI:	""")
		# self.label2.set_justify(Gtk.Justification.CENTER)
		# self.grid.attach(self.label2, 1, 3, 1, 1)

		# self.label3 = Gtk.Label()
		# self.label3.set_markup("%s" % (EFI))
		# self.label3.set_justify(Gtk.Justification.CENTER)
		# self.grid.attach(self.label3, 3, 3, 1, 1)

		self.label4 = Gtk.Label()
		self.label4.set_markup("""	Partitioning:	""")
		self.label4.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label4, 1, 4, 1, 1)

		self.label5 = Gtk.Label()
		self.label5.set_markup("""ROOT: %s
EFI: %s
HOME: %s,
SWAP: %s""" % (partitioner["ROOT"][0],partitioner["EFI"][0],partitioner["HOME"][0],partitioner["SWAP"][0]))
		self.label5.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label5, 3, 4, 1, 1)

		self.label6 = Gtk.Label()
		self.label6.set_markup("""
	<b>SYSTEM</b>
		""")
		self.label6.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label6, 1, 5, 3, 1)

		self.label7 = Gtk.Label()
		self.label7.set_markup("""	Language:	""")
		self.label7.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label7, 1, 6, 1, 1)

		self.label8 = Gtk.Label()
		self.label8.set_markup(LANG)
		self.label8.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label8, 3, 6, 1, 1)

		self.label9 = Gtk.Label()
		self.label9.set_markup("""	Time Zone:	""")
		self.label9.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label9, 1, 7, 1, 1)

		self.label10 = Gtk.Label()
		self.label10.set_markup(TIME_ZONE)
		self.label10.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label10, 3, 7, 1, 1)

		self.label11 = Gtk.Label()
		self.label11.set_markup("	Computer Name:	")
		self.label11.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label11, 1, 8, 1, 1)

		self.label12 = Gtk.Label()
		self.label12.set_markup(COMPNAME)
		self.label12.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label12, 3, 8, 1, 1)

		self.label13 = Gtk.Label()
		self.label13.set_markup("""
	<b>USER</b>
		""")
		self.label13.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label13, 1, 9, 3, 1)

		self.label14 = Gtk.Label()
		self.label14.set_markup("""	Username:	""")
		self.label14.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label14, 1, 10, 1, 1)

		self.label15 = Gtk.Label()
		self.label15.set_markup(USERNAME)
		self.label15.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label15, 3, 10, 1, 1)

		self.label16 = Gtk.Label()
		self.label16.set_markup("""	Password:	""")
		self.label16.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label16, 1, 11, 1, 1)

		self.label17 = Gtk.Label()
		self.label17.set_markup(PASS)
		self.label17.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label17, 3, 11, 1, 1)

		self.label23 = Gtk.Label()
		self.label23.set_markup("""	Auto-Login:	""")
		self.label23.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label23, 1, 12, 1, 1)

		self.label24 = Gtk.Label()
		self.label24.set_markup(LOGIN)
		self.label24.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label24, 3, 12, 1, 1)

		self.label18 = Gtk.Label()
		self.label18.set_markup("""
	<b>OTHER</b>
		""")
		self.label18.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label18, 1, 13, 3, 1)

		self.label19 = Gtk.Label()
		self.label19.set_markup("""	Install Extras:	""")
		self.label19.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label19, 1, 14, 1, 1)

		self.label20 = Gtk.Label()
		self.label20.set_markup(EXTRAS)
		self.label20.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label20, 3, 14, 1, 1)

		self.label21 = Gtk.Label()
		self.label21.set_markup("""	Install Updates:	""")
		self.label21.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label21, 1, 15, 1, 1)

		self.label22 = Gtk.Label()
		self.label22.set_markup(UPDATES)
		self.label22.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label22, 3, 15, 1, 1)

		self.button1 = Gtk.Button.new_with_label("INSTALL NOW -->")
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 3, 17, 1, 1)

		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.onexitclicked)
		self.grid.attach(self.button2, 1, 17, 1, 1)

	def onnextclicked(self,button):
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
