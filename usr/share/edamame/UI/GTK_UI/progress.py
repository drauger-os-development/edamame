#!shebang
# -*- coding: utf-8 -*-
#
#  progress.py
#
#  Copyright 2025 Thomas Castleman <batcastle@draugeros.org>
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
import signal
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from os import remove

window = None


class Main(Gtk.ApplicationWindow):
    """Progress UI Window"""
    def __init__(self, app, distro="Linux"):
        """Progress UI main set-up"""
        Gtk.Window.__init__(self, title="Edamame", application=app)
        # Gtk.Window.__init__(self, title="System Installer")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("system-installer")
        self.set_decorated(True)
        self.set_resizable(False)
        self.set_deletable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.distro = distro

        self.label = Gtk.Label()
        self.label.set_markup("""
\t<b>Installing %s to your internal hard drive.</b>\t
\tThis may take some time. If you have an error, please send\t
the log file (located at /tmp/edamame.log)
to: contact@draugeros.org   """ % (self.distro))
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label = self._set_default_margins(self.label)
        self.grid.attach(self.label, 1, 1, 1, 1)

        self.progress = Gtk.ProgressBar()
        self.progress.set_fraction(0)
        self.progress.set_show_text(True)
        self.progress = self._set_default_margins(self.progress)
        self.grid.attach(self.progress, 1, 3, 1, 1)

        self.file_contents = Gtk.TextBuffer()
        self.text = Gtk.TextView.new_with_buffer(self.file_contents)
        self.text.set_editable(False)
        self.text.set_cursor_visible(False)
        self.text.set_monospace(True)
        self.text = self._set_default_margins(self.text)
        self.grid.attach(self.text, 1, 5, 1, 1)

        self.set_position(Gtk.WindowPosition.CENTER)

        self.source_id = GLib.timeout_add(33, self.pulse)

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

    def read_file(self):
        """Read Progress log"""
        text = ""
        try:
            with open("/tmp/edamame.log", "r") as read_file:
                text = read_file.read()
            if len(text.split("\n")) > 10:
                text = text.split("\n")
                text = text[-10:]
                for each in enumerate(text):
                    if len(text[each[0]]) > 90:
                        text[each[0]] = text[each[0]][:90]
                    elif len(text[each[0]]) < 90:
                        multiplyer = 90 - len(text[each[0]])
                        text[each[0]] = text[each[0]] + (" " * multiplyer)
                text = "\n".join(text)
            self.file_contents.set_text(text, len(text))
        except FileNotFoundError:
            self.file_contents.set_text("", len(""))

        self.show_all()
        return True


    def pulse(self):
        """Update progress indicator and log output in GUI"""
        fraction = ""
        try:
            with open("/tmp/edamame-progress.log", "r") as prog_file:
                fraction = prog_file.read()
        except FileNotFoundError:
            fraction = 0
        try:
            fraction = int(fraction) / 100
            self.progress.set_fraction(fraction)
        except ValueError:
            self.progress.set_fraction(0)
        if fraction == 1:
            remove("/tmp/edamame-progress.log")
            remove("/mnt/tmp/edamame-progress.log")
            Gtk.main_quit("delete-event")
            self.destroy()
            self.source_id = None
            return False

        self.show_all()
        self.read_file()
        return True


class Worker(Gtk.Application):
    """Progress Window Worker"""
    def __init__(self, distro):
        self.distro = str(distro)
        Gtk.Application.__init__(self)
        self.win = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        self.win = Main(self, distro=self.distro)
        self.win.show_all()


def show_progress():
    """Show Progress UI"""
    try:
        with open("/etc/edamame/settings.json", "r") as file:
            distro = json.load(file)["distro"]
    except (FileNotFoundError, KeyError):
        distro = "Linux"
    signal.signal(signal.SIGTERM, handle_sig_term)
    global window
    window = Worker(distro)
    exit_status = window.run([])


def handle_sig_term(signum, frame):
    global window
    window.win.destroy()
    exit()


if __name__ == '__main__':
    show_progress()
