#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  confirm.py
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
from __future__ import print_function
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sys import argv

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class main(Gtk.Window):

    def __init__(self, AUTO_PART, ROOT, EFI, HOME, SWAP, LANG, TIME_ZONE, USERNAME, PASS, COMPNAME, EXTRAS, UPDATES, LOGIN, MODEL, LAYOUT, VARIENT):
        Gtk.Window.__init__(self, title="System Installer")
        self.install = False
        self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_from_file("/usr/share/icons/Drauger/720x720/Menus/install-drauger.png")

        self.label = Gtk.Label()
        self.label.set_markup("""
    <b>FINAL CONFIRMATION</b>
    Please read the below summary carefully.
    This is your final chance to cancel installation.\t
        """)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 1, 1, 3, 1)

        self.label1 = Gtk.Label()
        self.label1.set_markup("""
    <b>PARTITIONS</b>
        """)
        self.label1.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label1, 1, 2, 3, 1)

        self.label4 = Gtk.Label()
        self.label4.set_markup("""  Partitioning:   """)
        self.label4.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label4, 1, 4, 1, 1)

        self.label5 = Gtk.Label()

        if (AUTO_PART == "True"):
            self.label5.set_markup("""AUTO PARTITIONING ENABLED\t
INSTALLATION DRIVE: %s""" % (ROOT))
        else:
            self.label5.set_markup("""ROOT: %s
EFI: %s
HOME: %s
SWAP: %s""" % (ROOT,EFI,HOME,SWAP))

        self.label5.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(self.label5, 3, 4, 1, 1)

        self.label6 = Gtk.Label()
        self.label6.set_markup("""
    <b>SYSTEM</b>
        """)
        self.label6.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label6, 1, 5, 3, 1)

        self.label7 = Gtk.Label()
        self.label7.set_markup("""  Language:   """)
        self.label7.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label7, 1, 6, 1, 1)

        self.label8 = Gtk.Label()
        self.label8.set_markup(LANG)
        self.label8.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label8, 3, 6, 1, 1)

        self.label9 = Gtk.Label()
        self.label9.set_markup("""  Time Zone:  """)
        self.label9.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label9, 1, 7, 1, 1)

        self.label10 = Gtk.Label()
        self.label10.set_markup(TIME_ZONE)
        self.label10.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label10, 3, 7, 1, 1)

        self.label11 = Gtk.Label()
        self.label11.set_markup("   Computer Name:  ")
        self.label11.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label11, 1, 8, 1, 1)

        self.label12 = Gtk.Label()
        self.label12.set_markup(COMPNAME)
        self.label12.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label12, 3, 8, 1, 1)

        self.label13 = Gtk.Label()
        self.label13.set_markup("""
    <b>USER</b>
        """)
        self.label13.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label13, 1, 9, 3, 1)

        self.label14 = Gtk.Label()
        self.label14.set_markup(""" Username:   """)
        self.label14.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label14, 1, 10, 1, 1)

        self.label15 = Gtk.Label()
        self.label15.set_markup(USERNAME)
        self.label15.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label15, 3, 10, 1, 1)

        self.label16 = Gtk.Label()
        self.label16.set_markup(""" Password:   """)
        self.label16.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label16, 1, 11, 1, 1)

        self.label17 = Gtk.Label()
        self.label17.set_markup(PASS)
        self.label17.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label17, 3, 11, 1, 1)

        self.label23 = Gtk.Label()
        self.label23.set_markup(""" Auto-Login: """)
        self.label23.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label23, 1, 12, 1, 1)

        self.label24 = Gtk.Label()
        self.label24.set_markup(str(LOGIN))
        self.label24.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label24, 3, 12, 1, 1)

        self.label18 = Gtk.Label()
        self.label18.set_markup("""
    <b>OTHER</b>
        """)
        self.label18.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label18, 1, 13, 3, 1)

        self.label19 = Gtk.Label()
        self.label19.set_markup(""" Install Extras: """)
        self.label19.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label19, 1, 14, 1, 1)

        self.label20 = Gtk.Label()
        self.label20.set_markup(str(EXTRAS))
        self.label20.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label20, 3, 14, 1, 1)

        self.label21 = Gtk.Label()
        self.label21.set_markup(""" Install Updates:    """)
        self.label21.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label21, 1, 15, 1, 1)

        self.label22 = Gtk.Label()
        self.label22.set_markup(str(UPDATES))
        self.label22.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label22, 3, 15, 1, 1)

        self.label25 = Gtk.Label()
        self.label25.set_markup(""" Keyboard Model: """)
        self.label25.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label25, 1, 16, 1, 1)

        self.label26 = Gtk.Label()
        self.label26.set_markup(MODEL)
        self.label26.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label26, 3, 16, 1, 1)

        self.label27 = Gtk.Label()
        self.label27.set_markup(""" Keyboard Layout:    """)
        self.label27.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label27, 1, 17, 1, 1)

        self.label28 = Gtk.Label()
        self.label28.set_markup(LAYOUT)
        self.label28.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label28, 3, 17, 1, 1)

        self.label29 = Gtk.Label()
        self.label29.set_markup(""" Keyboard Varient:   """)
        self.label29.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label29, 1, 18, 1, 1)

        self.label30 = Gtk.Label()
        self.label30.set_markup(VARIENT)
        self.label30.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label30, 3, 18, 1, 1)

        self.button1 = Gtk.Button.new_with_label("INSTALL NOW -->")
        self.button1.connect("clicked", self.onnextclicked)
        self.grid.attach(self.button1, 3, 19, 1, 1)

        self.button2 = Gtk.Button.new_with_label("Exit")
        self.button2.connect("clicked", self.exit)
        self.grid.attach(self.button2, 1, 19, 1, 1)

    def onnextclicked(self,button):
        self.install = True
        self.exit("clicked")

    def onexitclicked(self,button):
        self.install = False
        self.exit("clicked")

    def exit(self, button):
        Gtk.main_quit("delete-event")
        self.destroy()
        print(1)
        return(1)

    def return_install(self):
        return self.install

def show_confirm(auto_part, root, efi, home, swap, lang, time_zone, username, password, comp_name, extras, updates, login, model, layout, varient):
    window = main(auto_part, root, efi, home, swap, lang, time_zone, username, password, comp_name, extras, updates, login, model, layout, varient)
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", main.exit)
    window.show_all()
    Gtk.main()
    data = window.return_install()
    window.exit("clicked")
    return data

if __name__ == '__main__':
    SETTINGS = argv[1]
    SETTINGS = SETTINGS.split(" , ")

    # Partitioning settings
    AUTO_PART = SETTINGS[0]
    ROOT = SETTINGS[1]
    EFI = SETTINGS[2]
    HOME = SETTINGS[3]
    SWAP = SETTINGS[4]

    # Locale settings
    LANG = SETTINGS[5]
    TIME_ZONE = SETTINGS[6]

    # User settings
    USERNAME = SETTINGS[7]
    COMPNAME = SETTINGS[8]
    PASS = SETTINGS[9]

    # Options settings
    EXTRAS = SETTINGS[10]
    UPDATES = SETTINGS[11]
    LOGIN = SETTINGS[12]

    #Keyboard Settings
    MODEL = SETTINGS[13]
    LAYOUT = SETTINGS[14]
    VARIENT = SETTINGS[15]
    if EXTRAS != "0" and EXTRAS != None:
        EXTRAS = "Yes"
    else:
        EXTRAS = "No"
    if UPDATES != "0" and UPDATES != None:
        UPDATES = "Yes"
    else:
        UPDATES = "No"
    if LOGIN != "0" and LOGIN != None:
        LOGIN = "Yes"
    else:
        LOGIN = "No"

    show_confirm(AUTO_PART, ROOT, EFI, HOME, SWAP, LANG, TIME_ZONE, USERNAME,
        PASS, COMPNAME, EXTRAS, UPDATES, LOGIN, MODEL, LAYOUT, VARIENT)
