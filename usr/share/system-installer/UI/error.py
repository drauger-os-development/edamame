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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sys import argv
from subprocess import Popen, check_output, PIPE, STDOUT
from os import remove, listdir, getenv
from datetime import datetime
import UI.report as report

class main(Gtk.Window):
    def __init__(self):
        global display
        Gtk.Window.__init__(self, title="System Installer")
        self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_from_file("/usr/share/icons/Drauger/720x720/Menus/install-drauger.png")
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
        self.clear_window()

        self.label = Gtk.Label()
        self.label.set_markup("<b>" + display  + "</b>")
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
        children = self.grid.get_children()
        for each in children:
            self.grid.remove(each)
        if (self.scrolling):
            self.scrolled_window.remove(self.grid)
            self.remove(self.scrolled_window)
            self.add(self.grid)
            self.scrolling = False
            self.set_default_size(-1, -1)

    def exit(self,button):
        Gtk.main_quit("delete-event")
        self.destroy()
        return(0)

main.main = report.main.main
main.toggle_UI = report.main.toggle_UI
main.message_accept = report.main.message_accept
main.message_handler = report.main.message_handler
main.generate_message = report.main.generate_message
main.preview_message = report.main.preview_message
main.send_report = report.main.send_report
main.cpu_explaination = report.main.cpu_explaination
main.cpu_toggle = report.main.cpu_toggle
main.disk_explaination = report.main.disk_explaination
main.disk_toggle = report.main.disk_toggle
main.generate_message = report.main.generate_message
main.gpu_explaination = report.main.gpu_explaination
main.gpu_toggle = report.main.gpu_toggle
main.log_explaination = report.main.log_explaination
main.log_toggle = report.main.log_toggle
main.ram_explaination = report.main.ram_explaination
main.ram_toggle = report.main.ram_toggle
main.toggle_UI = report.main.toggle_UI
main.main = report.main.main

def show_main():
    window = main()
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    display = str(argv[1])
    show_main()
