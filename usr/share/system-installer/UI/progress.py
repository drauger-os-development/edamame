#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  progress.py
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
from gi.repository import Gtk,GLib
from os import system
import sys, select

class main(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)

		self.label = Gtk.Label()
		self.label.set_markup("""	Installing Drauger OS to your internal hard drive.\nThis may take some time. If you have an error, please send\nthe log file (located at /tmp/system-installer.log) to: contact@draugeros.org	""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 1, 1)


		self.progress = Gtk.ProgressBar()
		self.progress.set_fraction(0)
		self.progress.set_show_text(True)
		self.progress.set_text("0 %")
		self.source_id = GLib.timeout_add(1000, self.pulse)
		self.grid.attach(self.progress, 1, 2, 1, 1)

		self.file_contents = Gtk.TextBuffer()
		self.text = Gtk.TextView.new_with_buffer(self.file_contents)
		self.text.set_editable(False)
		self.text.set_cursor_visible(False)
		self.text.set_monospace(True)


	def pulse(self):
		print("pulse")
		i, o, e = select.select( [sys.stdin], [], [], 1 )
		fraction=sys.stdin.readline().strip()
		if (not i):
			print("got nothing")
			return True
		fraction_bar=int(fraction) / 100
		self.progress.set_fraction(fraction_bar)
		self.progress.set_text("%s \%" % (fraction))
		if (fraction == 100):
			exit(0)
		return True


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
