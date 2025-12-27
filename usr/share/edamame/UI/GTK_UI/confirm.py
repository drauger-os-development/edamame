#!shebang
# -*- coding: utf-8 -*-
#
#  confirm.py
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
"""Confirm UI for Edamame"""
from __future__ import print_function
from sys import argv, stderr
import json
import auto_partitioner as ap
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


class Main(Gtk.Window):
    """UI Confirmation Class"""

    def __init__(self, settings):
        """set up confirmation UI"""
        Gtk.Window.__init__(self, title="Edamame")
        self.install = False
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("system-installer")

        label = Gtk.Label()
        label.set_markup("""
    <span size="x-large"><b>FINAL CONFIRMATION</b></span>
    Please read the below summary carefully.
    This is your final chance to cancel installation.\t
        """)
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 11, 1)

        label1 = Gtk.Label()
        label1.set_markup("""
    <span size="large"><b>PARTITIONS</b></span>
        """)
        label1.set_justify(Gtk.Justification.CENTER)
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 2, 1)

        label5 = Gtk.Label()

        if settings["AUTO_PART"]:
            label = """<b>AUTO PARTITIONING ENABLED</b>\t

<b>INSTALLATION DRIVE:</b> %s""" % (settings["ROOT"])
            if settings["raid_array"]["raid_type"] not in ("OEM", None):
                label = label + """

<b>RAID Type:</b> %s

<b>Drive 1:</b>   %s

<b>Drive 2:</b>   %s""" % (settings["raid_array"]["raid_type"],
                           settings["raid_array"]["disks"]["1"],
                           settings["raid_array"]["disks"]["2"])
                if settings["raid_array"]["raid_type"].lower() == "raid10":
                    label = label + """

<b>Drive 3:</b>   %s

<b>Drive 4:</b>   %s""" % (settings["raid_array"]["disks"]["3"],
                           settings["raid_array"]["disks"]["4"])
            else:
                label = label + """
<b>HOME:</b>      %s""" % (settings["HOME"])
        else:
            label = """<b>ROOT:</b>       %s

<b>EFI:</b>       %s

<b>SWAP:</b>      %s

<b>HOME:</b>     %s""" % (settings["ROOT"], settings["EFI"],
                          settings["SWAP"], settings["HOME"])

        label5.set_markup(label)
        label5.set_justify(Gtk.Justification.CENTER)
        label5 = self._set_default_margins(label5)
        self.grid.attach(label5, 1, 3, 2, (len(label.split("\n")) / 2))

        if "OEM" not in settings.values():
            # Attach the same separator in multiple places
            sep = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
            self.grid.attach(sep, 3, 2, 1, 6)

            label6 = Gtk.Label()
            label6.set_markup("""
    <span size="large"><b>SYSTEM</b></span>
        """)
            label6.set_justify(Gtk.Justification.CENTER)
            label6 = self._set_default_margins(label6)
            self.grid.attach(label6, 4, 2, 2, 1)

            label7 = Gtk.Label()
            label7.set_markup("""  <b>Language:</b>   """)
            label7.set_justify(Gtk.Justification.CENTER)
            label7 = self._set_default_margins(label7)
            self.grid.attach(label7, 4, 3, 1, 1)

            label8 = Gtk.Label()
            label8.set_markup(settings["LANG"])
            label8.set_justify(Gtk.Justification.CENTER)
            label8 = self._set_default_margins(label8)
            self.grid.attach(label8, 5, 3, 1, 1)

            label9 = Gtk.Label()
            label9.set_markup("""  <b>Time Zone:</b>  """)
            label9.set_justify(Gtk.Justification.CENTER)
            label9 = self._set_default_margins(label9)
            self.grid.attach(label9, 4, 4, 1, 1)

            label10 = Gtk.Label()
            label10.set_markup(settings["TIME_ZONE"])
            label10.set_justify(Gtk.Justification.CENTER)
            label10 = self._set_default_margins(label10)
            self.grid.attach(label10, 5, 4, 1, 1)

            label11 = Gtk.Label()
            label11.set_markup("   <b>Computer Name:</b>  ")
            label11.set_justify(Gtk.Justification.CENTER)
            label11 = self._set_default_margins(label11)
            self.grid.attach(label11, 4, 5, 1, 1)

            label12 = Gtk.Label()
            label12.set_markup(settings["COMPUTER_NAME"])
            label12.set_justify(Gtk.Justification.CENTER)
            label12 = self._set_default_margins(label12)
            self.grid.attach(label12, 5, 5, 1, 1)

            if ap.is_EFI():
                label31 = Gtk.Label()
                label31.set_markup("   <b>Compatibility Mode:</b>  ")
                label31.set_justify(Gtk.Justification.CENTER)
                label31 = self._set_default_margins(label31)
                self.grid.attach(label31, 4, 6, 1, 1)

                label32 = Gtk.Label()
                label32.set_markup(str(settings["COMPAT_MODE"]))
                label32.set_justify(Gtk.Justification.CENTER)
                label32 = self._set_default_margins(label32)
                self.grid.attach(label32, 5, 6, 1, 1)

            sep1 = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
            self.grid.attach(sep1, 6, 2, 1, 6)

            label13 = Gtk.Label()
            label13.set_markup("""
    <span size="large"><b>USER</b></span>
        """)
            label13.set_justify(Gtk.Justification.CENTER)
            label13 = self._set_default_margins(label13)
            self.grid.attach(label13, 7, 2, 2, 1)

            label14 = Gtk.Label()
            label14.set_markup(""" <b>Username:</b>   """)
            label14.set_justify(Gtk.Justification.CENTER)
            label14 = self._set_default_margins(label14)
            self.grid.attach(label14, 7, 3, 1, 1)

            label15 = Gtk.Label()
            label15.set_markup(settings["USERNAME"])
            label15.set_justify(Gtk.Justification.CENTER)
            label15 = self._set_default_margins(label15)
            self.grid.attach(label15, 8, 3, 1, 1)

            label16 = Gtk.Label()
            label16.set_markup(""" <b>Password:</b>   """)
            label16.set_justify(Gtk.Justification.CENTER)
            label16 = self._set_default_margins(label16)
            self.grid.attach(label16, 7, 4, 1, 1)

            label17 = Gtk.Label()
            label17.set_markup(settings["PASSWORD"])
            label17.set_justify(Gtk.Justification.CENTER)
            label17 = self._set_default_margins(label17)
            self.grid.attach(label17, 8, 4, 1, 1)

            label23 = Gtk.Label()
            label23.set_markup(""" <b>Auto-Login:</b> """)
            label23.set_justify(Gtk.Justification.CENTER)
            label23 = self._set_default_margins(label23)
            self.grid.attach(label23, 7, 5, 1, 1)

            label24 = Gtk.Label()
            label24.set_markup(str(settings["LOGIN"]))
            label24.set_justify(Gtk.Justification.CENTER)
            label24 = self._set_default_margins(label24)
            self.grid.attach(label24, 8, 5, 1, 1)

            sep2 = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
            self.grid.attach(sep2, 9, 2, 1, 6)

            label18 = Gtk.Label()
            label18.set_markup("""
    <span size="large"><b>OTHER</b></span>
        """)
            label18.set_justify(Gtk.Justification.CENTER)
            label18 = self._set_default_margins(label18)
            self.grid.attach(label18, 10, 2, 2, 1)

            label19 = Gtk.Label()
            label19.set_markup(""" <b>Install Extras:</b> """)
            label19.set_justify(Gtk.Justification.CENTER)
            label19 = self._set_default_margins(label19)
            self.grid.attach(label19, 10, 3, 1, 1)

            label20 = Gtk.Label()
            label20.set_markup(str(settings["EXTRAS"]))
            label20.set_justify(Gtk.Justification.CENTER)
            label20 = self._set_default_margins(label20)
            self.grid.attach(label20, 11, 3, 1, 1)

            label21 = Gtk.Label()
            label21.set_markup(""" <b>Install Updates:</b>    """)
            label21.set_justify(Gtk.Justification.CENTER)
            label21 = self._set_default_margins(label21)
            self.grid.attach(label21, 10, 4, 1, 1)

            label22 = Gtk.Label()
            label22.set_markup(str(settings["UPDATES"]))
            label22.set_justify(Gtk.Justification.CENTER)
            label22 = self._set_default_margins(label22)
            self.grid.attach(label22, 11, 4, 1, 1)

            label25 = Gtk.Label()
            label25.set_markup(""" <b>Keyboard Model:</b> """)
            label25.set_justify(Gtk.Justification.CENTER)
            label25 = self._set_default_margins(label25)
            self.grid.attach(label25, 10, 5, 1, 1)

            label26 = Gtk.Label()
            label26.set_markup(settings["MODEL"])
            label26.set_justify(Gtk.Justification.CENTER)
            label26 = self._set_default_margins(label26)
            self.grid.attach(label26, 11, 5, 1, 1)

            label27 = Gtk.Label()
            label27.set_markup(""" <b>Keyboard Layout:</b>    """)
            label27.set_justify(Gtk.Justification.CENTER)
            label27 = self._set_default_margins(label27)
            self.grid.attach(label27, 10, 6, 1, 1)

            label28 = Gtk.Label()
            label28.set_markup(settings["LAYOUT"])
            label28.set_justify(Gtk.Justification.CENTER)
            label28 = self._set_default_margins(label28)
            self.grid.attach(label28, 11, 6, 1, 1)

            label29 = Gtk.Label()
            label29.set_markup(""" <b>Keyboard Variant:</b>   """)
            label29.set_justify(Gtk.Justification.CENTER)
            label29 = self._set_default_margins(label29)
            self.grid.attach(label29, 10, 7, 1, 1)

            label30 = Gtk.Label()
            label30.set_markup(settings["VARIENT"])
            label30.set_justify(Gtk.Justification.CENTER)
            label30 = self._set_default_margins(label30)
            self.grid.attach(label30, 11, 7, 1, 1)

        button1 = Gtk.Button.new_with_label("INSTALL NOW -->")
        button1.connect("clicked", self.onnextclicked)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 11, 8, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 1, 8, 1, 1)

        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

    def onnextclicked(self, button):
        """set install to false"""
        self.install = True
        self.exit("clicked")

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

    def exit(self, button):
        """exit"""
        Gtk.main_quit("delete-event")
        self.destroy()
        print(1)
        return 1

    def return_install(self):
        """Getter for data"""
        return self.install


def show_confirm(settings, boot_time=False):
    """Show confirmation dialog"""
    window = Main(settings)
    if not boot_time:
        window.set_decorated(True)
    window.set_resizable(False)
    window.connect("delete-event", Main.exit)
    window.show_all()
    Gtk.main()
    data = window.return_install()
    window.exit("clicked")
    return data


if __name__ == "__main__":
    settings = json.loads(argv[1])
    print(show_confirm(settings))
