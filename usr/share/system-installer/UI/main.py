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
from os import getcwd, chdir, path, listdir, fork
import sys
import re
import json
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
    with open("/etc/system-installer/default.json") as config_file:
        DISTRO = json.loads(config_file.read())["distro"]

except FileNotFoundError:
    eprint("/etc/system-installer/default.json does not exist. In testing?")
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
        self.variant_setting = ""
        self.data = {}

        self.langs = {'Afar': "aa", 'Afrikaans': "af", 'Aragonese': "an",
                      'Arabic': "ar", 'Asturian': "ast", 'Belarusian': "be",
                      'Bulgarian': "bg", 'Breton': "br", 'Bosnian': "bs",
                      'Catalan': "ca", 'Czech': "cs", 'Welsh': "cy",
                      "Danish": 'da',
                      "German": 'de', "Greek": 'el', "English": 'en',
                      "Esperanto": 'eo',
                      "Spanish": 'es', "Estonian": 'et', "Basque": 'eu',
                      "Finnish": 'fi', "Faroese": 'fo', "French": 'fr',
                      "Irish": 'ga',
                      "Gaelic": 'gd', "Galician": 'gl', "Manx": 'gv',
                      "Hebrew": 'he',
                      "Croatian": 'hr', "Upper Sorbian": 'hsb',
                      "Hungarian": 'hu',
                      "Indonesian": 'id', "Icelandic": 'is', "Italian": 'it',
                      "Japanese": 'ja', "Kashmiri": 'ka', "Kazakh": 'kk',
                      "Greenlandic": 'kl', "Korean": 'ko', "Kurdish": 'ku',
                      "Cornish": 'kw', 'Bhili': "bhb",
                      "Ganda": 'lg', "Lithuanian": 'lt', "Latvian": 'lv',
                      "Malagasy": 'mg', "Maori": 'mi', "Macedonian": 'mk',
                      "Malay": 'ms', "Maltese": 'mt', "Min Nan Chinese": 'nan',
                      "North Ndebele": 'nb', "Dutch": 'nl',
                      "Norwegian Nynorsk": 'nn',
                      "Occitan": 'oc', "Oromo": 'om', "Polish": 'pl',
                      "Portuguese": 'pt', "Romanian": 'ro', "Russian": 'ru',
                      "Slovak": 'sk', "Slovenian": 'sl', "Northern Sami": 'so',
                      "Albanian": 'sq', "Serbian": 'sr', "Sotho": 'st',
                      "Swedish": 'sv',
                      "Tulu": 'tcy', "Tajik": 'tg', "Thai": 'th',
                      "Tagalog": 'tl',
                      "Turkish": 'tr', "Uighur": 'ug', "Ukrainian": 'uk',
                      "Uzbek": 'uz',
                      "Walloon": 'wa', "Xhosa": 'xh', "Yiddish": 'yi',
                      "Chinese": 'zh', "Zulu": 'zu'}

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
        self.grid.attach(self.label, 2, 1, 2, 1)

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
        """Password, Username, and Hostname Checker"""
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
        elif " " in self.username_setting:
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
        elif " " in self.compname_setting:
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
    Would you like to let %s automatically partition a drive for installation?\t
    Or, would you like to manually partition space for it?\t

    <b>NOTE</b>
    Auto partitioning takes up an entire drive. If you are uncomfortable with\t
    this, please either manually partition your drive, or abort installation
    now.\t
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
        self.device = check_output(["lsblk", "-n", "-i", "-o",
                                    "NAME,SIZE,TYPE"]).decode()
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
        self.grid.attach(self.disks, 1, 2, 3, 1)

        home_part = Gtk.CheckButton.new_with_label("Separate home partition")
        if ((self.home_setting != "") and (self.home_setting != "NULL")):
            home_part.set_active(True)
        home_part.connect("toggled", self.auto_home_setup)
        self.grid.attach(home_part, 1, 3, 2, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.onnext6clicked)
        self.grid.attach(button1, 4, 6, 1, 1)

        button4 = Gtk.Button.new_with_label("Make Space")
        button4.connect("clicked", self.make_space)
        self.grid.attach(button4, 3, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 2, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.partitioning)
        self.grid.attach(button3, 1, 6, 1, 1)

        self.show_all()

    def make_space(self, widget, drive=None):
        """Window for making space on an installed drive"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    Drive to Delete From\t
    """)
        label.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label, 1, 1, 3, 1)

        data = auto_partitioner.check_disk_state()
        devices = Gtk.ComboBoxText.new()
        for each in data:
            devices.append(each["name"],
                           "%s, size: %sGB" % (each["name"],
                                               int(auto_partitioner.bytes_to_gb(each["size"]))))
        devices.connect("changed", self.make_space_parts)
        self.grid.attach(devices, 1, 2, 3, 1)

        label2 = Gtk.Label()
        label2.set_markup("""
    Partition to Delete\t
    """)
        label2.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label2, 1, 3, 3, 1)

        self.parts = Gtk.ComboBoxText.new()
        self.grid.attach(self.parts, 1, 4, 3, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.auto_partition)
        self.grid.attach(button1, 3, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("!!! DELETE !!!")
        button3.connect("clicked", self.remove_part)
        self.grid.attach(button3, 2, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
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
        """Handle pre-existing vs making a new home directory"""
        if widget.get_active():
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
        """Provide options for pre-existing home partitions"""
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
            parts.connect("changed", self.select_home_part)
            self.grid.attach(parts, 1, 5, 2, 1)
        else:
            self.home_setting = "MAKE"

        self.show_all()

    def select_home_part(self, widget):
        """Set pre-existing home partition, based on user input"""
        device = widget.get_active_id()
        if path.exists(device):
            self.home_setting = device


    def onnext6clicked(self, button):
        """Force User to either pick a drive to install to, abort,
        or backtrack
        """
        if path.isdir("/sys/firmware/efi"):
            self.efi_setting = True
        else:
            self.efi_setting = False
        if self.home_setting == "":
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
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
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
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif not path.exists(self.root.get_text()):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
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

        elif (((self.efi.get_text() == "") or (
                self.efi.get_text()[0:5] != "/dev/")) and path.isdir("/sys/firmware/efi")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
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
        elif (not path.exists(self.efi.get_text()) or (self.efi.get_text() == "")) and path.isdir("/sys/firmware/efi"):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
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
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif (not path.exists(self.home.get_text()) and (
                self.home.get_text() != "")):
            label = Gtk.Label()
            label.set_markup("""
    What are the mount points for the partitions you wish to be used?
    Leave empty the partitions you don't want.
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
            try:
                self.grid.remove(self.grid.get_child_at(1, 1))
            except TypeError:
                pass
            self.grid.attach(label, 1, 1, 3, 1)

            self.show_all()
        elif (not path.exists(self.swap.get_text()) and (
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
            if ((self.swap.get_text() == "") or (
                    self.swap.get_text().upper() == "FILE")):
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
        Automatically login upon boot up. Does <b>NOT</b> require internet.""")
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

Language""")
        label2.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(label2, 2, 2, 1, 1)

        self.lang_menu = Gtk.ComboBoxText.new()
        for each in self.langs:
            self.lang_menu.append(self.langs[each], each)
        # self.lang_menu.append("english", "English")
        # self.lang_menu.append("chinese", "Chinese")
        # self.lang_menu.append("japanese", "Japanese")
        # self.lang_menu.append("spanish", "Spanish")
        # self.lang_menu.append("hindi", "Hindi")
        # self.lang_menu.append("german", "German")
        # self.lang_menu.append("french", "French")
        # self.lang_menu.append("italian", "Italian")
        # self.lang_menu.append("korean", "Korean")
        # self.lang_menu.append("russian", "Russian")
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
        button1.connect("clicked", self.on_locale_completed)
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
        zones = sorted(listdir("/usr/share/zoneinfo/"
                               + widget.get_active_id()))
        self.grid.remove(self.grid.get_child_at(2, 7))
        self.sub_region = Gtk.ComboBoxText.new()
        for each7 in zones:
            self.sub_region.append(each7, each7)
        time_zone = self.time_zone.split("/")
        if len(time_zone) > 1:
            self.sub_region.set_active_id(time_zone[1])
        self.grid.attach(self.sub_region, 2, 7, 1, 1)

        self.show_all()

    def on_locale_completed(self, button):
        """Set default language and time zone if user did not set them"""
        if self.lang_menu.get_active_id() is not None:
            self.lang_setting = self.lang_menu.get_active_id()
        else:
            self.lang_setting = "en"

        if ((self.time_menu.get_active_id() is not None) and (
                self.sub_region.get_active_id() is not None)):
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
        with open("/etc/system-installer/keyboards", "r") as file:
            layouts = file.read()
        layouts = layouts.split("\n")
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
        self.layout_menu.connect("changed", self.variant_narrower)
        self.grid.attach(self.layout_menu, 2, 3, 3, 1)

        variant_label = Gtk.Label()
        variant_label.set_markup("""Variant: """)
        variant_label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(variant_label, 1, 4, 1, 1)

        self.variant_menu = Gtk.ComboBoxText.new()
        self.variants = []
        for each8 in enumerate(layout_list):
            if layout_list[each8[0]][0] == "variant":
                self.variants.append(layout_list[each8[0]][-1])
        for each8 in self.variants:
            self.variant_menu.append(each8, each8)
        if self.variant_setting != "":
            self.variant_menu.set_active_id(self.variant_setting)
        self.grid.attach(self.variant_menu, 2, 4, 3, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.on_keyboard_completed)
        self.grid.attach(button1, 4, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        self.grid.attach(button2, 3, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.main_menu)
        self.grid.attach(button3, 1, 6, 1, 1)

        self.show_all()

    def variant_narrower(self, widget):
        """Narrow down possible keyboard variants"""
        term = self.layout_menu.get_active_id()
        self.variant_menu.remove_all()

        variant_len = len(self.variants) - 1
        local_variants = []
        for each9 in self.variants:
            local_variants.append(each9)
        while variant_len >= 0:
            if not term in self.variants[variant_len]:
                del local_variants[variant_len]
            variant_len = variant_len - 1

        for each9 in local_variants:
            self.variant_menu.append(each9, each9)
        if self.variant_setting != "":
            self.variant_menu.set_active_id(self.variant_setting)

        self.show_all()


    def on_keyboard_completed(self, button):
        """Set default keyboard layout if user did not specify one"""
        if self.model_menu.get_active_id() is not None:
            self.model_setting = self.model_menu.get_active_id()
        else:
            self.model_setting = "Generic 105-key PC (intl.)"
        if self.layout_menu.get_active_id() is not None:
            self.layout_setting = self.layout_menu.get_active_id()
        elif "kernel keymap" in self.model_setting:
            self.layout_setting = ""
        else:
            self.layout_setting = "English (US)"
        if self.variant_menu.get_active_id() is not None:
            self.variant_setting = self.variant_menu.get_active_id()
        elif "kernel keymap" in self.model_setting:
            self.variant_setting = ""
        else:
            self.variant_setting = "euro"
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
        Feel free to complete the segments below in any order.\t
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
        if "" in (self.root_setting, self.efi_setting, self.home_setting,
                  self.swap_setting, self.auto_part_setting, self.lang_setting,
                  self.username_setting, self.compname_setting,
                  self.password_setting, self.extras_setting,
                  self.updates_setting, self.login_setting, self.model_setting,
                  self.layout_setting, self.variant_setting):
            self.data = 1
        else:
            self.data = {"AUTO_PART": bool(self.auto_part_setting),
                         "ROOT": self.root_setting, "EFI": self.efi_setting,
                         "HOME": self.home_setting, "SWAP": self.swap_setting,
                         "LANG": self.lang_setting, "TIME_ZONE": self.time_zone,
                         "USERNAME": self.username_setting,
                         "PASSWORD": self.password_setting,
                         "COMPUTER_NAME": self.compname_setting,
                         "EXTRAS": bool(self.extras_setting),
                         "UPDATES": bool(self.updates_setting),
                         "LOGIN": bool(self.login_setting),
                         "MODEL": self.model_setting,
                         "LAYOUT": self.layout_setting,
                         "VARIANT": self.variant_setting}

    def exit(self, button):
        """Exit"""
        Gtk.main_quit("delete-event")
        self.destroy()
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
    if fork() == 0:
        make_kbd_names()
        return
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

def make_kbd_names():
    """Get Keyboard Names faster"""
    if path.isfile("/etc/system-installer/keyboards"):
        # Keyboards file already made. Nothing to do.
        return
    chdir("/usr/share/console-setup")
    layouts = check_output(["./kbdnames-maker"], stderr=DEVNULL).decode()
    chdir("/etc/system-installer")
    with open("keyboards", "w+") as file:
        file.write(layouts)


if __name__ == '__main__':
    show_main()
