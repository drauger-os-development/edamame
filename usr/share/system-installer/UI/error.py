#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  error.py
#
#  Copyright 2020 Thomas Castleman <contact@draugeros.org>
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
"""Error dialog for System Installer"""
from sys import argv
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import UI.report as report


class Main(Gtk.Window):
    """UI Error Class"""
    def __init__(self, display):
        """set up Error UI"""
        self.display = display
        Gtk.Window.__init__(self, title="System Installer")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("system-installer")
        self.scrolling = False
        self.opt_setting = False
        self.cpu_setting = False
        self.gpu_setting = False
        self.ram_setting = False
        self.disk_setting = False
        self.log_setting = False
        self.custom_setting = False
        self.main_menu("clicked")

    def main_menu(self, widget):
        """Main Menu"""
        self.clear_window()

        self.label = Gtk.Label()
        self.label.set_markup("<b>" + self.display  + "</b>")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 1, 1, 3, 1)

        self.label2 = Gtk.Label()
        self.label2.set_markup("""
    If you wish to notify the developers of this failed installation,\t\t
    you can send an installation report below.
    """)
        self.label2.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label2, 1, 2, 3, 1)

        self.button2 = Gtk.Button.new_with_label("Exit")
        self.button2.connect("clicked", self.exit)
        self.grid.attach(self.button2, 1, 3, 1, 1)

        self.button = Gtk.Button.new_with_label("Send Installation report")
        self.button.connect("clicked", self.main)
        self.grid.attach(self.button, 3, 3, 1, 1)

        self.show_all()

    def clear_window(self):
        """Clear window of everything"""
        children = self.grid.get_children()
        for each in children:
            self.grid.remove(each)
        if self.scrolling:
            self.scrolled_window.remove(self.grid)
            self.remove(self.scrolled_window)
            self.add(self.grid)
            self.scrolling = False
            self.set_default_size(-1, -1)

    def exit(self, button):
        """Exit"""
        Gtk.main_quit("delete-event")
        self.destroy()
        return 0

Main.main = report.Main.main
Main.toggle_ui = report.Main.toggle_ui
Main.message_accept = report.Main.message_accept
Main.message_handler = report.Main.message_handler
Main.generate_message = report.Main.generate_message
Main.preview_message = report.Main.preview_message
Main.send_report = report.Main.send_report
Main.cpu_explaination = report.Main.cpu_explaination
Main.cpu_toggle = report.Main.cpu_toggle
Main.disk_explaination = report.Main.disk_explaination
Main.disk_toggle = report.Main.disk_toggle
Main.generate_message = report.Main.generate_message
Main.gpu_explaination = report.Main.gpu_explaination
Main.gpu_toggle = report.Main.gpu_toggle
Main.log_explaination = report.Main.log_explaination
Main.log_toggle = report.Main.log_toggle
Main.ram_explaination = report.Main.ram_explaination
Main.ram_toggle = report.Main.ram_toggle

def show_error(display):
    """Show Error Dialog"""
    window = Main(display)
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Main.exit)
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    DISPLAY = str(argv[1])
    show_error(DISPLAY)
