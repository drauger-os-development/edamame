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

class main(Gtk.Window):
	def __init__(self):
			Gtk.Window.__init__(self, title="System Installer")
			self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
			self.add(self.grid)

			self.label = Gtk.Label()
			self.label.set_markup("""
	Welcome to the Drauger OS System Installer!
	
	A few things before we get started:
	
	<b>PARTITIONING</b>
	
	The Drauger OS System Installer places all partitons at the beginning of the drive
	when doing manual partitoning.
	It is advised to account for this if installing next to another OS.
	If using automatic partitoning, it uses all of the drives in your system
	(up to 2 drives will be used, favoring NVMe drives).
	
	<b>ALPHA WARNING</b>
	
	The Drauger OS System Installer is currently in alpha.
	Expect bugs.
	""")
			self.label.set_justify(Gtk.Justification.LEFT)
			self.grid.attach(self.label, 1, 1, 3, 1)
			
			self.button1 = Gtk.Button.new_with_label("Okay -->")
			self.button1.connect("clicked", self.onnextclicked)
			self.grid.attach(self.button1, 3, 2, 1, 1)
			
			self.button2 = Gtk.Button.new_with_label("Exit")
			self.button2.connect("clicked", self.onexitclicked)
			self.grid.attach(self.button2, 1, 2, 1, 1)
			
	def onnextclicked(self,button):
			exit(0)
	def onexitclicked(self,button):
			exit(1)
			
def show_main():
	window = main()
	window.set_decorated(False)
	window.set_resizable(False)
	window.set_opacity(0.0)
	window.set_position(Gtk.WindowPosition.CENTER)
	window.show_all()
	Gtk.main() 
	window.connect("delete-event", Gtk.main_quit)

show_main()
