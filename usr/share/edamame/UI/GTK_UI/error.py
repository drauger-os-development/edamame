#!shebang
# -*- coding: utf-8 -*-
#
#  error.py
#
#  Copyright 2024 Thomas Castleman <batcastle@draugeros.org>
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
"""Error dialog for Edamame"""
from sys import argv
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from UI.GTK_UI import report


class Main(report.Main):
    """UI Error Class"""
    def __init__(self, display, report_setting):
        """set up Error UI"""
        super(Main, self).__init__()
        self.display = display
        self.enable_reporting = report_setting
        self.scrolling = False
        self.main_menu("clicked")

    def main_menu(self, widget):
        """Main Menu"""
        self.clear_window()

        if hasattr(self, 'text_buffer'):
            self.text_buffer.set_text("", length=0)

        self.label = Gtk.Label()
        self.label.set_markup("<b>" + self.display + "</b>")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label = self._set_default_margins(self.label)
        self.grid.attach(self.label, 1, 1, 3, 1)

        if self.enable_reporting:
            self.label2 = Gtk.Label()
            self.label2.set_markup("""
    If you wish to notify the developers of this failed installation,\t\t
    you can send an installation report below.
    """)
            self.label2.set_justify(Gtk.Justification.CENTER)
            self.label2 = self._set_default_margins(self.label2)
            self.grid.attach(self.label2, 1, 2, 3, 1)

            self.button = Gtk.Button.new_with_label("Send Installation report")
            self.button.connect("clicked", self.main)
            self.button = self._set_default_margins(self.button)
            self.grid.attach(self.button, 3, 3, 1, 1)

        self.button2 = Gtk.Button.new_with_label("Exit")
        self.button2.connect("clicked", self.exit)
        self.button2 = self._set_default_margins(self.button2)
        self.grid.attach(self.button2, 1, 3, 1, 1)

        self.show_all()


def show_error(display: str, report_setting: bool = True):
    """Show Error Dialog

    `display` is displayed to the user as the main error text,
    along with instructions on how to send an installation report.
    `report` controls whether or not the user can send an installation report"""
    window = Main(display, report_setting)
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Main.exit)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    DISPLAY = str(argv[1])
    show_error(DISPLAY)
