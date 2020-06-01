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
"""Success Reporting UI"""
from subprocess import Popen, CalledProcessError
from os import remove, listdir
from shutil import rmtree
import sys
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import UI.report as report

class Main(Gtk.Window):
    """Success UI Class"""
    def __init__(self, settings):
        """Initialize data"""
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
        self.settings = settings
        self.main_menu("clicked")

    def main_menu(self, widget):
        """Main Success Window"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
\t<b>Drauger OS has been successfully installed on your computer!</b>\t

\tPlease consider sending an installtion report to our team,
\tusing the "Send Installation Report" button below.\t\n\n""")
        label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(label, 1, 1, 4, 1)

        button1 = Gtk.Button.new_with_label("Restart System")
        button1.connect("clicked", __reboot__)
        self.grid.attach(button1, 2, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 1, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("Advanced")
        button3.connect("clicked", self.onadvclicked)
        self.grid.attach(button3, 3, 6, 1, 1)

        button4 = Gtk.Button.new_with_label("Send Installation Report")
        button4.connect("clicked", self.main)
        self.grid.attach(button4, 4, 6, 1, 1)

        self.show_all()

    def onadvclicked(self, button):
        """Advanced Settings and Functions"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
 The below options are meant exclusivly for advanced users.

 <b>User discretion is advised.</b>

 """)
        label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(label, 1, 1, 3, 1)

        button1 = Gtk.Button.new_with_label("Dump Settings to File")
        button1.connect("clicked", self.dump_settings_dialog)
        self.grid.attach(button1, 3, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Delete Installation")
        button2.connect("clicked", self.ondeletewarn)
        self.grid.attach(button2, 1, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("Add PPA")
        button3.connect("clicked", self.add_ppa)
        self.grid.attach(button3, 2, 6, 1, 1)

        button4 = Gtk.Button.new_with_label("Exit")
        button4.connect("clicked", self.exit)
        self.grid.attach(button4, 3, 7, 1, 1)

        button5 = Gtk.Button.new_with_label("<-- Back")
        button5.connect("clicked", self.main_menu)
        self.grid.attach(button5, 1, 7, 1, 1)

        self.show_all()

    def ondeletewarn(self, button):
        """Warning about Deleting the installation"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
\tAre you sure you wish to delete the new installation? No data will be recoverable.\t
""")
        label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(label, 1, 1, 3, 1)

        button5 = Gtk.Button.new_with_label("DELETE")
        button5.connect("clicked", self.delete_install)
        self.grid.attach(button5, 2, 2, 1, 1)

        button4 = Gtk.Button.new_with_label("Exit")
        button4.connect("clicked", self.exit)
        self.grid.attach(button4, 3, 2, 1, 1)

        button5 = Gtk.Button.new_with_label("<-- Back")
        button5.connect("clicked", self.onadvclicked)
        self.grid.attach(button5, 1, 2, 1, 1)

        self.show_all()

    def delete_install(self, button):
        """Delete Installation from Drive
         This code is dangerous. Be wary
        """
        delete = listdir("/mnt")
        for each in delete:
            try:
                remove("/mnt/" + each)
            except IsADirectoryError:
                rmtree("/mnt/" + each)
        self.exit("clicked")

    def add_ppa(self, button):
        """UI to add PPA to installation"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""\n\tWhat PPAs would you like to add?\t\n""")
        label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(label, 1, 1, 3, 1)

        label1 = Gtk.Label()
        label1.set_markup("""\tPPA:""")
        label1.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label1, 1, 2, 1, 1)

        self.ppa_entry = Gtk.Entry()
        self.ppa_entry.set_visibility(True)
        self.grid.attach(self.ppa_entry, 2, 2, 1, 1)

        button4 = Gtk.Button.new_with_label("Add PPA")
        button4.connect("clicked", self.add_ppa_backend)
        self.grid.attach(button4, 2, 3, 1, 1)

        button4 = Gtk.Button.new_with_label("Exit")
        button4.connect("clicked", self.exit)
        self.grid.attach(button4, 3, 3, 1, 1)

        button5 = Gtk.Button.new_with_label("<-- Back")
        button5.connect("clicked", self.onadvclicked)
        self.grid.attach(button5, 1, 3, 1, 1)

        self.show_all()

    def add_ppa_backend(self, button):
        """Unfunction to add PPAs"""
        self.grid.remove(self.grid.get_child_at(1, 1))
        try:
            Popen(["add-apt-repository", "--yes", "PPA:%s" %
                   ((self.ppa_entry.get_text()).lower())])

            label = Gtk.Label()
            label.set_markup("""\n\tWhat PPAs would you like to add?\t
\t<b>%s added successfully!</b>\t\n""" % (self.ppa_entry.get_text()))
            label.set_justify(Gtk.Justification.CENTER)
            self.grid.attach(label, 1, 1, 2, 1)
        except CalledProcessError:
            label = Gtk.Label()
            label.set_markup("""\n\tWhat PPAs would you like to add?\t
\t<b>adding %s failed.</b>\t\n""" % (self.ppa_entry.get_text()))
            label.set_justify(Gtk.Justification.CENTER)
            self.grid.attach(label, 1, 1, 2, 1)

        self.ppa_entry.set_text("")

        self.show_all()

    def exit(self, button):
        """Exit"""
        Gtk.main_quit("delete-event")
        self.destroy()
        return 0

    def clear_window(self):
        """Clear Winodw"""
        children = self.grid.get_children()
        for each in children:
            self.grid.remove(each)
        if self.scrolling:
            self.scrolled_window.remove(self.grid)
            self.remove(self.scrolled_window)
            self.add(self.grid)
            self.scrolling = False
            self.set_default_size(-1, -1)

    def dump_settings_dialog(self, button):
        """Dump Settings Dialog"""
        dialog = Gtk.FileChooserDialog("System Installer", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))


        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            data = dialog.get_filename()
            dump_settings(self.settings, data)

        dialog.destroy()

def dump_settings(settings, path):
    """Dump Settings to File"""
    with open(path, "w+") as dump_file:
        json.dump(settings, dump_file, indent=1)

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

def show_success(settings):
    """Show Success UI"""
    window = Main(settings)
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Main.exit)
    window.show_all()
    Gtk.main()

def __reboot__(button):
    Popen(["systemctl", "reboot", "now"])
    sys.exit(0)

if __name__ == '__main__':
    show_success(sys.argv[1])
