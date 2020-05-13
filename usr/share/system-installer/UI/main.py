#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
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
"""Main Installation UI"""
from __future__ import print_function
from subprocess import Popen, check_output, DEVNULL
from os import getcwd, chdir, path, listdir
import sys
import re
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)

def has_special_character(input_string):
    """Check for special characters"""
    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(input_string) is None:
        return False
    else:
        return True

def hasspace(input_string):
    """Check for spaces"""
    for each3 in input_string:
        if each3.isspace():
            return True
    return False


try:
    CONFIG_DIR = listdir("/etc/system-installer")
    for each in enumerate(CONFIG_DIR):
        if CONFIG_DIR[each[0]] == "quick-install-template.json":
            del CONFIG_DIR[each[0]]
            if len(CONFIG_DIR) == 1:
                break
            else:
                for each1 in enumerate(CONFIG_DIR):
                    if CONFIG_DIR[each1[0]] == "default.json":
                        del CONFIG_DIR[each[0]]
                        if len(CONFIG_DIR) != 1:
                            eprint("More than one custom config file in /etc/system-installer is not supported.")
                            eprint("Please remove all but one and try again.")
                            eprint("'default.config' and 'quick-install-template.config' may remain though.")
                            sys.exit(2)
                        else:
                            break
                break
    with open("/etc/system-installer/%s" % (CONFIG_DIR[0])) as config_file:
        DISTRO = json.loads(config_file.read())["distro"]


except FileNotFoundError:
    eprint("/etc/system-installer does not exist. In testing?")
    DISTRO = "Drauger OS"




DEFAULT = """
    Welcome to the %s System Installer!

    A few things before we get started:

    <b>PARTITIONING</b>

    The %s System Installer uses Gparted to allow the user to set up their partitions
    It is advised to account for this if installing next to another OS.
    If using automatic partitoning, it will take up the entirety of the drive told to use.
    Loss of data from usage of this tool is entirely at the fault of the user.
    You have been warned.

    <b>ALPHA WARNING</b>

    The %s System Installer is currently in alpha.
    Expect bugs.
    """ % (DISTRO, DISTRO, DISTRO)

KEYBOARD_COMPLETION = "TO DO"
USER_COMPLETION = "TO DO"
PART_COMPLETION = "TO DO"
LOCALE_COMPLETION = "TO DO"
OPTIONS_COMPLETION = "TO DO"

class Main(Gtk.Window):
    """Main UI Window"""
    def __init__(self):
        """Initialize the Window"""
        Gtk.Window.__init__(self, title="System Installer")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("system-installer")

        # Initialize setting values
        self.root_setting = ""
        self.efi_setting = ""
        self.home_setting = ""
        self.swap_setting = ""
        self.auto_part_setting = ""
        self.lang_setting = ""
        self.time_zone = ""
        self.username_setting = ""
        self.compname_setting = ""
        self.password_setting = ""
        self.extras_setting = ""
        self.updates_setting = ""
        self.login_setting = ""
        self.model_setting = ""
        self.layout_setting = ""
        self.varient_setting = ""
        self.data = {}

        # Open initial window
        self.reset("clicked")

    def quick_install_warning(self, button):
        """Quick Install Mode Entry Point"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>QUICK INSTALL MODE INITIATED</b>

    You have activated Quick Install mode.

    This mode allows users to provide the system installation utility with
    a config file containing their prefrences for installation and set up.

    An example of one of these can be found at /etc/system-installer/quick-install-template.json\t
    """)
        label.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label, 1, 1, 3, 1)

        button4 = Gtk.Button.new_with_label("Select Config File")
        button4.connect("clicked", self.select_config)
        self.grid.attach(button4, 3, 2, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.reset)
        self.grid.attach(button3, 2, 2, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 1, 2, 1, 1)

        self.show_all()

    def reset(self, button):
        """Main Splash Window"""
        global DEFAULT
        self.clear_window()

        label = Gtk.Label()
        label.set_markup(DEFAULT)
        label.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label, 1, 1, 3, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.main_menu)
        self.grid.attach(button1, 3, 2, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 1, 2, 1, 1)

        button3 = Gtk.Button.new_with_label("Quick Install")
        button3.connect("clicked", self.quick_install_warning)
        self.grid.attach(button3, 2, 2, 1, 1)

        self.show_all()

    def select_config(self, widget):
        """Quick Install File Selection Window"""
        eprint("\t###\tQUICK INSTALL MODE ACTIVATED\t###\t")
        dialog = Gtk.FileChooserDialog("System Installer", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.data = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            self.data = 1

        dialog.destroy()
        self.exit("clicked")

    def add_filters(self, dialog):
        """Add Filters to Quick Install File Selection Window"""
        filter_text = Gtk.FileFilter()
        filter_text.set_name("JSON")
        filter_text.add_mime_type("application/json")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def main_menu(self, button):
        """Main Menu"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
        Feel free to complete any of the below segments in any order.\t
        However, all segments must be completed.\n""")
        self.grid.attach(label, 2, 1, 2, 1)

        completion_label = Gtk.Label()
        completion_label.set_markup("""<b>COMPLETION</b>""")
        self.grid.attach(completion_label, 2, 2, 1, 1)

        button8 = Gtk.Button.new_with_label("Keyboard")
        button8.connect("clicked", self.keyboard)
        self.grid.attach(button8, 3, 3, 1, 1)

        label_keyboard = Gtk.Label()
        label_keyboard.set_markup(KEYBOARD_COMPLETION)
        self.grid.attach(label_keyboard, 2, 3, 1, 1)

        button4 = Gtk.Button.new_with_label("Locale and Time")
        button4.connect("clicked", self.locale)
        self.grid.attach(button4, 3, 4, 1, 1)

        label_locale = Gtk.Label()
        label_locale.set_markup(LOCALE_COMPLETION)
        self.grid.attach(label_locale, 2, 4, 1, 1)

        button5 = Gtk.Button.new_with_label("Options")
        button5.connect("clicked", self.options)
        self.grid.attach(button5, 3, 5, 1, 1)

        label_options = Gtk.Label()
        label_options.set_markup(OPTIONS_COMPLETION)
        self.grid.attach(label_options, 2, 5, 1, 1)

        button6 = Gtk.Button.new_with_label("Partitioning")
        button6.connect("clicked", self.partitioning)
        self.grid.attach(button6, 3, 6, 1, 1)

        label_part = Gtk.Label()
        label_part.set_markup(PART_COMPLETION)
        self.grid.attach(label_part, 2, 6, 1, 1)

        button7 = Gtk.Button.new_with_label("User Settings")
        button7.connect("clicked", self.user)
        self.grid.attach(button7, 3, 7, 1, 1)

        label_user = Gtk.Label()
        label_user.set_markup(USER_COMPLETION)
        self.grid.attach(label_user, 2, 7, 1, 1)

        button1 = Gtk.Button.new_with_label("DONE")
        button1.connect("clicked", self.done)
        self.grid.attach(button1, 4, 8, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 1, 8, 1, 1)

        self.show_all()

    def user(self, button):
        """User setup Window"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>Set Up Main User</b>
        """)
        label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(label, 1, 1, 3, 1)

        label1 = Gtk.Label()
        label1.set_markup("    Username:   ")
        label1.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label1, 1, 3, 2, 1)

        self.username = Gtk.Entry()
        self.username.set_text(self.username_setting)
        self.grid.attach(self.username, 3, 3, 1, 1)

        label2 = Gtk.Label()
        label2.set_markup("    Computer\'s Name:   ")
        label2.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label2, 1, 4, 2, 1)

        self.compname = Gtk.Entry()
        self.compname.set_text(self.compname_setting)
        self.grid.attach(self.compname, 3, 4, 1, 1)

        label3 = Gtk.Label()
        label3.set_markup("    Password:   ")
        label3.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label3, 1, 5, 2, 1)

        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.password.set_text(self.password_setting)
        self.grid.attach(self.password, 3, 5, 1, 1)

        label4 = Gtk.Label()
        label4.set_markup("    Confirm Pasword:    ")
        label4.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label4, 1, 6, 2, 1)

        self.passconf = Gtk.Entry()
        self.passconf.set_visibility(False)
        self.passconf.set_text(self.password_setting)
        self.grid.attach(self.passconf, 3, 6, 1, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.onnext2clicked)
        self.grid.attach(button1, 3, 8, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 2, 8, 1, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main_menu)
        self.grid.attach(button1, 1, 8, 1, 1)

        self.show_all()

    def onnext2clicked(self, button):
        """Password, Username, and hostname Checker"""
        self.password_setting = self.password.get_text()
        pass2 = self.passconf.get_text()
        self.username_setting = self.username.get_text()
        self.username_setting = self.username_setting.lower()
        self.compname_setting = self.compname.get_text()
        if self.password_setting != pass2:
            label5 = Gtk.Label()
            label5.set_markup("Passwords do not match")
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 2, 1)
        elif len(self.password_setting) < 4:
            label5 = Gtk.Label()
            label5.set_markup("Password is less than 4 characters")
            self.grid.remove(label5)
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 2, 1)
        elif has_special_character(self.username_setting):
            label5 = Gtk.Label()
            label5.set_markup("Username contains special characters")
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 2, 1)
        elif hasspace(self.username_setting):
            label5 = Gtk.Label()
            label5.set_markup("Username contains space")
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 2, 1)
        elif len(self.username_setting) < 1:
            label5 = Gtk.Label()
            label5.set_markup("Username empty")
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 2, 1)
        elif has_special_character(self.compname_setting):
            label5 = Gtk.Label()
            label5.set_markup("Computer Name contains non-hyphen special character")
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 2, 1)
        elif hasspace(self.compname_setting):
            label5 = Gtk.Label()
            label5.set_markup("Computer Name contains space")
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 2, 1)
        elif len(self.compname_setting) < 1:
            label5 = Gtk.Label()
            label5.set_markup("Computer Name is empty")
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 2, 1)
        else:
            global USER_COMPLETION
            USER_COMPLETION = "COMPLETED"
            self.main_menu("clicked")

        self.show_all()

    def partitioning(self, button):
        """Partitioning Main Window"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    Would you like to let %s automaticly partition a drive for installation?\t
    Or, would you like to manually partition space for it?\t

    <b>NOTE</b>
    Auto partitioning takes up an entire drive. If you are uncomfortable with this,\t
    please either manually partition your drive, or abort installation now.\t
    """ % (DISTRO))
        label.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label, 1, 1, 7, 1)

        link = Gtk.Button.new_with_label("Manual Partitioning")
        link.connect("clicked", self.opengparted)
        self.grid.attach(link, 5, 5, 1, 1)

        button1 = Gtk.Button.new_with_label("Automatic Partitioning")
        button1.connect("clicked", self.auto_partition)
        self.grid.attach(button1, 7, 5, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 3, 5, 1, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main_menu)
        self.grid.attach(button1, 1, 5, 1, 1)

        self.show_all()

    def auto_partition(self, button):
        """Auto Partitioning Settings Window"""
        self.clear_window()
        self.auto_part_setting = True

        # Get a list of disks and their capacity
        self.device = check_output(["lsblk", "-n", "-i", "-o", "NAME,SIZE,TYPE"]).decode()
        self.device = list(self.device)
        del self.device[-1]
        self.device = "".join(self.device)
        self.device = self.device.split("\n")
        dev = []
        for each2 in enumerate(self.device):
            if "loop" in self.device[each2[0]]:
                continue
            elif "part" in self.device[each2[0]]:
                continue
            else:
                dev.append(self.device[each2[0]])
        devices = []
        for each4 in dev:
            devices.append(each4.split())
        devices = [x for x in devices if x != []]
        for each4 in devices:
            if each4[0] == "sr0":
                devices.remove(each4)
        for each4 in enumerate(devices):
            devices[each4[0]].remove(devices[each4[0]][2])
        for each4 in enumerate(devices):
            devices[each4[0]][0] = "/dev/%s" % (devices[each4[0]][0])

        # Jesus Christ that's a lot of parsing and formatting.
        # At least it's done.
        # Now we have to make a GUI using them . . .

        label = Gtk.Label()
        label.set_markup("""
    Which drive would you like to install to?\t
    """)
        label.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label, 1, 1, 3, 1)

        self.disks = Gtk.ComboBoxText.new()
        for each4 in enumerate(devices):
            self.disks.append("%s" % (devices[each4[0]][0]),
                              "%s    Size: %s" % (devices[each4[0]][0],
                                                  devices[each4[0]][1]))
        if self.root_setting != "":
            self.disks.set_active_id(self.root_setting)
        self.grid.attach(self.disks, 1, 2, 2, 1)

        home_part = Gtk.CheckButton.new_with_label("Seperate home partition")
        if ((self.home_setting != "") and (self.home_setting != "NULL")):
            home_part.set_active(True)
        home_part.connect("toggled", self.auto_home_setup)
        self.grid.attach(home_part, 1, 3, 2, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.onnext6clicked)
        self.grid.attach(button1, 3, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 2, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.partitioning)
        self.grid.attach(button3, 1, 6, 1, 1)

        self.show_all()

    def auto_home_setup(self, widget):
        """Handle preexisting vs making a new home directory"""
        if widget.get_active() == 1:
            pre_exist = Gtk.CheckButton.new_with_label("Pre-existing")
            pre_exist.connect("toggled", self.auto_home_setup2)
            self.grid.attach(pre_exist, 1, 4, 2, 1)

            self.home_setting = "MAKE"
        else:
            try:
                self.grid.remove(self.grid.get_child_at(1, 4))
            except TypeError:
                pass
            self.home_setting = ""

        self.show_all()

    def auto_home_setup2(self, widget):
        """Provide options for prexisting home partitions"""
        if widget.get_active() == 1:
            dev = []
            for each5 in enumerate(self.device):
                if "loop" in self.device[each5[0]]:
                    continue
                elif "disk" in self.device[each5[0]]:
                    continue
                else:
                    dev.append(self.device[each5[0]])
            devices = []
            for each5 in dev:
                devices.append(each5.split())
            devices = [x for x in devices if x != []]
            for each5 in devices:
                if each5[0] == "sr0":
                    devices.remove(each5)
            for each5 in enumerate(devices):
                devices[each5[0]].remove(devices[each5[0]][2])
            for each5 in enumerate(devices):
                devices[each5[0]][0] = list(devices[each5[0]][0])
                del devices[each5[0]][0][0]
                del devices[each5[0]][0][0]
                devices[each5[0]][0] = "".join(devices[each5[0]][0])
            print(devices)
            for each5 in enumerate(devices):
                devices[each5[0]][0] = "/dev/%s" % ("".join(devices[each5[0]][0]))

            parts = Gtk.ComboBoxText.new()
            for each5 in enumerate(devices):
                parts.append("%s" % (devices[each5[0]][0]),
                             "%s    Size: %s" % (devices[each5[0]][0],
                                                 devices[each5[0]][1]))
            if self.home_setting != "":
                parts.set_active_id(self.home_setting)
            self.grid.attach(parts, 1, 5, 2, 1)
        else:
            self.grid.remove(parts)
            self.home_setting = "MAKE"

        self.show_all()

    def onnext6clicked(self, button):
        """Force User to either pick a drive to install to, abort,
        or backtrack
        """
        if path.isdir("/sys/firmware/efi"):
            self.efi_setting = True
        else:
            self.efi_setting = False
        self.home_setting = "NULL"
        self.swap_setting = "FILE"
        if self.disks.get_active_id() is None:
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            label = Gtk.Label()
            label.set_markup("""
    Which drive would you like to install to?\t

    <b>You must pick a drive to install to or abort installation.</b>\t
    """)
            label.set_justify(Gtk.Justification.LEFT)
            self.grid.attach(label, 1, 1, 3, 1)
            self.show_all()
        else:
            self.root_setting = self.disks.get_active_id()
            global PART_COMPLETION
            PART_COMPLETION = "COMPLETED"
            self.main_menu("clicked")



    def input_part(self, button):
        """Manual Partitioning Input Window"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>
    """)
        label.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label, 1, 1, 3, 1)

        label2 = Gtk.Label()
        label2.set_markup("/")
        label2.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label2, 1, 2, 1, 1)

        self.root = Gtk.Entry()
        self.root.set_text(self.root_setting)
        self.grid.attach(self.root, 2, 2, 1, 1)

        label3 = Gtk.Label()
        label3.set_markup("/boot/efi")
        label3.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label3, 1, 3, 1, 1)

        self.efi = Gtk.Entry()
        self.efi.set_text(self.efi_setting)
        self.grid.attach(self.efi, 2, 3, 1, 1)

        label5 = Gtk.Label()
        label5.set_markup("Must be fat32")
        label5.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label5, 3, 3, 1, 1)

        label4 = Gtk.Label()
        label4.set_markup("/home")
        label4.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label4, 1, 4, 1, 1)

        self.home = Gtk.Entry()
        self.home.set_text(self.home_setting)
        self.grid.attach(self.home, 2, 4, 1, 1)

        label6 = Gtk.Label()
        label6.set_markup("SWAP")
        label6.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label6, 1, 5, 1, 1)

        self.swap = Gtk.Entry()
        self.swap.set_text(self.swap_setting)
        self.grid.attach(self.swap, 2, 5, 1, 1)

        label7 = Gtk.Label()
        label7.set_markup("Must be linux-swap or file")
        label7.set_justify(Gtk.Justification.RIGHT)
        self.grid.attach(label7, 3, 5, 1, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.onnext4clicked)
        self.grid.attach(button1, 3, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 2, 6, 1, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.partitioning)
        self.grid.attach(button1, 1, 6, 1, 1)

        self.show_all()

    def onnext4clicked(self, button):
        """Check device paths provided for manual partitioner"""
        if ((self.root.get_text() == "") or
                (self.root.get_text()[0:5] != "/dev/")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>

    / NOT SET
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif not path.exists(self.root.get_text()):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>

    Not a Valid Device on /
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()

        elif (((self.efi.get_text() == "") or
               (self.efi.get_text()[0:5] != "/dev/")) and
              path.isdir("/sys/firmware/efi")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>

    You are using EFI, therefore an EFI partition
    must be set.
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif (not path.exists(self.efi.get_text()) or
              ((self.efi.get_text() == "") and
               not path.isdir("/sys/firmware/efi"))):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>

    Not a Valid Device on /boot/efi
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif ((self.home.get_text() != "") and
              (self.home.get_text()[0:5] != "/dev/")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>

    Please input a valid device path for HOME partition.
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif (not path.exists(self.home.get_text()) and
              (self.home.get_text() != "")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>

    Not a Valid Device on /home
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif ((self.swap.get_text() != "") and
              (self.swap.get_text()[0:5] != "/dev/") and
              (self.swap.get_text().upper() != "FILE")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>

    SWAP must be set to a valid partition path, "FILE", or
    left empty.
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif (not path.exists(self.swap.get_text()) and
              (self.swap.get_text().upper() != "FILE") and
              (self.swap.get_text() != "")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>

    Not a Valid Device on SWAP
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        else:
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partions you wish to be used?
    Leave empty the partions you don't want.
    <b> / MUST BE USED </b>
    """)
            label.set_justify(Gtk.Justification.LEFT)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)
            self.root_setting = self.root.get_text()

            self.show_all()
            if self.efi.get_text() == "":
                self.efi_setting = "NULL"
            else:
                self.efi_setting = self.efi.get_text()
            if self.home.get_text() == "":
                self.home_setting = "NULL"
            else:
                self.home_setting = self.home.get_text()
            if ((self.swap.get_text() == "") or
                    (self.swap.get_text().upper() == "FILE")):
                self.swap_setting = "FILE"
            else:
                self.swap_setting = self.swap.get_text()
            global PART_COMPLETION
            PART_COMPLETION = "COMPLETED"
            self.main_menu("clicked")



    def opengparted(self, button):
        """Open GParted"""
        Popen("gparted", stdout=DEVNULL, stderr=DEVNULL)
        self.auto_part_setting = False
        self.input_part("clicked")

    def options(self, button):
        """Extraneous options menu"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>Extra Options</b>
    The below options require a network connection, unless otherwise stated.\t
    Please ensure you are connected before selecting any of these options.
        """)
        label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(label, 1, 1, 2, 1)

        label1 = Gtk.Label()
        label1.set_markup("""
        Install third-party packages such as NVIDIA drivers if necessary\t\t
""")
        label1.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label1, 2, 2, 1, 1)

        self.extras = Gtk.CheckButton.new_with_label("Install Restricted Extras")
        if self.extras_setting == 1:
            self.extras.set_active(True)
        self.grid.attach(self.extras, 1, 3, 2, 1)

        label2 = Gtk.Label()
        label2.set_markup("""
        Update the system during installation""")
        label2.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label2, 2, 4, 1, 1)

        self.updates = Gtk.CheckButton.new_with_label("Update before reboot")
        if self.updates_setting == 1:
            self.updates.set_active(True)
        self.grid.attach(self.updates, 1, 5, 2, 1)

        label2 = Gtk.Label()
        label2.set_markup("""
        Automaticly login upon boot up. Does <b>NOT</b> require internet.""")
        label2.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label2, 2, 6, 1, 1)

        self.login = Gtk.CheckButton.new_with_label("Enable Auto-Login")
        if self.login_setting == 1:
            self.login.set_active(True)
        self.grid.attach(self.login, 1, 7, 2, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.options_next)
        self.grid.attach(button1, 2, 8, 1, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main_menu)
        self.grid.attach(button1, 1, 8, 1, 1)

        self.show_all()

    def options_next(self, button):
        """Set update and extras settings"""
        if self.extras.get_active():
            self.extras_setting = 1
        else:
            self.extras_setting = 0
        if self.updates.get_active():
            self.updates_setting = 1
        else:
            self.updates_setting = 0
        if self.login.get_active():
            self.login_setting = 1
        else:
            self.login_setting = 0
        global OPTIONS_COMPLETION
        OPTIONS_COMPLETION = "COMPLETED"
        self.main_menu("clicked")

    def locale(self, button):
        """Language and Time Zone settings menu"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
<b>Choose your Language and Time Zone</b>""")
        label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(label, 1, 1, 3, 1)

        label2 = Gtk.Label()
        label2.set_markup("""

Langauge""")
        label2.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label2, 2, 2, 1, 1)

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
        self.lang_menu.append("other", "Other, User will need to set up manually.")
        if self.lang_setting != "":
            self.lang_menu.set_active_id(self.lang_setting)
        self.grid.attach(self.lang_menu, 2, 3, 1, 1)

        label3 = Gtk.Label()
        label3.set_markup("""

Region""")
        label3.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label3, 2, 4, 1, 1)

        time_zone = self.time_zone.split("/")
        self.time_menu = Gtk.ComboBoxText.new()
        zones = ["Africa", "America", "Antarctica", "Arctic", "Asia",
                 "Atlantic", "Australia", "Brazil", "Canada", "Chile",
                 "Europe", "Indian", "Mexico", "Pacific", "US"]
        for each6 in zones:
            self.time_menu.append(each6, each6)
        # self.time_menu.append("EST", "Eastern Standard Time")
        # self.time_menu.append("CST", "Central Standard Time")
        # self.time_menu.append("MST", "Mountain Standard Time")
        # self.time_menu.append("PST", "Pacific Standard Time")
        # self.time_menu.append("AST", "Alaska Standard Time")
        # self.time_menu.append("HST", "Hawaii Standard Time")
        # self.time_menu.append("MIT", "Midway Islands Time")
        # self.time_menu.append("NST", "New Zealand Standard Time")
        # self.time_menu.append("SST", "Soloman Standard Time")
        # self.time_menu.append("AET", "Austrailia Eastern Time")
        # self.time_menu.append("ACT", "Austrailia Central Time")
        # self.time_menu.append("JST", "Japan Standard Time")
        # self.time_menu.append("CTT", "China Taiwan Time")
        # self.time_menu.append("VST", "Vietnam Standard Time")
        # self.time_menu.append("BST", "Bangladesh Standard Time")
        # self.time_menu.append("PLT", "Pakistan Lahore Time")
        # self.time_menu.append("NET", "Near East Time")
        # self.time_menu.append("EAT", "East Africa Time")
        # self.time_menu.append("ART", "(Arabic) Egypt Standard Time")
        # self.time_menu.append("EET", "Eastern European Time")
        # self.time_menu.append("ECT", "European Central Time")
        # self.time_menu.append("GMT", "Greenwich Mean Time")
        # self.time_menu.append("CAT", "Central African Time")
        # self.time_menu.append("BET", "Brazil Eastern Time")
        # self.time_menu.append("AGT", "Argentina Standard Time")
        # self.time_menu.append("PRT", "Puerto Rico and US Virgin Islands Time")
        # self.time_menu.append("IET", "Indiana Eastern Standard Time")
        if len(time_zone) > 0:
            self.time_menu.set_active_id(time_zone[0])
        self.time_menu.connect("changed", self.update_subregion)
        self.grid.attach(self.time_menu, 2, 5, 1, 1)

        label4 = Gtk.Label()
        label4.set_markup("""

Sub-Region""")
        label4.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label4, 2, 6, 1, 1)

        self.sub_region = Gtk.ComboBoxText.new()
        self.grid.attach(self.sub_region, 2, 7, 1, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.onnext3clicked)
        self.grid.attach(button1, 4, 8, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 2, 8, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.main_menu)
        self.grid.attach(button3, 1, 8, 1, 1)

        self.update_subregion(self.time_menu)

        self.show_all()

    def update_subregion(self, widget):
        """Narrow subregions to possible areas
        It makes no sense to be in New York, China, when New York is in the
        USA
        """
        if widget.get_active_id() is None:
            return
        zones = sorted(listdir("/usr/share/zoneinfo/" +
                               widget.get_active_id()))
        self.grid.remove(self.grid.get_child_at(2, 7))
        self.sub_region = Gtk.ComboBoxText.new()
        for each7 in zones:
            self.sub_region.append(each7, each7)
        time_zone = self.time_zone.split("/")
        if len(time_zone) > 1:
            self.sub_region.set_active_id(time_zone[1])
        self.grid.attach(self.sub_region, 2, 7, 1, 1)

        self.show_all()

    def onnext3clicked(self, button):
        """Set default language and time zone if user did not set them"""
        if self.lang_menu.get_active_id() is not None:
            self.lang_setting = self.lang_menu.get_active_id()
        else:
            self.lang_setting = "english"

        if ((self.time_menu.get_active_id() is not None) and
                (self.sub_region.get_active_id() is not None)):
            self.time_zone = self.time_menu.get_active_id()
            self.time_zone = self.time_zone + "/"
            self.time_zone = self.time_zone + self.sub_region.get_active_id()
        else:
            self.time_zone = "America/New_York"

        global LOCALE_COMPLETION
        LOCALE_COMPLETION = "COMPLETED"
        self.main_menu("clicked")

    def keyboard(self, button):
        """Keyboard Settings Dialog"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>Choose your Keyboard layout</b>\t
    """)
        label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(label, 1, 1, 4, 1)

        model_label = Gtk.Label()
        model_label.set_markup("""Model: """)
        model_label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(model_label, 1, 2, 1, 1)

        self.model_menu = Gtk.ComboBoxText.new()
        pwd = getcwd()
        chdir("/usr/share/console-setup")
        layouts = check_output(["./kbdnames-maker"], stderr=DEVNULL)
        chdir(pwd)
        layouts = str(layouts)
        layouts = layouts.split("\\n")
        layout_list = []
        for each8 in layouts:
            layout_list.append(each8.split("*"))
        for each8 in enumerate(layout_list):
            del layout_list[each8[0]][0]
        del layout_list[-1]
        model = []
        for each8 in enumerate(layout_list):
            if layout_list[each8[0]][0] == "model":
                model.append(layout_list[each8[0]][-1])
        model = sorted(model)
        for each8 in model:
            self.model_menu.append(each8, each8)
        if self.model_setting != "":
            self.model_menu.set_active_id(self.model_setting)
        self.grid.attach(self.model_menu, 2, 2, 3, 1)

        layout_label = Gtk.Label()
        layout_label.set_markup("""Layout: """)
        layout_label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(layout_label, 1, 3, 1, 1)

        self.layout_menu = Gtk.ComboBoxText.new()
        layouts = []
        for each8 in enumerate(layout_list):
            if layout_list[each8[0]][0] == "layout":
                layouts.append(layout_list[each8[0]][-1])
        layouts = sorted(layouts)
        for each8 in layouts:
            self.layout_menu.append(each8, each8)
        if self.layout_setting != "":
            self.layout_menu.set_active_id(self.layout_setting)
        self.layout_menu.connect("changed", self.varient_narrower)
        self.grid.attach(self.layout_menu, 2, 3, 3, 1)

        varient_label = Gtk.Label()
        varient_label.set_markup("""Varient: """)
        varient_label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(varient_label, 1, 4, 1, 1)

        self.varient_menu = Gtk.ComboBoxText.new()
        self.varients = []
        for each8 in enumerate(layout_list):
            if layout_list[each8[0]][0] == "variant":
                self.varients.append(layout_list[each8[0]][-1])
        for each8 in self.varients:
            self.varient_menu.append(each8, each8)
        if self.varient_setting != "":
            self.varient_menu.set_active_id(self.varient_setting)
        self.grid.attach(self.varient_menu, 2, 4, 3, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.onnext5clicked)
        self.grid.attach(button1, 4, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 3, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.main_menu)
        self.grid.attach(button3, 1, 6, 1, 1)

        self.show_all()

    def varient_narrower(self, widget):
        """Narrow down possible keyboard varients"""
        term = self.layout_menu.get_active_id()
        self.varient_menu.remove_all()

        varient_len = len(self.varients) - 1
        local_varients = []
        for each9 in self.varients:
            local_varients.append(each9)
        while varient_len >= 0:
            if not term in self.varients[varient_len]:
                del local_varients[varient_len]
            varient_len = varient_len - 1

        for each9 in local_varients:
            self.varient_menu.append(each9, each9)
        if self.varient_setting != "":
            self.varient_menu.set_active_id(self.varient_setting)

        self.show_all()


    def onnext5clicked(self, button):
        """Set default keyboard layout if user did not specify one"""
        if self.model_menu.get_active_id() is not None:
            self.model_setting = self.model_menu.get_active_id()
        else:
            self.model_setting = "Generic 105-key PC (intl.)"
        if self.layout_menu.get_active_id() is not None:
            self.layout_setting = self.layout_menu.get_active_id()
        else:
            self.layout_setting = "English (US)"
        if self.varient_menu.get_active_id() is not None:
            self.varient_setting = self.varient_menu.get_active_id()
        else:
            self.varient_setting = "euro"
        global KEYBOARD_COMPLETION
        KEYBOARD_COMPLETION = "COMPLETED"

        self.main_menu("clicked")

    def done(self, button):
        """Check to see if each segment has been completed
        If it hasn't, print a warning, else
        Print out the value of stuffs and exit
        """
        global KEYBOARD_COMPLETION
        global LOCALE_COMPLETION
        global OPTIONS_COMPLETION
        global PART_COMPLETION
        global USER_COMPLETION
        if ((KEYBOARD_COMPLETION != "COMPLETED") or
                (LOCALE_COMPLETION != "COMPLETED") or
                (OPTIONS_COMPLETION != "COMPLETED") or
                (PART_COMPLETION != "COMPLETED") or
                (USER_COMPLETION != "COMPLETED")):
            self.label.set_markup("""
        Feel free to complete any of the below segments in any order.\t
        However, all segments must be completed.

        <b>One or more segments have not been completed</b>
        Please complete these segments, then try again.
        Or, exit installation.\n""")
        else:
            self.complete()
        self.show_all()

    def complete(self):
        """Set settings var"""
        Gtk.main_quit("delete-event")
        self.destroy()
        # Vars to return:
            #   1  * self.auto_part_setting
            #   2  * self.password_setting
            #   3  * self.username_setting
            #   4  * self.compname_setting
            #   5  * self.root_setting
            #   6  * self.efi_setting
            #   7  * self.home_setting
            #   8  * self.swap_setting
            #   9  * self.extras_setting
            #   10  * self.updates_setting
            #   11 * self.login_setting
            #   12 * self.model_setting
            #   13 * self.layout_setting
            #   14 * self.lang_setting
            #   15 * self.time_zone
            #   16 * self.varient_setting
        if "" in (self.root_setting, self.efi_setting, self.home_setting,
                  self.swap_setting, self.auto_part_setting, self.lang_setting,
                  self.username_setting, self.compname_setting,
                  self.password_setting, self.extras_setting,
                  self.updates_setting, self.login_setting, self.model_setting,
                  self.layout_setting, self.varient_setting):
            self.data = 1
        else:
            self.data = {"AUTO_PART":bool(self.auto_part_setting),
                         "ROOT":self.root_setting, "EFI":self.efi_setting,
                         "HOME":self.home_setting, "SWAP":self.swap_setting,
                         "LANG":self.lang_setting, "TIME_ZONE":self.time_zone,
                         "USERNAME":self.username_setting,
                         "PASSWORD":self.password_setting,
                         "COMPUTER_NAME":self.compname_setting,
                         "EXTRAS":bool(self.extras_setting),
                         "UPDATES":bool(self.updates_setting),
                         "LOGIN":bool(self.login_setting),
                         "MODEL":self.model_setting,
                         "LAYOUT":self.layout_setting,
                         "VARIENT":self.varient_setting}


    def exit(self, button):
        """Exit"""
        Gtk.main_quit("delete-event")
        self.destroy()
        print(1)
        return 1

    def clear_window(self):
        """Clear Window"""
        children = self.grid.get_children()
        for each0 in children:
            self.grid.remove(each0)

    def return_data(self):
        """Return settings"""
        return self.data


def show_main():
    """Show Main UI"""
    window = Main()
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Main.exit)
    window.show_all()
    Gtk.main()
    data = window.return_data()
    window.exit("clicked")
    return data

if __name__ == '__main__':
    show_main()
