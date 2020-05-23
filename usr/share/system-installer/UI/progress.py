#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  progress.py
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
"""Progress Window GUI"""
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from os import remove

class Main(Gtk.ApplicationWindow):
    """Progress UI Window"""
    def __init__(self, app):
        """Progress UI main set-up"""
        Gtk.Window.__init__(self, title="System Installer", application=app)
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("system-installer")
        self.set_decorated(True)
        self.set_resizable(False)
        self.set_deletable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.label = Gtk.Label()
        self.label.set_markup("""
\t<b>Installing Drauger OS to your internal hard drive.</b>
This may take some time. If you have an error, please send
the log file (located at /tmp/system-installer.log)
to: contact@draugeros.org   """)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 1, 1, 1, 1)


        self.progress = Gtk.ProgressBar()
        self.progress.set_fraction(0)
        self.progress.set_show_text(True)
        self.grid.attach(self.progress, 1, 3, 1, 1)

        self.file_contents = Gtk.TextBuffer()
        self.text = Gtk.TextView.new_with_buffer(self.file_contents)
        self.text.set_editable(False)
        self.text.set_cursor_visible(False)
        self.text.set_monospace(True)
        self.grid.attach(self.text, 1, 5, 1, 1)

        self.source_id = GLib.timeout_add(33, self.pulse)

    def read_file(self):
        """Read Progress log"""
        text = ""
        try:
            with open("/tmp/system-installer.log", "r") as read_file:
                text = read_file.read()
            self.file_contents.set_text(text, len(text))
        except FileNotFoundError:
            self.file_contents.set_text("", len(""))

        self.show_all()
        return True


    def pulse(self):
        """Update progress indicator and log output in GUI"""
        fraction = ""
        try:
            with open("/tmp/system-installer-progress.log", "r") as prog_file:
                fraction = prog_file.read()
        except FileNotFoundError:
            fraction = 0
        try:
            fraction = int(fraction) / 100
            self.progress.set_fraction(fraction)
        except ValueError:
            self.progress.set_fraction(0)
        if fraction == 1:
            remove("/tmp/system-installer-progress.log")
            remove("/mnt/tmp/system-installer-progress.log")
            sys.exit(0)

        self.show_all()
        self.read_file()
        return True

class Worker(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = Main(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

def show_progress():
    """Show Progress UI"""
    window = Worker()
    exit_status = window.run(sys.argv)
    # sys.exit(exit_status)

if __name__ == '__main__':
    show_progress()
