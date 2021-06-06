#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2021 Thomas Castleman <contact@draugeros.org>
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
import sys
import re
import json
import os
from subprocess import Popen, check_output, DEVNULL
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import auto_partitioner


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


def has_special_character(input_string):
    """Check for special characters"""
    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(input_string) is None:
        return False
    return True


try:
    with open("/etc/system-installer/settings.json") as config_file:
        DISTRO = json.loads(config_file.read())["distro"]

except FileNotFoundError:
    eprint("/etc/system-installer/settings.json does not exist. In testing?")
    DISTRO = "Drauger OS"


DEFAULT = """
    Welcome to the %s System Installer!

    A few things before we get started:

    <b>PARTITIONING</b>

    The %s System Installer uses Gparted to allow the user to set up their
    partitions manually. It is advised to account for this if installing next to
    another OS. If using automatic partitoning, it will take up the entirety of
    the drive told to use. Loss of data from usage of this tool is entirely at the
    fault of the user. You have been warned.

    <b>BETA WARNING</b>

    The %s System Installer is currently in beta.
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
        self.data = {"AUTO_PART": "", "HOME": "", "ROOT": "", "EFI": "",
                     "SWAP": "", "LANG": "", "TIME_ZONE": "", "USERNAME": "",
                     "PASSWORD": "", "COMPUTER_NAME": "", "EXTRAS": "",
                     "UPDATES": "", "LOGIN": "", "MODEL": "", "LAYOUT": "",
                     "VARIENT": "", "raid_array": {"raid_type": None,
                                                   "disks": {"1": None,
                                                             "2": None,
                                                             "3": None,
                                                             "4": None}}}

        self.langs = {'Afar': "aa", 'Afrikaans': "af", 'Aragonese': "an",
                      'Arabic': "ar", 'Asturian': "ast", 'Belarusian': "be",
                      'Bulgarian': "bg", 'Breton': "br", 'Bosnian': "bs",
                      'Catalan': "ca", 'Czech': "cs", 'Welsh': "cy",
                      "Danish": 'da', "German": 'de', "Greek": 'el',
                      "English": 'en', "Esperanto": 'eo', "Spanish": 'es',
                      "Estonian": 'et', "Basque": 'eu', "Finnish": 'fi',
                      "Faroese": 'fo', "French": 'fr', "Irish": 'ga',
                      "Gaelic": 'gd', "Galician": 'gl', "Manx": 'gv',
                      "Hebrew": 'he', "Croatian": 'hr', "Upper Sorbian": 'hsb',
                      "Hungarian": 'hu', "Indonesian": 'id', "Icelandic": 'is',
                      "Italian": 'it', "Japanese": 'ja', "Kashmiri": 'ka',
                      "Kazakh": 'kk', "Greenlandic": 'kl', "Korean": 'ko',
                      "Kurdish": 'ku', "Cornish": 'kw', 'Bhili': "bhb",
                      "Ganda": 'lg', "Lithuanian": 'lt', "Latvian": 'lv',
                      "Malagasy": 'mg', "Maori": 'mi', "Macedonian": 'mk',
                      "Malay": 'ms', "Maltese": 'mt', "Min Nan Chinese": 'nan',
                      "North Ndebele": 'nb', "Dutch": 'nl',
                      "Norwegian Nynorsk": 'nn', "Occitan": 'oc', "Oromo": 'om',
                      "Polish": 'pl', "Portuguese": 'pt', "Romanian": 'ro',
                      "Russian": 'ru', "Slovak": 'sk', "Slovenian": 'sl',
                      "Northern Sami": 'so', "Albanian": 'sq', "Serbian": 'sr',
                      "Sotho": 'st', "Swedish": 'sv', "Tulu": 'tcy',
                      "Tajik": 'tg', "Thai": 'th', "Tagalog": 'tl',
                      "Turkish": 'tr', "Uighur": 'ug', "Ukrainian": 'uk',
                      "Uzbek": 'uz', "Walloon": 'wa', "Xhosa": 'xh',
                      "Yiddish": 'yi', "Chinese": 'zh', "Zulu": 'zu'}
        self.raid_def = {"RAID0": {"min_drives": 2,
                                   "desc": "Max performance, Least Reliability",
                                   "raid_num": 0},
                         "RAID1": {"min_drives": 2,
                                   "desc": "Least Performance, Max Reliability",
                                   "raid_num": 1},
                         "RAID10": {"min_drives": 4,
                                    "desc": "Balanced Performance and Reliability",
                                    "raid_num": 10}}

        # Open initial window
        self.reset("clicked")

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

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
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        button4 = Gtk.Button.new_with_label("Select Config File")
        button4.connect("clicked", self.select_config)
        button4 = self._set_default_margins(button4)
        self.grid.attach(button4, 3, 2, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.reset)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 2, 2, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 1, 2, 1, 1)

        self.show_all()

    def reset(self, button):
        """Main Splash Window"""
        global DEFAULT
        self.clear_window()

        label = Gtk.Label()
        label.set_markup(DEFAULT)
        label.set_justify(Gtk.Justification.LEFT)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 4, 1)

        button1 = Gtk.Button.new_with_label("Normal Installation")
        button1.connect("clicked", self.main_menu)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 4, 2, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 1, 2, 1, 1)

        button3 = Gtk.Button.new_with_label("Quick Installation")
        button3.connect("clicked", self.quick_install_warning)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 2, 2, 1, 1)

        button4 = Gtk.Button.new_with_label("OEM Installation")
        button4.connect("clicked", self.oem_startup)
        button4 = self._set_default_margins(button4)
        self.grid.attach(button4, 3, 2, 1, 1)

        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

    def oem_startup(self, widget):
        """Start up OEM installation"""
        self.data = "/etc/system-installer/oem-install.json"
        self.complete()

    def select_config(self, widget):
        """Quick Install File Selection Window"""
        eprint("\t###\tQUICK INSTALL MODE ACTIVATED\t###\t")
        dialog = Gtk.FileChooserDialog("System Installer", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
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
        json_filter_text = Gtk.FileFilter()
        json_filter_text.set_name("JSON Files (*.json)")
        json_filter_text.add_mime_type("application/json")
        dialog.add_filter(json_filter_text)

        xz_filter_text = Gtk.FileFilter()
        xz_filter_text.set_name("XZ compressed Tar balls (*.tar.xz)")
        xz_filter_text.add_mime_type("application/x-xz-compressed-tar")
        dialog.add_filter(xz_filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def main_menu(self, button):
        """Main Menu"""
        self.clear_window()

        self.label = Gtk.Label()
        self.label.set_markup("""
        Feel free to complete any of the below segments in any order.\t
        However, all segments must be completed.\n""")
        self.label = self._set_default_margins(self.label)
        self.grid.attach(self.label, 2, 1, 2, 1)

        completion_label = Gtk.Label()
        completion_label.set_markup("""<b>COMPLETION</b>""")
        completion_label = self._set_default_margins(completion_label)
        self.grid.attach(completion_label, 2, 2, 1, 1)

        button8 = Gtk.Button.new_with_label("Keyboard")
        button8.connect("clicked", self.keyboard)
        button8 = self._set_default_margins(button8)
        self.grid.attach(button8, 3, 3, 1, 1)

        label_keyboard = Gtk.Label()
        label_keyboard.set_markup(KEYBOARD_COMPLETION)
        label_keyboard = self._set_default_margins(label_keyboard)
        self.grid.attach(label_keyboard, 2, 3, 1, 1)

        button4 = Gtk.Button.new_with_label("Locale and Time")
        button4.connect("clicked", self.locale)
        button4 = self._set_default_margins(button4)
        self.grid.attach(button4, 3, 4, 1, 1)

        label_locale = Gtk.Label()
        label_locale.set_markup(LOCALE_COMPLETION)
        label_locale = self._set_default_margins(label_locale)
        self.grid.attach(label_locale, 2, 4, 1, 1)

        button5 = Gtk.Button.new_with_label("Options")
        button5.connect("clicked", self.options)
        button5 = self._set_default_margins(button5)
        self.grid.attach(button5, 3, 5, 1, 1)

        label_options = Gtk.Label()
        label_options.set_markup(OPTIONS_COMPLETION)
        label_options = self._set_default_margins(label_options)
        self.grid.attach(label_options, 2, 5, 1, 1)

        button6 = Gtk.Button.new_with_label("Partitioning")
        button6.connect("clicked", self.partitioning)
        button6 = self._set_default_margins(button6)
        self.grid.attach(button6, 3, 6, 1, 1)

        label_part = Gtk.Label()
        label_part.set_markup(PART_COMPLETION)
        label_part = self._set_default_margins(label_part)
        self.grid.attach(label_part, 2, 6, 1, 1)

        button7 = Gtk.Button.new_with_label("User Settings")
        button7.connect("clicked", self.user)
        button7 = self._set_default_margins(button7)
        self.grid.attach(button7, 3, 7, 1, 1)

        label_user = Gtk.Label()
        label_user.set_markup(USER_COMPLETION)
        label_user = self._set_default_margins(label_user)
        self.grid.attach(label_user, 2, 7, 1, 1)

        button1 = Gtk.Button.new_with_label("DONE")
        button1.connect("clicked", self.done)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 4, 8, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
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
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        label1 = Gtk.Label()
        label1.set_markup("    Username:   ")
        label1.set_justify(Gtk.Justification.RIGHT)
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 3, 2, 1)

        self.username = Gtk.Entry()
        self.username.set_text(self.data["USERNAME"])
        self.username = self._set_default_margins(self.username)
        self.grid.attach(self.username, 3, 3, 1, 1)

        label2 = Gtk.Label()
        label2.set_markup("    Computer\'s Name:   ")
        label2.set_justify(Gtk.Justification.RIGHT)
        label2 = self._set_default_margins(label2)
        self.grid.attach(label2, 1, 4, 2, 1)

        self.compname = Gtk.Entry()
        self.compname.set_text(self.data["COMPUTER_NAME"])
        self.compname = self._set_default_margins(self.compname)
        self.grid.attach(self.compname, 3, 4, 1, 1)

        label3 = Gtk.Label()
        label3.set_markup("    Password:   ")
        label3.set_justify(Gtk.Justification.RIGHT)
        label3 = self._set_default_margins(label3)
        self.grid.attach(label3, 1, 5, 2, 1)

        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.password.set_text(self.data["PASSWORD"])
        self.password = self._set_default_margins(self.password)
        self.grid.attach(self.password, 3, 5, 1, 1)

        label4 = Gtk.Label()
        label4.set_markup("    Confirm Pasword:    ")
        label4.set_justify(Gtk.Justification.RIGHT)
        label4 = self._set_default_margins(label4)
        self.grid.attach(label4, 1, 6, 2, 1)

        self.passconf = Gtk.Entry()
        self.passconf.set_visibility(False)
        self.passconf.set_text(self.data["PASSWORD"])
        self.passconf = self._set_default_margins(self.passconf)
        self.grid.attach(self.passconf, 3, 6, 1, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.onnext2clicked)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 3, 8, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 2, 8, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 1, 8, 1, 1)

        self.show_all()

    def onnext2clicked(self, button):
        """Password, Username, and hostname Checker"""
        self.data["PASSWORD"] = self.password.get_text()
        pass2 = self.passconf.get_text()
        self.data["USERNAME"] = self.username.get_text()
        self.data["USERNAME"] = self.data["USERNAME"].lower()
        self.data["COMPUTER_NAME"] = self.compname.get_text()
        if self.data["PASSWORD"] != pass2:
            label5 = Gtk.Label()
            label5.set_markup("Passwords do not match")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif len(self.data["PASSWORD"]) < 4:
            label5 = Gtk.Label()
            label5.set_markup("Password is less than 4 characters")
            label5 = self._set_default_margins(label5)
            self.grid.remove(label5)
            label5.set_justify(Gtk.Justification.CENTER)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif has_special_character(self.data["USERNAME"]):
            label5 = Gtk.Label()
            label5.set_markup("Username contains special characters")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif " " in self.data["USERNAME"]:
            label5 = Gtk.Label()
            label5.set_markup("Username contains space")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif len(self.data["USERNAME"]) < 1:
            label5 = Gtk.Label()
            label5.set_markup("Username empty")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif has_special_character(self.data["COMPUTER_NAME"]):
            label5 = Gtk.Label()
            label5.set_markup("Computer Name contains non-hyphen special character")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif " " in self.data["COMPUTER_NAME"]:
            label5 = Gtk.Label()
            label5.set_markup("Computer Name contains space")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif len(self.data["COMPUTER_NAME"]) < 1:
            label5 = Gtk.Label()
            label5.set_markup("Computer Name is empty")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
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
    Would you like to let %s automatically partition a drive for installation?\t
    Or, would you like to manually partition space for it?\t

    <b>NOTE</b>
    Auto partitioning takes up an entire drive. If you are uncomfortable with\t
    this, please either manually partition your drive, or abort installation
    now.\t
    """ % (DISTRO))
        label.set_justify(Gtk.Justification.LEFT)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 7, 1)

        link = Gtk.Button.new_with_label("Manual Partitioning")
        link.connect("clicked", self.opengparted)
        link = self._set_default_margins(link)
        self.grid.attach(link, 5, 5, 1, 1)

        button1 = Gtk.Button.new_with_label("Automatic Partitioning")
        button1.connect("clicked", self.auto_partition)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 7, 5, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 3, 5, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 1, 5, 1, 1)

        self.show_all()

    def auto_partition(self, button):
        """Auto Partitioning Settings Window"""
        self.clear_window()
        self.data["AUTO_PART"] = True

        # Get a list of disks and their capacity
        self.devices = json.loads(check_output(["lsblk", "-n", "-i", "--json",
                                                "-o", "NAME,SIZE,TYPE"]).decode())
        self.devices = self.devices["blockdevices"]
        dev = []
        for each2 in enumerate(self.devices):
            if "loop" in self.devices[each2[0]]["name"]:
                continue
            dev.append(self.devices[each2[0]])
        devices = []
        for each4 in dev:
            devices.append(each4)
        devices = [x for x in devices if x != []]
        for each4 in devices:
            if each4["name"] == "sr0":
                devices.remove(each4)
        for each4 in enumerate(devices):
            del devices[each4[0]]["type"]
        for each4 in enumerate(devices):
            devices[each4[0]]["name"] = "/dev/%s" % (devices[each4[0]]["name"])

        # Jesus Christ that's a lot of parsing and formatting.
        # At least it's done.
        # Now we just need to remove anything that may have been used to make a
        # RAID Array

        for each in range(len(devices) - 1, -1, -1):
            for each1 in self.data["raid_array"]["disks"]:
                if devices[each]["name"] == self.data["raid_array"]["disks"][each1]:
                    del devices[each]
                    break

        # Now we have to make a GUI using them . . .

        label = Gtk.Label()
        label.set_markup("""
    Which drive would you like to install to?\t
    """)
        label.set_justify(Gtk.Justification.LEFT)
        label = self._set_default_margins(label)
        self.grid.attach(label, 2, 1, 3, 1)

        self.disks = Gtk.ComboBoxText.new()
        for each4 in enumerate(devices):
            self.disks.append("%s" % (devices[each4[0]]["name"]),
                              "%s    Size: %s" % (devices[each4[0]]["name"],
                                                  devices[each4[0]]["size"]))
        if self.data["ROOT"] != "":
            self.disks.set_active_id(self.data["ROOT"])
        self.disks = self._set_default_margins(self.disks)
        self.disks.connect("changed", self._set_root_part)
        self.grid.attach(self.disks, 2, 2, 3, 1)

        home_part = Gtk.CheckButton.new_with_label("Separate home partition")
        if ((self.data["HOME"] != "") and (self.data["HOME"] != "NULL")):
            home_part.set_active(True)
        home_part.connect("toggled", self.auto_home_setup)
        home_part = self._set_default_margins(home_part)
        self.grid.attach(home_part, 3, 3, 2, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.confirm_auto_part)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 5, 6, 1, 1)

        button5 = Gtk.Button.new_with_label("Make RAID Array")
        button5.connect("clicked", self.define_array)
        button5 = self._set_default_margins(button5)
        self.grid.attach(button5, 4, 6, 1, 1)

        button4 = Gtk.Button.new_with_label("Make Space")
        button4.connect("clicked", self.make_space)
        button4 = self._set_default_margins(button4)
        self.grid.attach(button4, 3, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 2, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.partitioning)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 1, 6, 1, 1)

        self.show_all()

    def define_array(self, widget, error=None):
        """Define btrfs RAID Array settings"""
        self.clear_window()

        dev = []
        for each2 in enumerate(self.devices):
            if "loop" in self.devices[each2[0]]["name"]:
                continue
            dev.append(self.devices[each2[0]])
        devices = []
        for each4 in dev:
            devices.append(each4)
        devices = [x for x in devices if x != []]
        for each4 in devices:
            if each4["name"] == "sr0":
                devices.remove(each4)

        for each in range(len(devices) - 1, -1, -1):
            if devices[each]["name"] == self.data["ROOT"]:
                del devices[each]

        if self.data["raid_array"]["raid_type"] is None:
            loops = 2
        else:
            loops = self.raid_def[self.data["raid_array"]["raid_type"]]["min_drives"]

        label = Gtk.Label()
        label.set_markup("""<b>Define RAID Array</b>
RAID Arrays can only be used as your home partition.""")
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        label1 = Gtk.Label()
        if error is None:
            label1.set_markup("""Please Select which RAID Type to use and which
drives to use for the RAID array.""")
        elif error == "type_not_set":
            label1.set_markup("""You must select a RAID Type to proceed.""")
        elif error == "disk_not_set":
            label1.set_markup("""You do not have enough drives set for this RAID
Type. Minimum drives is: %s""" % (loops))
        label1.set_justify(Gtk.Justification.CENTER)
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 3, 1)

        label2 = Gtk.Label()
        label2.set_markup("RAID Type: ")
        label2.set_justify(Gtk.Justification.CENTER)
        label2 = self._set_default_margins(label2)
        self.grid.attach(label2, 1, 3, 1, 1)

        raid_type = Gtk.ComboBoxText.new()
        for each in self.raid_def:
            raid_type.append(each,
                             "%s: %s" % (each, self.raid_def[each]["desc"]))
        raid_type = self._set_default_margins(raid_type)
        raid_type.set_active_id(self.data["raid_array"]["raid_type"])
        raid_type.connect("changed", self._change_raid_type)
        self.grid.attach(raid_type, 2, 3, 2, 1)

        for each in range(loops):
            label = Gtk.Label()
            label.set_markup("Drive %s" % (each + 1))
            label.set_justify(Gtk.Justification.CENTER)
            label = self._set_default_margins(label)
            self.grid.attach(label, 1, 4 + each, 1, 1)

            device_drop_down = Gtk.ComboBoxText.new()
            for each4 in devices:
                skip = False
                for each1 in self.data["raid_array"]["disks"]:
                    if each4["name"] == self.data["raid_array"]["disks"][each1]:
                        if str(each + 1) != each1:
                            skip = True
                if skip:
                    continue
                device_drop_down.append("%s" % (each4["name"]),
                                        "%s    Size: %s" % (each4["name"],
                                                            each4["size"]))

            device_drop_down.set_active_id(self.data["raid_array"]["disks"][str(each + 1)])
            if (each + 1) == 1:
                device_drop_down.connect("changed", self._assign_raid_disk_1)
            elif (each + 1) == 2:
                device_drop_down.connect("changed", self._assign_raid_disk_2)
            elif (each + 1) == 3:
                device_drop_down.connect("changed", self._assign_raid_disk_3)
            elif (each + 1) == 4:
                device_drop_down.connect("changed", self._assign_raid_disk_4)
            device_drop_down = self._set_default_margins(device_drop_down)
            self.grid.attach(device_drop_down, 2, 4 + each, 2, 1)

        button1 = Gtk.Button.new_with_label("Done")
        button1.connect("clicked", self.confirm_raid_array)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 3, 9, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 1, 9, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back to Main Menu")
        button3.connect("clicked", self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 2, 9, 1, 1)

        self.show_all()

    # I know there is a better way to assign disks than this, or at least a
    # Better way to define these functions. But this was the simplest way I can
    # Think to do it right now. In the future, I want to add the ability to
    # increase RAID Array size, but that will have to include some more dynamic
    # programming that I just don't know how to do or care to learn right now
    # considering it's 1 AM at time of writing

    def _assign_raid_disk_1(self, widget):
        """Assign RAID Disk 1"""
        self.data["raid_array"]["disks"]["1"] = widget.get_active_id()
        self.define_array("clicked")

    def _assign_raid_disk_2(self, widget):
        """Assign RAID Disk 2"""
        self.data["raid_array"]["disks"]["2"] = widget.get_active_id()
        self.define_array("clicked")

    def _assign_raid_disk_3(self, widget):
        """Assign RAID Disk 3"""
        self.data["raid_array"]["disks"]["3"] = widget.get_active_id()
        self.define_array("clicked")

    def _assign_raid_disk_4(self, widget):
        """Assign RAID Disk 4"""
        self.data["raid_array"]["disks"]["4"] = widget.get_active_id()
        self.define_array("clicked")

    def _change_raid_type(self, widget):
        """Set RAID type"""
        self.data["raid_array"]["raid_type"] = widget.get_active_id()
        if self.data["raid_array"]["raid_type"].lower() in ("raid0", "raid1"):
            self.data["raid_array"]["disks"]["3"] = None
            self.data["raid_array"]["disks"]["4"] = None
        self.define_array("clicked")

    def confirm_raid_array(self, widget):
        """Confirm RAID settings and modify other
        installer settings as necessary"""
        if self.data["raid_array"]["raid_type"] is None:
            self.define_array("clicked", error="type_not_set")
            return
        count = 0
        for each in self.data["raid_array"]["disks"]:
            if self.data["raid_array"]["disks"][each] is not None:
                count += 1
        if count < self.raid_def[self.data["raid_array"]["raid_type"]]["min_drives"]:
            self.define_array("clicked", error="disk_not_set")
            return

        self.clear_window()

        label = Gtk.Label()
        label.set_markup("<b>Are you sure you want to make this RAID Array?</b>")
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        label1 = Gtk.Label()
        label1.set_markup("<b>RAID Type:</b> %s" % (self.data["raid_array"]["raid_type"]))
        label1.set_justify(Gtk.Justification.CENTER)
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 3, 1)

        for each in self.data["raid_array"]["disks"]:
            if self.data["raid_array"]["disks"][each] is None:
                continue
            label = Gtk.Label()
            label.set_markup("""<b>Drive %s:</b> %s""" % (each,
                                                          self.data["raid_array"]["disks"][each]))
            label.set_justify(Gtk.Justification.CENTER)
            label = self._set_default_margins(label)
            self.grid.attach(label, 1, 2 + int(each), 3, 1)

        button1 = Gtk.Button.new_with_label("Confirm")
        button1.connect("clicked", self.cement_raid_array)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 3, 9, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 1, 9, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.define_array)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 2, 9, 1, 1)

        self.show_all()

    def cement_raid_array(self, widget):
        """Set alternate settings so that the RAID Array can be handled internally"""
        self.data["HOME"] = self.data["raid_array"]["disks"]["1"]
        self.auto_partition("clicked")

    def make_space(self, widget, drive=None):
        """Window for making space on an installed drive"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    Drive to Delete From\t
    """)
        label.set_justify(Gtk.Justification.LEFT)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        data = auto_partitioner.check_disk_state()
        devices = Gtk.ComboBoxText.new()
        for each in data:
            devices.append(each["name"],
                           "%s, size: %sGB" % (each["name"],
                                               int(auto_partitioner.bytes_to_gb(each["size"]))))
        devices.connect("changed", self.make_space_parts)
        devices = self._set_default_margins(devices)
        self.grid.attach(devices, 1, 2, 3, 1)

        label2 = Gtk.Label()
        label2.set_markup("""
    Partition to Delete\t
    """)
        label2.set_justify(Gtk.Justification.LEFT)
        label2 = self._set_default_margins(label2)
        self.grid.attach(label2, 1, 3, 3, 1)

        self.parts = Gtk.ComboBoxText.new()
        self.parts = self._set_default_margins(self.parts)
        self.grid.attach(self.parts, 1, 4, 3, 1)

        button1 = Gtk.Button.new_with_label("Done")
        button1.connect("clicked", self.auto_partition)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 3, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("!!! DELETE !!!")
        button3.connect("clicked", self.remove_part)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 2, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 1, 6, 1, 1)

        if drive is not None:
            devices.set_active_id(drive)
            self.make_space_parts(devices)
        self.show_all()

    def make_space_parts(self, widget):
        """Set partitions to show for make_space()"""
        self.parts.remove_all()
        data = auto_partitioner.check_disk_state()
        name = widget.get_active_id()
        for each in data:
            if each["name"] == name:
                if "children" in each:
                    for each1 in each["children"]:
                        self.parts.append(each1["name"],
                                          "%s, filesystem: %s, size: %sGB" % (each1["name"],
                                                                              each1["fstype"],
                                                                              int(auto_partitioner.bytes_to_gb(each1["size"]))))
        self.show_all()

    def remove_part(self, widget):
        """Interface for removing partitions"""
        part = self.parts.get_active_id()
        auto_partitioner.delete_part(part)
        if "nvme" in part:
            self.make_space("clicked", drive=part[:-2])
        else:
            self.make_space("clicked", drive=part[:-1])


    def auto_home_setup(self, widget):
        """Handle preexisting vs making a new home directory"""
        if widget.get_active():
            pre_exist = Gtk.CheckButton.new_with_label("Pre-existing")
            pre_exist.connect("toggled", self.auto_home_setup2)
            pre_exist = self._set_default_margins(pre_exist)
            self.grid.attach(pre_exist, 1, 4, 2, 1)

            self.data["HOME"] = "MAKE"
        else:
            try:
                self.grid.remove(self.grid.get_child_at(1, 4))
            except TypeError:
                pass
            self.data["HOME"] = ""

        self.show_all()

    def auto_home_setup2(self, widget):
        """Provide options for prexisting home partitions"""
        if widget.get_active() == 1:
            dev = []
            for each5 in enumerate(self.device):
                if ("loop" in self.device[each5[0]]) or ("disk" in self.device[each5[0]]):
                    continue
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
            for each5 in enumerate(devices):
                devices[each5[0]][0] = "/dev/%s" % ("".join(devices[each5[0]][0]))

            parts = Gtk.ComboBoxText.new()
            for each5 in enumerate(devices):
                parts.append("%s" % (devices[each5[0]][0]),
                             "%s    Size: %s" % (devices[each5[0]][0],
                                                 devices[each5[0]][1]))
            if self.data["HOME"] != "":
                parts.set_active_id(self.data["HOME"])
            parts.connect("changed", self.select_home_part)
            parts = self._set_default_margins(parts)
            self.grid.attach(parts, 1, 5, 2, 1)
        else:
            self.data["HOME"] = "MAKE"

        self.show_all()

    def select_home_part(self, widget):
        """Set pre-existing home partition, based on user input"""
        device = widget.get_active_id()
        if os.path.exists(device):
            self.data["HOME"] = device

    def _set_root_part(self, widget):
        """set root drive"""
        self.data["ROOT"] = widget.get_active_id()
        self.auto_partition("clicked")


    def confirm_auto_part(self, button):
        """Force User to either pick a drive to install to, abort,
        or backtrack
        """
        if os.path.isdir("/sys/firmware/efi"):
            self.data["EFI"] = True
        else:
            self.data["EFI"] = False
        if self.data["HOME"] == "":
            self.data["HOME"] = "NULL"
        self.data["SWAP"] = "FILE"
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
            label = self._set_default_margins(label)
            self.grid.attach(label, 1, 1, 3, 1)
            self.show_all()
        else:
            self.data["ROOT"] = self.disks.get_active_id()
            global PART_COMPLETION
            PART_COMPLETION = "COMPLETED"
            self.main_menu("clicked")


    def input_part(self, button):
        """Manual Partitioning Input Window"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>
    """)
        label.set_justify(Gtk.Justification.LEFT)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        label2 = Gtk.Label()
        label2.set_markup("/")
        label2.set_justify(Gtk.Justification.RIGHT)
        label2 = self._set_default_margins(label2)
        self.grid.attach(label2, 1, 2, 1, 1)

        self.root = Gtk.Entry()
        self.root.set_text(self.data["ROOT"])
        self.root = self._set_default_margins(self.root)
        self.grid.attach(self.root, 2, 2, 1, 1)

        label3 = Gtk.Label()
        label3.set_markup("/boot/efi")
        label3.set_justify(Gtk.Justification.RIGHT)
        label3 = self._set_default_margins(label3)
        self.grid.attach(label3, 1, 3, 1, 1)

        self.efi = Gtk.Entry()
        self.efi.set_text(self.data["EFI"])
        self.efi = self._set_default_margins(self.efi)
        self.grid.attach(self.efi, 2, 3, 1, 1)

        label5 = Gtk.Label()
        label5.set_markup("Must be fat32")
        label5.set_justify(Gtk.Justification.RIGHT)
        label5 = self._set_default_margins(label5)
        self.grid.attach(label5, 3, 3, 1, 1)

        label4 = Gtk.Label()
        label4.set_markup("/home")
        label4.set_justify(Gtk.Justification.RIGHT)
        label4 = self._set_default_margins(label4)
        self.grid.attach(label4, 1, 4, 1, 1)

        self.home = Gtk.Entry()
        self.home.set_text(self.data["HOME"])
        self.home = self._set_default_margins(self.home)
        self.grid.attach(self.home, 2, 4, 1, 1)

        label6 = Gtk.Label()
        label6.set_markup("SWAP")
        label6.set_justify(Gtk.Justification.RIGHT)
        label6 = self._set_default_margins(label6)
        self.grid.attach(label6, 1, 5, 1, 1)

        self.swap = Gtk.Entry()
        self.swap.set_text(self.data["SWAP"])
        self.swap = self._set_default_margins(self.swap)
        self.grid.attach(self.swap, 2, 5, 1, 1)

        label7 = Gtk.Label()
        label7.set_markup("Must be linux-swap or file")
        label7.set_justify(Gtk.Justification.RIGHT)
        label7 = self._set_default_margins(label7)
        self.grid.attach(label7, 3, 5, 1, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.onnext4clicked)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 3, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 2, 6, 1, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.partitioning)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 1, 6, 1, 1)

        self.show_all()

    def onnext4clicked(self, button):
        """Check device paths provided for manual partitioner"""
        if ((self.root.get_text() == "") or (
                self.root.get_text()[0:5] != "/dev/")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>

    / NOT SET
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif not os.path.exists(self.root.get_text()):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>

    Not a Valid Device on /
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()

        elif (((self.efi.get_text() == "") or (
                self.efi.get_text()[0:5] != "/dev/")) and os.path.isdir("/sys/firmware/efi")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>

    You are using EFI, therefore an EFI partition
    must be set.
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif (not os.path.exists(self.efi.get_text()) or (self.efi.get_text() == "")) and os.path.isdir("/sys/firmware/efi"):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>

    Not a Valid Device on /boot/efi
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif ((self.home.get_text() != "") and (
                self.home.get_text()[0:5] != "/dev/")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>

    Please input a valid device path for HOME partition.
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif (not os.path.exists(self.home.get_text()) and (
                self.home.get_text() != "")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>

    Not a Valid Device on /home
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif ((self.swap.get_text() != "") and (
                self.swap.get_text()[0:5] != "/dev/") and (
                    self.swap.get_text().upper() != "FILE")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>

    SWAP must be set to a valid partition path, "FILE", or
    left empty.
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif (not os.path.exists(self.swap.get_text()) and (
                self.swap.get_text().upper() != "FILE") and (
                    self.swap.get_text() != "")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>

    Not a Valid Device on SWAP
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        else:
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
    <b> / MUST BE USED </b>
    """)
            label.set_justify(Gtk.Justification.LEFT)
            label = self._set_default_margins(label)
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)
            self.data["ROOT"] = self.root.get_text()

            self.show_all()
            if self.efi.get_text() == "":
                self.data["EFI"] = "NULL"
            else:
                self.data["EFI"] = self.efi.get_text()
            if self.home.get_text() == "":
                self.data["HOME"] = "NULL"
            else:
                self.data["HOME"] = self.home.get_text()
            if ((self.swap.get_text() == "") or (
                    self.swap.get_text().upper() == "FILE")):
                self.data["SWAP"] = "FILE"
            else:
                self.data["SWAP"] = self.swap.get_text()
            global PART_COMPLETION
            PART_COMPLETION = "COMPLETED"
            self.main_menu("clicked")

    def opengparted(self, button):
        """Open GParted"""
        Popen("gparted", stdout=DEVNULL, stderr=DEVNULL)
        self.data["AUTO_PART"] = False
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
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 2, 1)

        label1 = Gtk.Label()
        label1.set_markup("""
        Install third-party packages such as NVIDIA drivers if necessary\t\t
""")
        label1.set_justify(Gtk.Justification.LEFT)
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 2, 1)

        self.extras = Gtk.CheckButton.new_with_label("Install Restricted Extras")
        if self.data["EXTRAS"] == 1:
            self.extras.set_active(True)
        self.extras = self._set_default_margins(self.extras)
        self.grid.attach(self.extras, 1, 3, 2, 1)

        label2 = Gtk.Label()
        label2.set_markup("""
        Update the system during installation""")
        label2.set_justify(Gtk.Justification.LEFT)
        label2 = self._set_default_margins(label2)
        self.grid.attach(label2, 1, 4, 2, 1)

        self.updates = Gtk.CheckButton.new_with_label("Update before reboot")
        if self.data["UPDATES"] == 1:
            self.updates.set_active(True)
        self.updates = self._set_default_margins(self.updates)
        self.grid.attach(self.updates, 1, 5, 2, 1)

        label2 = Gtk.Label()
        label2.set_markup("""
        Automatically login upon boot up. Does <b>NOT</b> require internet.""")
        label2.set_justify(Gtk.Justification.LEFT)
        label2 = self._set_default_margins(label2)
        self.grid.attach(label2, 1, 6, 2, 1)

        self.login = Gtk.CheckButton.new_with_label("Enable Auto-Login")
        if self.data["LOGIN"] == 1:
            self.login.set_active(True)
        self.login = self._set_default_margins(self.login)
        self.grid.attach(self.login, 1, 7, 2, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.options_next)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 2, 8, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.main_menu)
        buton3 = self._set_default_margins(button3)
        self.grid.attach(button3, 1, 8, 1, 1)

        self.show_all()

    def options_next(self, button):
        """Set update and extras settings"""
        if self.extras.get_active():
            self.data["EXTRAS"] = 1
        else:
            self.data["EXTRAS"] = 0
        if self.updates.get_active():
            self.data["UPDATES"] = 1
        else:
            self.data["UPDATES"] = 0
        if self.login.get_active():
            self.data["LOGIN"] = 1
        else:
            self.data["LOGIN"] = 0
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
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        label2 = Gtk.Label()
        label2.set_markup("""

Language""")
        label2.set_justify(Gtk.Justification.LEFT)
        label2 = self._set_default_margins(label2)
        self.grid.attach(label2, 2, 2, 1, 1)

        self.lang_menu = Gtk.ComboBoxText.new()
        for each in self.langs:
            self.lang_menu.append(self.langs[each], each)
        self.lang_menu.append("other", "Other, User will need to set up manually.")
        if self.data["LANG"] != "":
            self.lang_menu.set_active_id(self.data["LANG"])
        self.lang_menu = self._set_default_margins(self.lang_menu)
        self.grid.attach(self.lang_menu, 2, 3, 1, 1)

        label3 = Gtk.Label()
        label3.set_markup("""

Region""")
        label3.set_justify(Gtk.Justification.LEFT)
        label3 = self._set_default_margins(label3)
        self.grid.attach(label3, 2, 4, 1, 1)

        time_zone = self.data["TIME_ZONE"].split("/")
        self.time_menu = Gtk.ComboBoxText.new()
        zones = ["Africa", "America", "Antarctica", "Arctic", "Asia",
                 "Atlantic", "Australia", "Brazil", "Canada", "Chile",
                 "Europe", "Indian", "Mexico", "Pacific", "US"]
        for each6 in zones:
            self.time_menu.append(each6, each6)
        if len(time_zone) > 0:
            self.time_menu.set_active_id(time_zone[0])
        self.time_menu.connect("changed", self.update_subregion)
        self.time_menu = self._set_default_margins(self.time_menu)
        self.grid.attach(self.time_menu, 2, 5, 1, 1)

        label4 = Gtk.Label()
        label4.set_markup("""

Sub-Region""")
        label4.set_justify(Gtk.Justification.LEFT)
        label4 = self._set_default_margins(label4)
        self.grid.attach(label4, 2, 6, 1, 1)

        self.sub_region = Gtk.ComboBoxText.new()
        self.sub_region = self._set_default_margins(self.sub_region)
        self.grid.attach(self.sub_region, 2, 7, 1, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.on_locale_completed)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 4, 8, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 2, 8, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.main_menu)
        button3 = self._set_default_margins(button3)
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
        zones = sorted(os.listdir("/usr/share/zoneinfo/"
                               + widget.get_active_id()))
        self.grid.remove(self.grid.get_child_at(2, 7))
        self.sub_region = Gtk.ComboBoxText.new()
        for each7 in zones:
            self.sub_region.append(each7, each7)
        time_zone = self.data["TIME_ZONE"].split("/")
        if len(time_zone) > 1:
            self.sub_region.set_active_id(time_zone[1])
        self.sub_region = self._set_default_margins(self.sub_region)
        self.grid.attach(self.sub_region, 2, 7, 1, 1)

        self.show_all()

    def on_locale_completed(self, button):
        """Set default language and time zone if user did not set them"""
        if self.lang_menu.get_active_id() is not None:
            self.data["LANG"] = self.lang_menu.get_active_id()
        else:
            self.data["LANG"] = "en"

        if ((self.time_menu.get_active_id() is not None) and (
                self.sub_region.get_active_id() is not None)):
            self.data["TIME_ZONE"] = self.time_menu.get_active_id()
            self.data["TIME_ZONE"] = self.data["TIME_ZONE"] + "/"
            self.data["TIME_ZONE"] = self.data["TIME_ZONE"] + self.sub_region.get_active_id()
        else:
            self.data["TIME_ZONE"] = "America/New_York"

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
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 4, 1)

        model_label = Gtk.Label()
        model_label.set_markup("""Model: """)
        model_label.set_justify(Gtk.Justification.CENTER)
        model_label = self._set_default_margins(model_label)
        self.grid.attach(model_label, 1, 2, 1, 1)

        self.model_menu = Gtk.ComboBoxText.new()
        with open("/etc/system-installer/keyboards.json", "r") as file:
            keyboards = json.load(file)
        layout_list = keyboards["layouts"]
        model = keyboards["models"]
        for each8 in model:
            self.model_menu.append(model[each8], each8)
        if self.data["MODEL"] != "":
            self.model_menu.set_active_id(self.data["MODEL"])
        self.model_menu = self._set_default_margins(self.model_menu)
        self.grid.attach(self.model_menu, 2, 2, 3, 1)

        layout_label = Gtk.Label()
        layout_label.set_markup("""Layout: """)
        layout_label.set_justify(Gtk.Justification.CENTER)
        layout_label = self._set_default_margins(layout_label)
        self.grid.attach(layout_label, 1, 3, 1, 1)

        self.layout_menu = Gtk.ComboBoxText.new()
        for each8 in layout_list:
            self.layout_menu.append(layout_list[each8], each8)
        if self.data["LAYOUT"] != "":
            self.layout_menu.set_active_id(self.data["LAYOUT"])
        self.layout_menu.connect("changed", self.varient_narrower)
        self.layout_menu = self._set_default_margins(self.layout_menu)
        self.grid.attach(self.layout_menu, 2, 3, 3, 1)

        varient_label = Gtk.Label()
        varient_label.set_markup("""Variant: """)
        varient_label.set_justify(Gtk.Justification.CENTER)
        varient_label = self._set_default_margins(varient_label)
        self.grid.attach(varient_label, 1, 4, 1, 1)

        self.varient_menu = Gtk.ComboBoxText.new()
        self.varients = keyboards["varints"]
        for each8 in self.varients:
            for each9 in self.varients[each8]:
                self.varient_menu.append(self.varients[each8][each9], each9)
        if self.data["VARIENT"] != "":
            self.varient_menu.set_active_id(self.data["VARIENT"])
        self.varient_menu = self._set_default_margins(self.varient_menu)
        self.grid.attach(self.varient_menu, 2, 4, 3, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.on_keyboard_completed)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 4, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 3, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 1, 6, 1, 1)

        self.show_all()

    def varient_narrower(self, widget):
        """Narrow down possible keyboard varients"""
        term = self.layout_menu.get_active_id()
        self.varient_menu.remove_all()

        for each9 in self.varients[term]:
            self.varient_menu.append(self.varients[term][each9], each9)
        if self.data["VARIENT"] != "":
            self.varient_menu.set_active_id(self.data["VARIENT"])
        self.varient_menu = self._set_default_margins(self.varient_menu)

        self.show_all()


    def on_keyboard_completed(self, button):
        """Set default keyboard layout if user did not specify one"""
        if self.model_menu.get_active_id() is not None:
            self.data["MODEL"] = self.model_menu.get_active_id()
        else:
            self.data["MODEL"] = "Generic 105-key PC (intl.)"
        if self.layout_menu.get_active_id() is not None:
            self.data["LAYOUT"] = self.layout_menu.get_active_id()
        elif "kernel keymap" in self.data["MODEL"]:
            self.data["LAYOUT"] = ""
        else:
            self.data["LAYOUT"] = "English (US)"
        if self.varient_menu.get_active_id() is not None:
            self.data["VARIENT"] = self.varient_menu.get_active_id()
        elif "kernel keymap" in self.data["MODEL"]:
            self.data["VARIENT"] = ""
        else:
            self.data["VARIENT"] = "euro"
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
        if ((KEYBOARD_COMPLETION != "COMPLETED"
            ) or (LOCALE_COMPLETION != "COMPLETED"
                 ) or (OPTIONS_COMPLETION != "COMPLETED"
                      ) or (PART_COMPLETION != "COMPLETED"
                           ) or (USER_COMPLETION != "COMPLETED")):
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
        if isinstance(self.data, str):
            if os.path.isfile(self.data):
                return
            else:
                self.data = 1
        elif isinstance(self.data, dict):
            if "" in self.data.values():
                self.data = 1
            else:
                self.data["EXTRAS"] = bool(self.data["EXTRAS"])
                self.data["UPDATES"] = bool(self.data["UPDATES"])
                self.data["LOGIN"] = bool(self.data["LOGIN"])
        else:
            self.data = 1

    def exit(self, button):
        """Exit dialog"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""\n<b>Are you sure you want to exit?</b>

Exiting now will cause all your settings to be lost.""")
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 2, 1)

        yes = Gtk.Button.new_with_label("Exit")
        yes.connect("clicked", self._exit)
        yes = self._set_default_margins(yes)
        self.grid.attach(yes, 1, 2, 1, 1)

        no = Gtk.Button.new_with_label("Return")
        no.connect("clicked", self.main_menu)
        no = self._set_default_margins(no)
        self.grid.attach(no, 2, 2, 1, 1)

        self.show_all()

    def _exit(self, button):
        """Exit"""
        Gtk.main_quit("delete-event")
        self.destroy()
        self.data = 1
        return 1

    def clear_window(self):
        """Clear Window"""
        children = self.grid.get_children()
        for each0 in children:
            self.grid.remove(each0)

    def return_data(self):
        """Return settings"""
        return self.data


def show_main(boot_time=False):
    """Show Main UI"""
    make_kbd_names()
    window = Main()
    if not boot_time:
        window.set_decorated(True)
    window.set_resizable(False)
    window.connect("delete-event", Main._exit)
    window.show_all()
    Gtk.main()
    data = window.return_data()
    window.exit("clicked")
    window.destroy()
    return data


def make_kbd_names():
    """Get Keyboard Names faster"""
    if os.path.isfile("/etc/system-installer/keyboards.json"):
        # Keyboards file already made. Nothing to do.
        return
    with open("/usr/share/console-setup/KeyboardNames.pl") as file:
        data = file.read()
    data = data.split("\n")
    for each in range(len(data) - 1, -1, -1):
        data[each] = data[each].replace(" =>", ":")
        data[each] = data[each].replace(");", "},")
        data[each] = data[each].replace("'", '"')
        data[each] = data[each].replace("\\", "")
        if "%variants" in data[each]:
            data[each] = '"varints": {'
        elif "%layouts" in data[each]:
            data[each] = '"layouts": {'
        elif "%models" in data[each]:
            data[each] = '"models": {'
        elif (("package" in data[each]) or ("1;" in data[each])):
            del data[each]
        elif "#!/" in data[each]:
            data[each] = "{"
        elif "(" in data[each]:
            if data[each][-1] == "(":
                data[each] = data[each].replace("(", "{")
        if "}" in data[each]:
            data[each - 1] = data[each - 1][:-1]
    while True:
        if data[-1] == "":
            del data[-1]
        else:
            data[-1] = "}}"
            break
    data = "\n".join(data)
    os.chdir("/etc/system-installer")
    with open("keyboards.json", "w+") as file:
        file.write(data)


if __name__ == '__main__':
    show_main()
