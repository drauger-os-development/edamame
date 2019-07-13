#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  get_locale.py
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
<b>Choose your Language and Time Zone</b>""")
		self.label.set_justify(Gtk.Justification.CENTER)
		self.grid.attach(self.label, 1, 1, 3, 1)
		
		self.label2 = Gtk.Label()
		self.label2.set_markup("""

Langauge""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 1, 2, 1, 1)
		
		self.lang_menu = Gtk.ComboBoxText.new()
		self.lang_menu.append("english", "English")
		self.lang_menu.append("chinese", "Chinese")
		self.lang_menu.append("japanese", "Japanese")
		self.lang_menu.append("spanish", "Spanish")
		self.lang_menu.append("hindi", "Hindi")
		self.lang_menu.append("german", "German")
		self.lang_menu.append("french", "French")
		self.lang_menu.append("italian", "Italian")
		self.lang_menu.append("korean", "Korean")
		self.lang_menu.append("russian", "Russian")
		self.lang_menu.append("other", "Other, User will set up manually.")
		self.grid.attach(self.lang_menu, 1, 3, 1, 1)
		
		self.label2 = Gtk.Label()
		self.label2.set_markup("""

Time Zone""")
		self.label2.set_justify(Gtk.Justification.LEFT)
		self.grid.attach(self.label2, 1, 4, 1, 1)
		
		self.time_menu = Gtk.ComboBoxText.new()
		self.time_menu.append("EST", "Eastern Standard Time")
		self.time_menu.append("CST", "Central Standard Time")
		self.time_menu.append("MST", "Mountain Standard Time")
		self.time_menu.append("PST", "Pacific Standard Time")
		self.time_menu.append("AST", "Alaska Standard Time")
		self.time_menu.append("HST", "Hawaii Standard Time")
		self.time_menu.append("MIT", "Midway Islands Time")
		self.time_menu.append("NST", "New Zealand Standard Time")
		self.time_menu.append("SST", "Soloman Standard Time")
		self.time_menu.append("AET", "Austrailia Eastern Time")
		self.time_menu.append("ACT", "Austrailia Central Time")
		self.time_menu.append("JST", "Japan Standard Time")
		self.time_menu.append("CTT", "China Taiwan Time")
		self.time_menu.append("VST", "Vietnam Standard Time")
		self.time_menu.append("BST", "Bangladesh Standard Time")
		self.time_menu.append("PLT", "Pakistan Lahore Time")
		self.time_menu.append("NET", "Near East Time")
		self.time_menu.append("EAT", "East Africa Time")
		self.time_menu.append("ART", "(Arabic) Egypt Standard Time")
		self.time_menu.append("EET", "Eastern European Time")
		self.time_menu.append("ECT", "European Central Time")
		self.time_menu.append("GMT", "Greenwich Mean Time")
		self.time_menu.append("CAT", "Central African Time")
		self.time_menu.append("BET", "Brazil Eastern Time")
		self.time_menu.append("AGT", "Argentina Standard Time")
		self.time_menu.append("PRT", "Puerto Rico and US Virgin Islands Time")
		self.time_menu.append("IET", "Indiana Eastern Standard Time")
		self.grid.attach(self.time_menu, 1, 5, 1, 1)
		
		self.button1 = Gtk.Button.new_with_label("Okay -->")
		self.button1.connect("clicked", self.onnextclicked)
		self.grid.attach(self.button1, 3, 6, 1, 1)
			
		self.button2 = Gtk.Button.new_with_label("Exit")
		self.button2.connect("clicked", self.onexitclicked)
		self.grid.attach(self.button2, 2, 6, 1, 1)
			
	def onnextclicked(self,button):
			print("%s   %s" % (self.lang_menu.get_active_id(), self.time_menu.get_active_id()))
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

