#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  partition-maker.py
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
from subprocess import Popen
EFI=argv[1]
MAX=argv[2]
MAX=float(MAX)

class main(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="System Installer")
		self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.grid)
		
		ad1 = Gtk.Adjustment(0, 0, 100, 5, 10, 0)
		
		if EFI == "200":
			self.label = Gtk.Label()
			self.label.set_markup("""
	<b>Your system has been detected as using UEFI.</b>
	A 200 MB UEFI partion will be created at the beginning of your drive		
	when installation begins
	""")
			self.label.set_justify(Gtk.Justification.LEFT)
			self.grid.attach(self.label, 1, 1, 1, 1)
		
		self.label2 = Gtk.Label()
		self.label2.set_markup("""
		
	<b>The Drauger OS System Installer creates a SWAP file by default</b>
	You do not have to worry about accounting for this when making system partions.		
	
	<b>This slider is for the whole drive</b>
		""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 1, 2, 1, 1)
		
		self.label3 = Gtk.Label()
		self.label3.set_markup("""
		
		Main Partion Size (in Gigabytes)""")
		self.label3.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label3, 1, 3, 1, 1)
		
		self.mainpart = Gtk.Scale.new_with_range(orientation=Gtk.Orientation.HORIZONTAL, min=16, max=MAX, step=0.1)
		self.mainpart.set_value(MAX)
		self.grid.attach(self.mainpart, 1, 4, 3, 1)
		
		self.link = Gtk.Button.new_with_label("Open Gparted")
		self.link.connect("clicked", self.opengparted)
		self.grid.attach(self.link, 1, 5, 1, 1)
		
		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 3, 5, 1, 1)
			
		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.onexitclicked)
		self.grid.attach(self.button2, 2, 5, 1, 1)
			
	def onnextclicked(self,button):
			print(self.mainpart.get_value())
			exit(0)
	def onexitclicked(self,button):
			exit(1)
	def opengparted(self,button):
		Popen("gparted")
		
		
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
