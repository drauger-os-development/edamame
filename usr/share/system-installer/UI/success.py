#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  success.py
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
from subprocess import Popen, check_output, PIPE, STDOUT
from os import remove, listdir, getenv
from shutil import rmtree
from datetime import datetime
import UI.report as report

class main(Gtk.Window):

    def __init__(self):
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
        self.label.set_markup("""\n\t<b>Drauger OS has been successfully installed on your computer!</b>\t

\tPlease consider sending an installtion report to our team,
\tusing the "Send Installation Report" button below.\t\n\n""")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 1, 1, 4, 1)

        self.button1 = Gtk.Button.new_with_label("Restart System")
        self.button1.connect("clicked", self.onnextclicked)
        self.grid.attach(self.button1, 2, 6, 1, 1)

        self.button2 = Gtk.Button.new_with_label("Exit")
        self.button2.connect("clicked", self.exit)
        self.grid.attach(self.button2, 1, 6, 1, 1)

        self.button2 = Gtk.Button.new_with_label("Advanced")
        self.button2.connect("clicked", self.onadvclicked)
        self.grid.attach(self.button2, 3, 6, 1, 1)

        self.button4 = Gtk.Button.new_with_label("Send Installation Report")
        self.button4.connect("clicked", self.main)
        self.grid.attach(self.button4, 4, 6, 1, 1)

        self.show_all()

    def onnextclicked(self,button):
        Popen(["systemctl", "reboot", "now"])
        exit(0)

    def onadvclicked(self,button):
        self.clear_window()

        self.label = Gtk.Label()
        self.label.set_markup("""\n The below options are meant exclusivly for advanced users. <b>User discretion is advised.</b>   \n""")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 1, 1, 3, 1)

        self.button1 = Gtk.Button.new_with_label("Open Chroot Terminal")
        self.button1.connect("clicked", self.chrootclicked)
        self.grid.attach(self.button1, 3, 6, 1, 1)

        self.button2 = Gtk.Button.new_with_label("Delete Installation")
        self.button2.connect("clicked", self.ondeletewarn)
        self.grid.attach(self.button2, 1, 6, 1, 1)

        self.button3 = Gtk.Button.new_with_label("Add PPA")
        self.button3.connect("clicked", self.addPPA)
        self.grid.attach(self.button3, 2, 6, 1, 1)

        self.button4 = Gtk.Button.new_with_label("Exit")
        self.button4.connect("clicked", self.exit)
        self.grid.attach(self.button4, 2, 7, 1, 1)

        self.show_all()

    def ondeletewarn(self,button):
        self.clear_window()

        self.label.set_markup("""\n\tAre you sure you wish to delete the new installation? No data will be recoverable.\t\n""")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 1, 1, 3, 1)

        self.button5 = Gtk.Button.new_with_label("DELETE")
        self.button5.connect("clicked", self.delete_install)
        self.grid.attach(self.button5,2, 2, 1, 1)

        self.button4 = Gtk.Button.new_with_label("Exit")
        self.button4.connect("clicked", self.exit)
        self.grid.attach(self.button4, 3, 2, 1, 1)

        self.button5 = Gtk.Button.new_with_label("<-- Back")
        self.button5.connect("clicked",self.onadvclicked)
        self.grid.attach(self.button5, 1, 2, 1, 1)

        self.show_all()

    def delete_install(self,button):
        # This code is dangerous. Be wary
        delete = listdir("/mnt")
        for each in delete:
            try:
                remove("/mnt/" + each)
            except IsADirectoryError:
                rmtree("/mnt/" + each)
        self.exit("clicked")


    def chrootclicked(self,button):
        Popen(["gnome-terminal", "--", "arch-chroot", "/mnt"])
        exit(0)

    def addPPA(self,button):
        self.clear_window()

        self.label = Gtk.Label()
        self.label.set_markup("""\n\tWhat PPAs would you like to add?\t\n""")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 1, 1, 3, 1)

        self.label1 = Gtk.Label()
        self.label1.set_markup("""\tPPA:""")
        self.label1.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(self.label1, 1, 2, 1, 1)

        self.PPAentry = Gtk.Entry()
        self.PPAentry.set_visibility(True)
        self.grid.attach(self.PPAentry, 2, 2, 1, 1)

        self.button4 = Gtk.Button.new_with_label("Add PPA")
        self.button4.connect("clicked", self.addPPA_backend)
        self.grid.attach(self.button4, 2, 3, 1, 1)

        self.button4 = Gtk.Button.new_with_label("Exit")
        self.button4.connect("clicked", self.exit)
        self.grid.attach(self.button4, 3, 3, 1, 1)

        self.button5 = Gtk.Button.new_with_label("<-- Back")
        self.button5.connect("clicked",self.onadvclicked)
        self.grid.attach(self.button5, 1, 3, 1, 1)

        self.show_all()

    def addPPA_backend(self,button):
        self.grid.remove(self.label)
        try:
            Popen(["add-apt-repository","--yes","PPA:%s" % ((self.PPAentry.get_text()).lower())])

            self.label = Gtk.Label()
            self.label.set_markup("""\n\tWhat PPAs would you like to add?\t\n\t<b>%s added successfully!</b>\t\n""" % (self.PPAentry.get_text()))
            self.label.set_justify(Gtk.Justification.CENTER)
            self.grid.attach(self.label, 1, 1, 2, 1)
        except:
            self.label = Gtk.Label()
            self.label.set_markup("""\n\tWhat PPAs would you like to add?\t\n\t<b>adding %s failed.</b>\t\n""" % (self.PPAentry.get_text()))
            self.label.set_justify(Gtk.Justification.CENTER)
            self.grid.attach(self.label, 1, 1, 2, 1)

        self.PPAentry.set_text("")

        self.show_all()

    def exit(self,button):
        Gtk.main_quit("delete-event")
        self.destroy()
        return(0)

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

def exit_button(x,y):
    Gtk.main_quit("delete-event")
    exit(1)

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

def show_success():
    window = main()
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event",main.exit)
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    show_success()
