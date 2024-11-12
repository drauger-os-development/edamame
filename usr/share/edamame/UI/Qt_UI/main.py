#!shebang
# -*- coding: utf-8 -*-
#
#  main.py
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
"""Main Installation UI"""
from __future__ import print_function
import re
import sys
import json
import os
import subprocess
import traceback
import random
from qtpy import QtGui, QtWidgets, QtCore
import common
import auto_partitioner as ap
try:
    import UI.Qt_UI.qt_common as QCommon
except ImportError:
    import qt_common as QCommon


def has_special_character(input_string):
    """Check for special characters"""
    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(input_string) is None:
        return False
    return True


with open("../../../../../etc/edamame/settings.json") as config_file:
    SETTINGS = json.loads(config_file.read())


DEFAULT = f"""
# Welcome to the {SETTINGS["distro"]} System Installer!\n
\n\n
A few things before we get started:\n
\n\n
**PARTITIONING**\n
\n\n
The {SETTINGS["distro"]} System Installer uses Gparted to allow the user to set up their\n
partitions manually. It is advised to account for this if installing next to\n
another OS. If using automatic partitoning, it will take up the entirety of\n
the drive told to use. Loss of data from usage of this tool is entirely at the\n
fault of the user. You have been warned.\n
\n"""

KEYBOARD_COMPLETION = "TO DO"
USER_COMPLETION = "TO DO"
PART_COMPLETION = "TO DO"
LOCALE_COMPLETION = "TO DO"
OPTIONS_COMPLETION = "TO DO"


class Main(QtWidgets.QWidget):
    """Main UI Window"""
    def __init__(self, screen_size):
        """Initialize the Window"""
        super().__init__()
        self.setWindowTitle("Edamame")
        self.setWindowIcon(QtGui.QIcon.fromTheme("system-installer"))
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.screen_size = (screen_size.width(), screen_size.height())

        # Initialize setting values
        self.data = {"AUTO_PART": "", "HOME": "", "ROOT": "", "EFI": "",
                     "SWAP": "", "LANG": "", "TIME_ZONE": "", "USERNAME": "",
                     "PASSWORD": "", "COMPUTER_NAME": "", "EXTRAS": "",
                     "UPDATES": "", "LOGIN": "", "MODEL": "", "LAYOUT": "",
                     "VARIENT": "", "raid_array": {"raid_type": None,
                                                   "disks": {"1": None,
                                                             "2": None,
                                                             "3": None,
                                                             "4": None}},
                     "COMPAT_MODE": ""}

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
        try:
            margin = QtCore.QMargins(10, 10, 10, 10)
            widget.setContentsMargins(margin)
        except AttributeError:
            common.eprint("WARNING: QtCore.QMargins() does not exist. Spacing in UI might be a bit wonky.")
        return widget

    def quick_install_warning(self, button):
        """Quick Install Mode Entry Point"""
        self.clear_window()

        label = QtWidgets.QLabel("""\n
# QUICK INSTALL MODE INITIATED\n
\n
You have activated Quick Install mode.\n
\n
This mode allows users to provide the system installation utility with\n
a config file containing their prefrences for installation and set up.\n
\n
An example of one of these can be found at /etc/edamame/quick-install-template.json\n
\n""")
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        button4 = QtWidgets.QPushButton("Select Config File")
        button4.clicked.connect(self.select_config)
        button4 = self._set_default_margins(button4)
        self.grid.addWidget(button4, 2, 3, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.reset)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 2, 2, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 2, 1, 1, 1)

    def reset(self, button):
        """Main Splash Window"""
        global DEFAULT
        self.clear_window()

        label = QtWidgets.QLabel(DEFAULT)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label.setAlignment(QtCore.Qt.AlignLeft)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 4)

        button1 = QtWidgets.QPushButton("Normal Installation")
        button1.clicked.connect(self.main_menu)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 2, 4, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 2, 1, 1, 1)

        button3 = QtWidgets.QPushButton("Quick Installation")
        button3.clicked.connect(self.quick_install_warning)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 2, 2, 1, 1)

        button4 = QtWidgets.QPushButton("OEM Installation")
        button4.clicked.connect(self.oem_startup)
        button4 = self._set_default_margins(button4)
        self.grid.addWidget(button4, 2, 3, 1, 1)

    def oem_startup(self, widget):
        """Start up OEM installation"""
        self.clear_window()

        # show a confirmation window

        label = QtWidgets.QLabel("""
## Are you sure you want to do an OEM installation?\n
\n
OEM installation should **ONLY** be used by OEMs, or those installing\n
Drauger OS for other people, ahead of time. It has several limitations\n
over a normal or quick installation:\n
\n
* Takes up the entire drive it is installed to\n
* Locale, keyboard, and password must be set AFTER installation\n
* Hostname and username can not be set by the user\n
* Restricted Extras AND Updates are automatically installed\n
* A Swap file will automatically be generated to enable Hybrid Sleep\n
\n""")
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        button1 = QtWidgets.QPushButton("Proceed -->")
        button1.clicked.connect(self.oem_run)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 2, 3, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 2, 2, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.reset)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 2, 1, 1, 1)

    def oem_run(self, widget):
        """Start up OEM installation"""
        self.data = "/etc/edamame/oem-install.json"
        self.complete()

    def select_config(self, widget):
        """Quick Install File Selection Window"""
        common.eprint("\t###\tQUICK INSTALL MODE ACTIVATED\t###\t")
        dialog = QtWidgets.QFileDialog(self)

        dialog.setMimeTypeFilters(["application/json", "application/x-xz-compressed-tar"])

        dialog.exec()
        response = dialog.selectedFiles()[0]
        if response != "":
            self.data = response
            self.complete()
        else:
            self.data = 1
            self.exit("clicked")

    def main_menu(self, button):
        """Main Menu"""
        self.clear_window()

        self.label = QtWidgets.QLabel("""
### Feel free to complete any of the below segments in any order.\n
### However, all segments must be completed.\n""")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextFormat(QtCore.Qt.MarkdownText)
        self.label = self._set_default_margins(self.label)
        self.grid.addWidget(self.label, 1, 2, 1, 2)

        completion_label = QtWidgets.QLabel("""**COMPLETION**""")
        completion_label.setAlignment(QtCore.Qt.AlignCenter)
        completion_label.setTextFormat(QtCore.Qt.MarkdownText)
        completion_label = self._set_default_margins(completion_label)
        self.grid.addWidget(completion_label, 2, 2, 1, 1)

        button8 = QtWidgets.QPushButton("Keyboard")
        button8.clicked.connect(self.keyboard)
        button8 = self._set_default_margins(button8)
        self.grid.addWidget(button8, 3, 3, 1, 1)

        label_keyboard = QtWidgets.QLabel(KEYBOARD_COMPLETION)
        label_keyboard.setAlignment(QtCore.Qt.AlignCenter)
        label_keyboard.setTextFormat(QtCore.Qt.MarkdownText)
        label_keyboard = self._set_default_margins(label_keyboard)
        self.grid.addWidget(label_keyboard, 3, 2, 1, 1)

        button4 = QtWidgets.QPushButton("Locale and Time")
        button4.clicked.connect(self.locale)
        button4 = self._set_default_margins(button4)
        self.grid.addWidget(button4, 4, 3, 1, 1)

        label_locale = QtWidgets.QLabel(LOCALE_COMPLETION)
        label_locale.setAlignment(QtCore.Qt.AlignCenter)
        label_locale.setTextFormat(QtCore.Qt.MarkdownText)
        label_locale = self._set_default_margins(label_locale)
        self.grid.addWidget(label_locale, 4, 2, 1, 1)

        button5 = QtWidgets.QPushButton("Options")
        button5.clicked.connect(self.options)
        button5 = self._set_default_margins(button5)
        self.grid.addWidget(button5, 5, 3, 1, 1)

        label_options = QtWidgets.QLabel(OPTIONS_COMPLETION)
        label_options.setAlignment(QtCore.Qt.AlignCenter)
        label_options.setTextFormat(QtCore.Qt.MarkdownText)
        label_options = self._set_default_margins(label_options)
        self.grid.addWidget(label_options, 5, 2, 1, 1)

        button6 = QtWidgets.QPushButton("Partitioning")
        button6.clicked.connect(self.partitioning)
        button6 = self._set_default_margins(button6)
        self.grid.addWidget(button6, 6, 3, 1, 1)

        label_part = QtWidgets.QLabel(PART_COMPLETION)
        label_part.setAlignment(QtCore.Qt.AlignCenter)
        label_part.setTextFormat(QtCore.Qt.MarkdownText)
        label_part = self._set_default_margins(label_part)
        self.grid.addWidget(label_part, 6, 2, 1, 1)

        button7 = QtWidgets.QPushButton("User Settings")
        button7.clicked.connect(self.user)
        button7 = self._set_default_margins(button7)
        self.grid.addWidget(button7, 7, 3, 1, 1)

        label_user = QtWidgets.QLabel(USER_COMPLETION)
        label_user.setAlignment(QtCore.Qt.AlignCenter)
        label_user.setTextFormat(QtCore.Qt.MarkdownText)
        label_user = self._set_default_margins(label_user)
        self.grid.addWidget(label_user, 7, 2, 1, 1)

        button1 = QtWidgets.QPushButton("DONE")
        button1.clicked.connect(self.done)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 8, 4, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 8, 1, 1, 1)

    def user(self, button):
        """User setup Window"""
        self.clear_window()

        label = QtWidgets.QLabel("""# Set Up Main User""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        label1 = QtWidgets.QLabel("    Username:   ")
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 3, 1, 1, 2)

        self.username = QtWidgets.QLineEdit()
        self.username.setText(self.data["USERNAME"])
        self.username = self._set_default_margins(self.username)
        self.grid.addWidget(self.username, 3, 3, 1, 1)

        label2 = QtWidgets.QLabel("    Computer\'s Name:   ")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setTextFormat(QtCore.Qt.MarkdownText)
        label2 = self._set_default_margins(label2)
        self.grid.addWidget(label2, 4, 1, 1, 2)

        self.compname = QtWidgets.QLineEdit()
        self.compname.setText(self.data["COMPUTER_NAME"])
        self.compname = self._set_default_margins(self.compname)
        self.grid.addWidget(self.compname, 4, 3, 1, 1)

        auto_gen_hostname = QtWidgets.QPushButton("Auto-Generate Computer Name")
        auto_gen_hostname.clicked.connect(self.generate_hostname)
        auto_gen_hostname = self._set_default_margins(auto_gen_hostname)
        self.grid.addWidget(auto_gen_hostname, 4, 4, 1, 1)

        label3 = QtWidgets.QLabel("    Password:   ")
        label3.setAlignment(QtCore.Qt.AlignCenter)
        label3.setTextFormat(QtCore.Qt.MarkdownText)
        label3 = self._set_default_margins(label3)
        self.grid.addWidget(label3, 5, 1, 1, 2)

        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setText(self.data["PASSWORD"])
        self.password = self._set_default_margins(self.password)
        self.grid.addWidget(self.password, 5, 3, 1, 1)

        label4 = QtWidgets.QLabel("    Confirm Pasword:    ")
        label4.setAlignment(QtCore.Qt.AlignCenter)
        label4.setTextFormat(QtCore.Qt.MarkdownText)
        label4 = self._set_default_margins(label4)
        self.grid.addWidget(label4, 6, 1, 1, 2)

        self.passconf = QtWidgets.QLineEdit()
        self.passconf.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passconf.setText(self.data["PASSWORD"])
        self.passconf = self._set_default_margins(self.passconf)
        self.grid.addWidget(self.passconf, 6, 3, 1, 1)

        button1 = QtWidgets.QPushButton("Okay -->")
        button1.clicked.connect(self.onnext2clicked)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 8, 4, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 8, 2, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 8, 1, 1, 1)

    def generate_hostname(self, widget):
        """Generate a hostname that follows these rules:
        - 16 characters long
        - Starts with "DRAUGER-", no quotation marks
        - The remaining characters should be a randomly generated string of uppercase letters and numbers
        - Avoid Letters:
          - O, I
        - Avoid numnbers:
          - 0, 1
        - Have no special characters"""
        remaining_len = SETTINGS["hostname_append_len"]
        allowed_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        allowed_numbers = [2, 3, 4, 5, 6, 7, 8, 9]
        suffix = []
        while remaining_len > 0:
            if (random.randint(0, 10) % 2) == 0:
                # letter
                suffix.append(random.sample(allowed_letters, 1)[0])
            else:
                # number
                suffix.append(str(random.sample(allowed_numbers, 1)[0]))
            remaining_len -= 1
        suffix = "".join(suffix)
        output = f"{SETTINGS['hostname_prepend']}-{suffix}"

        self.data["COMPUTER_NAME"] = output
        self.compname.setText(output)

    def onnext2clicked(self, button):
        """Password, Username, and hostname Checker"""
        self.data["PASSWORD"] = self.password.text()
        pass2 = self.passconf.text()
        self.data["USERNAME"] = self.username.text()
        self.data["USERNAME"] = self.data["USERNAME"].lower()
        self.data["COMPUTER_NAME"] = self.compname.text()
        if self.data["PASSWORD"] != pass2:
            label5 = QtWidgets.QLabel("Passwords do not match")
            label5.setAlignment(QtCore.Qt.AlignCenter)
            label5.setTextFormat(QtCore.Qt.MarkdownText)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.itemAtPosition(7, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label5, 7, 1, 1, 3)
        elif len(self.data["PASSWORD"]) < SETTINGS["min_password_length"]:
            label5 = QtWidgets.QLabel("Password is less than 4 characters")
            label5.setAlignment(QtCore.Qt.AlignCenter)
            label5.setTextFormat(QtCore.Qt.MarkdownText)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.itemAtPosition(7, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label5, 7, 1, 1, 3)
        elif has_special_character(self.data["USERNAME"]):
            label5 = QtWidgets.QLabel("Username contains special characters")
            label5.setAlignment(QtCore.Qt.AlignCenter)
            label5.setTextFormat(QtCore.Qt.MarkdownText)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.itemAtPosition(7, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label5, 7, 1, 1, 3)
        elif " " in self.data["USERNAME"]:
            label5 = QtWidgets.QLabel("Username contains space")
            label5.setAlignment(QtCore.Qt.AlignCenter)
            label5.setTextFormat(QtCore.Qt.MarkdownText)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.itemAtPosition(7, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label5, 7, 1, 1, 3)
        elif len(self.data["USERNAME"]) < 1:
            label5 = QtWidgets.QLabel("Username empty")
            label5.setAlignment(QtCore.Qt.AlignCenter)
            label5.setTextFormat(QtCore.Qt.MarkdownText)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.itemAtPosition(7, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label5, 7, 1, 1, 3)
        elif has_special_character(self.data["COMPUTER_NAME"]):
            label5 = QtWidgets.QLabel("Computer Name contains non-hyphen special character")
            label5.setAlignment(QtCore.Qt.AlignCenter)
            label5.setTextFormat(QtCore.Qt.MarkdownText)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.itemAtPosition(7, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label5, 7, 1, 1, 3)
        elif " " in self.data["COMPUTER_NAME"]:
            label5 = QtWidgets.QLabel("Computer Name contains space")
            label5.setAlignment(QtCore.Qt.AlignCenter)
            label5.setTextFormat(QtCore.Qt.MarkdownText)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.itemAtPosition(7, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label5, 7, 1, 1, 3)
        elif len(self.data["COMPUTER_NAME"]) < 1:
            label5 = QtWidgets.QLabel("Computer Name is empty")
            label5.setAlignment(QtCore.Qt.AlignCenter)
            label5.setTextFormat(QtCore.Qt.MarkdownText)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.itemAtPosition(7, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label5, 7, 1, 1, 3)
        else:
            global USER_COMPLETION
            USER_COMPLETION = "COMPLETED"
            self.main_menu("clicked")

    def partitioning(self, button):
        """Partitioning Main Window"""
        self.clear_window()

        label = QtWidgets.QLabel(f"""
Would you like to let {SETTINGS["distro"]} automatically partition a drive for installation?\n
Or, would you like to manually partition space for it?\n
\n
**NOTE**\n
Auto partitioning takes up an entire drive. If you are uncomfortable with\n
this, please either manually partition your drive, or abort installation\n
now.\n
\n""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 7)

        link = QtWidgets.QPushButton("Manual Partitioning")
        link.clicked.connect(self.opengparted)
        link = self._set_default_margins(link)
        self.grid.addWidget(link, 5, 5, 1, 1)

        button1 = QtWidgets.QPushButton("Automatic Partitioning")
        button1.clicked.connect(self.auto_partition)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 5, 7, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 5, 3, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 5, 1, 1, 1)

    def auto_partition(self, button):
        """Auto Partitioning Settings Window"""
        self.clear_window()
        self.data["AUTO_PART"] = True

        # Get a list of disks and their capacity
        self.devices = json.loads(subprocess.check_output(["lsblk", "-n", "-i", "--json",
                                                           "-o", "NAME,SIZE,TYPE,FSTYPE"]).decode())
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
            if "sr" in each4["name"]:
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

        label = QtWidgets.QLabel("""Which drive would you like to install to?""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 2, 1, 3)

        self.disks = QtWidgets.QComboBox()
        for each4 in enumerate(devices):
            self.disks.addItem(f"{devices[each4[0]]["name"]}    Size: {devices[each4[0]]["size"]}", (devices[each4[0]]["name"]))
        if self.data["ROOT"] != "":
            self.disks.setCurrentText(self.data["ROOT"])
        self.disks = self._set_default_margins(self.disks)
        self.disks.currentTextChanged.connect(self._set_root_part)
        self.grid.addWidget(self.disks, 2, 2, 1, 3)

        home_part = QtWidgets.QCheckBox("Separate home partition")
        if ((self.data["HOME"] != "") and (self.data["HOME"] != "NULL")):
            home_part.setChecked(True)
        home_part.toggled.connect(self.auto_home_setup)
        home_part = self._set_default_margins(home_part)
        self.grid.addWidget(home_part, 3, 3, 1, 2)

        button1 = QtWidgets.QPushButton("Okay -->")
        button1.clicked.connect(self.confirm_auto_part)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 5, 1, 1)

        button5 = QtWidgets.QPushButton("Make RAID Array")
        button5.clicked.connect(self.define_array)
        button5 = self._set_default_margins(button5)
        self.grid.addWidget(button5, 6, 4, 1, 1)

        button4 = QtWidgets.QPushButton("Make Space")
        button4.clicked.connect(self.make_space)
        button4 = self._set_default_margins(button4)
        self.grid.addWidget(button4, 6, 3, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 2, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.partitioning)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 6, 1, 1, 1)

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

        label = QtWidgets.QLabel("""**Define RAID Array**
RAID Arrays can only be used as your home partition.""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        label1 = QtWidgets.QLabel()
        if error is None:
            label1.setText("""Please Select which RAID Type to use and which
drives to use for the RAID array.""")
        elif error == "type_not_set":
            label1.setText("""You must select a RAID Type to proceed.""")
        elif error == "disk_not_set":
            label1.setText("""You do not have enough drives set for this RAID
Type. Minimum drives is: %s""" % (loops))
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 3)

        label2 = QtWidgets.QLabel("RAID Type: ")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setTextFormat(QtCore.Qt.MarkdownText)
        label2 = self._set_default_margins(label2)
        self.grid.addWidget(label2, 3, 1, 1, 1)

        raid_type = QtWidgets.QComboBox()
        for each in self.raid_def:
            raid_type.addItem(f"{each}: {self.raid_def[each]["desc"]}", each)
        raid_type = self._set_default_margins(raid_type)
        raid_type.setItemText(self.data["raid_array"]["raid_type"])
        raid_type.currentTextChanged.connect(self._change_raid_type)
        self.grid.addWidget(raid_type, 3, 2, 1, 2)

        for each in range(loops):
            label = QtWidgets.QLabel(f"Drive {each + 1}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setTextFormat(QtCore.Qt.MarkdownText)
            label = self._set_default_margins(label)
            self.grid.addWidget(label, 4 + each, 1, 1, 1)

            device_drop_down = QtWidgets.QComboBox()
            for each4 in devices:
                skip = False
                for each1 in self.data["raid_array"]["disks"]:
                    if each4["name"] == self.data["raid_array"]["disks"][each1]:
                        if str(each + 1) != each1:
                            skip = True
                if skip:
                    continue
                device_drop_down.addItem(f"{each4["name"]}    Size: {each4["size"]}", each4["name"])

            device_drop_down.setCurrentIndex(self.data["raid_array"]["disks"][str(each + 1)])
            if (each + 1) == 1:
                device_drop_down.currentTextChanged.connect(self._assign_raid_disk_1)
            elif (each + 1) == 2:
                device_drop_down.currentTextChanged.connect(self._assign_raid_disk_2)
            elif (each + 1) == 3:
                device_drop_down.currentTextChanged.connect(self._assign_raid_disk_3)
            elif (each + 1) == 4:
                device_drop_down.currentTextChanged.connect(self._assign_raid_disk_4)
            device_drop_down = self._set_default_margins(device_drop_down)
            self.grid.addWidget(device_drop_down, 4 + each, 2, 1, 2)

        button1 = QtWidgets.QPushButton("Done")
        button1.clicked.connect(self.confirm_raid_array)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 9, 3, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 9, 1, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back to Main Menu")
        button3.clicked.connect(self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 9, 2, 1, 1)

    # I know there is a better way to assign disks than this, or at least a
    # Better way to define these functions. But this was the simplest way I can
    # Think to do it right now. In the future, I want to add the ability to
    # increase RAID Array size, but that will have to include some more dynamic
    # programming that I just don't know how to do or care to learn right now
    # considering it's 1 AM at time of writing

    def _assign_raid_disk_1(self, widget):
        """Assign RAID Disk 1"""
        self.data["raid_array"]["disks"]["1"] = widget
        self.define_array("clicked")

    def _assign_raid_disk_2(self, widget):
        """Assign RAID Disk 2"""
        self.data["raid_array"]["disks"]["2"] = widget
        self.define_array("clicked")

    def _assign_raid_disk_3(self, widget):
        """Assign RAID Disk 3"""
        self.data["raid_array"]["disks"]["3"] = widget
        self.define_array("clicked")

    def _assign_raid_disk_4(self, widget):
        """Assign RAID Disk 4"""
        self.data["raid_array"]["disks"]["4"] = widget
        self.define_array("clicked")

    def _change_raid_type(self, widget):
        """Set RAID type"""
        self.data["raid_array"]["raid_type"] = widget
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

        label = QtWidgets.QLabel("**Are you sure you want to make this RAID Array?**")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        label1 = QtWidgets.QLabel(f"**RAID Type:** {self.data["raid_array"]["raid_type"]}")
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 3)

        for each in self.data["raid_array"]["disks"]:
            if self.data["raid_array"]["disks"][each] is None:
                continue
            label = QtWidgets.QLabel(f"""**Drive {each}:** {self.data["raid_array"]["disks"][each]}""")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setTextFormat(QtCore.Qt.MarkdownText)
            label = self._set_default_margins(label)
            self.grid.addWidget(label, 2 + int(each), 1, 1, 3)

        button1 = QtWidgets.QPushButton("Confirm")
        button1.clicked.connect(self.cement_raid_array)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 9, 3, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 9, 1, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.define_array)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 9, 2, 1, 1)

    def cement_raid_array(self, widget):
        """Set alternate settings so that the RAID Array can be handled internally"""
        self.data["HOME"] = self.data["raid_array"]["disks"]["1"]
        self.auto_partition("clicked")

    def make_space(self, widget, drive=None):
        """Window for making space on an installed drive"""
        self.clear_window()

        label = QtWidgets.QLabel("""Drive to Delete From""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        data = ap.check_disk_state()
        devices = QtWidgets.QComboBox()
        for each in data:
            devices.addItem(f"{each['name']}, size: {int(ap.bytes_to_gb(each['size']))}GB", each["name"])
        devices.currentTextChanged.connect(self.make_space_parts)
        devices = self._set_default_margins(devices)
        self.grid.addWidget(devices, 2, 1, 1, 3)

        label2 = QtWidgets.QLabel("""Partition to Delete""")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setTextFormat(QtCore.Qt.MarkdownText)
        label2 = self._set_default_margins(label2)
        self.grid.addWidget(label2, 3, 1, 1, 3)

        self.parts = QtWidgets.QComboBox()
        self.parts = self._set_default_margins(self.parts)
        self.grid.addWidget(self.parts, 4, 1, 1, 3)

        button1 = QtWidgets.QPushButton("Done")
        button1.clicked.connect(self.auto_partition)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 3, 1, 1)

        button3 = QtWidgets.QPushButton("!!! DELETE !!!")
        button3.clicked.connect(self.confirm_remove_part)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 6, 2, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 1, 1, 1)

        if drive is not None:
            devices.setCurrentText(drive)
            self.make_space_parts(devices)

    def make_space_parts(self, widget):
        """Set partitions to show for make_space()"""
        self.parts.remove_all()
        data = ap.check_disk_state()
        name = widget.currentText()
        for each in data:
            if each["name"] == name:
                if "children" in each:
                    for each1 in each["children"]:
                        self.parts.addItem(f"{each1['name']}, filesystem: {each1['fstype']}, size: {int(ap.bytes_to_gb(each1['size']))}GB",
                                           each1["name"])

    def confirm_remove_part(self, widget):
        """Confirm removal of designated partition"""
        self.clear_window()

        label = QtWidgets.QLabel("""**Are you sure you want to delete this partition?**""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        label1 = QtWidgets.QLabel(self.parts.currentText())
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 1)

        button1 = QtWidgets.QPushButton("NO")
        button1.clicked.connect(self.make_space)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 3, 1, 1)

        button3 = QtWidgets.QPushButton("YES")
        button3.clicked.connect(self.remove_part)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 6, 2, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 1, 1, 1)

    def remove_part(self, widget):
        """Interface for removing partitions"""
        part = self.parts.currentText()
        ap.delete_part(part)
        if "nvme" in part:
            self.make_space("clicked", drive=part[:-2])
        else:
            self.make_space("clicked", drive=part[:-1])

    def auto_home_setup(self, widget):
        """Handle preexisting vs making a new home directory"""
        if widget:
            pre_exist = QtWidgets.QCheckBox("Pre-existing")
            pre_exist.toggled.connect(self.auto_home_setup2)
            pre_exist = self._set_default_margins(pre_exist)
            self.grid.addWidget(pre_exist, 4, 1, 1, 2)

            self.data["HOME"] = "MAKE"
        else:
            try:
                self.grid.itemAtPosition(4, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.data["HOME"] = ""

    def auto_home_setup2(self, widget):
        """Provide options for prexisting home partitions"""
        if widget:
            dev_list = tuple(self.devices)
            new_dev_list = []  # this will be the final list that is displayed for the user

            # todo: account for BTRFS drives that have no partitions
            for device in dev_list:  # we will iterate through the dev list and add devices to the new list
                try:
                    if device == []:  # if the device is empty, we skip
                        continue
                    elif 'children' in device:
                        for child in device['children']:
                            if "type" not in child.keys():  # if it doesn't have a label, skip
                                continue
                            elif not child['type'] == 'part':  # if it isn't labeled partition, skip
                                continue

                            test_child = {'name': child['name'], 'size': child['size']}

                            if test_child not in new_dev_list:  # make sure child object is not already in dev_list
                                new_dev_list.append(test_child)
                    elif device["fstype"] is not None:
                        # if the drive has no partition table, just a file system,
                        # add it
                        if device["fstype"] != "squashfs":
                            # don't add it, beacuse it's a squashfs file system
                            new_device = {"name": device["name"], "size": device["size"]}
                            new_dev_list.append(new_device)
                    elif "type" not in device.keys():  # if it doesn't have a label, skip
                        continue
                    elif device['type'] != 'part':
                        # if it isn't labeled partition, skip
                        continue
                    else:
                        new_device = {'name': device['name'], 'size': device['size']}

                        new_dev_list.append(new_device)
                except KeyError:
                    common.eprint(traceback.format_exc())
                    print(json.dumps(device, indent=2))

            # TEMPORARY: Remove the ability to use a home partition on the same
            # drive as where the root partition is
            for each in range(len(new_dev_list) - 1, -1, -1):
                if self.data["ROOT"][5:] in new_dev_list[each]["name"]:
                    del new_dev_list[each]

            home_cmbbox = QtWidgets.QComboBox()

            # properly format device names and add to combo box
            for device in new_dev_list:
                if device["name"][:5] != "/dev/":
                    device['name'] = f"/dev/{device['name']}"

                home_cmbbox.addItem(f"{device['name']}    Size: {device['size']}", device['name'])

            if self.data["HOME"] != "":
                home_cmbbox.setCurrentText(self.data["HOME"])
            home_cmbbox.currentTextChanged.connect(self.select_home_part)
            parts = self._set_default_margins(home_cmbbox)
            self.grid.addWidget(home_cmbbox, 5, 1, 1, 2)
        else:
            self.data["HOME"] = "MAKE"

    def select_home_part(self, widget):
        """Set pre-existing home partition, based on user input"""
        if os.path.exists(widget):
            self.data["HOME"] = widget

    def _set_root_part(self, widget):
        """set root drive"""
        self.data["ROOT"] = widget
        # self.auto_partition("clicked")

    def confirm_auto_part(self, button):
        """Force User to either pick a drive to install to, abort,
        or backtrack
        """
        if ap.is_EFI():
            self.data["EFI"] = True
        else:
            self.data["EFI"] = False
        if self.data["HOME"] == "":
            self.data["HOME"] = "NULL"
        self.data["SWAP"] = "FILE"
        if self.disks.currentText() is None:
            try:
                self.grid.itemAtPosition(1, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            label = QtWidgets.QLabel("""
Which drive would you like to install to?\n
\n
**You must pick a drive to install to or abort installation.**\n
\n""")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setTextFormat(QtCore.Qt.MarkdownText)
            label = self._set_default_margins(label)
            self.grid.addWidget(label, 1, 1, 1, 3)

        else:
            self.data["ROOT"] = self.disks.currentText()
            global PART_COMPLETION
            PART_COMPLETION = "COMPLETED"
            self.main_menu("clicked")

    def set_up_partitioner_label(self, additional_message=""):
        """prepare top label for display on manual partitioner

        Keyword arguments:
        additonal message -- any errors that need to be displayed below original message

        Return value:
        label -- the top label ready for additional formatting and display
        """
        label = QtWidgets.QLabel()

        input_string = """
What are the mount points for the partitions you wish to be used?\n
Leave empty the partitions you don't want.\n
**ROOT PARTITION MUST BE USED**\n"""

        if additional_message != "":
            input_string = input_string + "\n" + additional_message

        label.setText(input_string)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)

        return label

    def input_part(self, button):
        """Manual Partitioning Input Window"""
        self.clear_window()

        label = self.set_up_partitioner_label()
        self.grid.addWidget(label, 1, 1, 1, 3)

        label2 = QtWidgets.QLabel("ROOT Partition (Mounted at /)")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setTextFormat(QtCore.Qt.MarkdownText)
        label2 = self._set_default_margins(label2)
        self.grid.addWidget(label2, 2, 1, 1, 2)

        self.root = QtWidgets.QComboBox()
        self.root = self._set_default_margins(self.root)
        self.root.currentTextChanged.connect(self.update_possible_root_parts)
        self.grid.addWidget(self.root, 2, 3, 1, 1)

        self.root_parts = QtWidgets.QComboBox()
        self.root_parts = self._set_default_margins(self.root_parts)
        self.root_parts.currentTextChanged.connect(self.update_possible_home_parts)
        self.grid.addWidget(self.root_parts, 3, 3, 1, 1)

        root_info = QtWidgets.QPushButton("Info on Root Partition")
        root_info.clicked.connect(self.explain_root)
        root_info = self._set_default_margins(root_info)
        self.grid.addWidget(root_info, 2, 4, 1, 1)

        if ap.is_EFI():
            label3 = QtWidgets.QLabel("EFI Partition (Mounted at /boot/efi)")
            label3.setAlignment(QtCore.Qt.AlignCenter)
            label3.setTextFormat(QtCore.Qt.MarkdownText)
            label3 = self._set_default_margins(label3)
            self.grid.addWidget(label3, 4, 1, 1, 2)

            self.efi = QtWidgets.QComboBox()
            self.efi = self._set_default_margins(self.efi)
            self.efi.currentTextChanged.connect(self.update_possible_efi_parts)
            self.grid.addWidget(self.efi, 4, 3, 1, 1)

            self.efi_parts = QtWidgets.QComboBox()
            self.efi_parts = self._set_default_margins(self.efi_parts)
            self.grid.addWidget(self.efi_parts, 5, 3, 1, 1)

            efi_info = QtWidgets.QPushButton("Info on EFI Partition")
            efi_info.clicked.connect(self.explain_efi)
            efi_info = self._set_default_margins(efi_info)
            self.grid.addWidget(efi_info, 4, 4, 1, 1)

        label4 = QtWidgets.QLabel("Home Partition (Mounted at /home) (optional)")
        label4.setAlignment(QtCore.Qt.AlignCenter)
        label4.setTextFormat(QtCore.Qt.MarkdownText)
        label4 = self._set_default_margins(label4)
        self.grid.addWidget(label4, 6, 1, 1, 2)

        self.home = QtWidgets.QComboBox()
        self.home = self._set_default_margins(self.home)
        self.home.currentTextChanged.connect(self.update_possible_home_parts)
        self.grid.addWidget(self.home, 6, 3, 1, 1)

        self.home_parts = QtWidgets.QComboBox()
        self.home_parts = self._set_default_margins(self.home_parts)
        self.home_parts.currentTextChanged.connect(self.update_possible_root_parts)
        self.grid.addWidget(self.home_parts, 7, 3, 1, 1)

        home_info = QtWidgets.QPushButton("Info on Home Partition")
        home_info.clicked.connect(self.explain_home)
        home_info = self._set_default_margins(home_info)
        self.grid.addWidget(home_info, 6, 4, 1, 1)

        label6 = QtWidgets.QLabel("SWAP")
        label6.setAlignment(QtCore.Qt.AlignCenter)
        label6.setTextFormat(QtCore.Qt.MarkdownText)
        label6 = self._set_default_margins(label6)
        self.grid.addWidget(label6, 8, 1, 1, 2)

        self.swap =QtWidgets.QComboBox()
        self.swap = self._set_default_margins(self.swap)
        self.swap.currentTextChanged.connect(self.update_possible_swap_parts)
        self.grid.addWidget(self.swap, 8, 3, 1, 1)

        self.swap_parts = QtWidgets.QComboBox()
        self.swap_parts = self._set_default_margins(self.swap_parts)
        self.grid.addWidget(self.swap_parts, 9, 3, 1, 1)

        swap_info = QtWidgets.QPushButton("Info on SWAP")
        swap_info.clicked.connect(self.explain_swap)
        swap_info = self._set_default_margins(swap_info)
        self.grid.addWidget(swap_info, 8, 4, 1, 1)

        self.scan_for_usable_drives("clicked")

        button1 = QtWidgets.QPushButton("Okay -->")
        button1.clicked.connect(self.check_man_part_settings)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 10, 4, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 10, 3, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.partitioning)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 10, 1, 1, 1)

        button4 = QtWidgets.QPushButton("Refresh Drives")
        if ap.is_EFI():
            button4.clicked.connect(self.scan_for_usable_drives)
        else:
            button4.clicked.connect(self.scan_for_usable_drives)
        button4 = self._set_default_margins(button4)
        self.grid.addWidget(button4, 10, 2, 1, 1)

    def update_possible_root_parts(self, root_drive_dropdown):
        """Update possible root partitions based on given drive"""
        if self.root.currentText() in ("", None):
            print("No drive selected for root. No action necessary")
            return
        flag = False
        drives = ap.check_disk_state()
        parts = []
        for each in drives:
            if each["name"] == root_drive_dropdown:
                if "children" in each:
                    parts = each["children"]
        if parts == []:
            return
        setting = root_drive_dropdown
        self.root_parts.setCurrentText(None)
        for each in range(self.root_parts.count() - 1, -1, -1):
            self.root_parts.removeItem(each)
        for each in parts:
            if each["fstype"] in ("ext4", "ext3", "btrfs", "xfs", "f2fs"):
                if each["size"] >= ap.LIMITER:
                    if each["name"] != self.home_parts.currentText():
                        self.root_parts.addItem(each["name"], each["name"])
                    if each["name"] == setting:
                        flag = True
        self.root_parts.addItem("Root Partition", "Root Partition")

        if flag:
            self.root_parts.setCurrentText(setting)
        elif self.data["ROOT"] not in ("", None, "NULL"):
            self.root_parts.setCurrentText(self.data["ROOT"])
        else:
            self.root_parts.setCurrentText("Root Partition")

    def update_possible_home_parts(self, home_drive_dropdown):
        """Update possible root partitions based on given drive"""
        if self.home.currentText() in ("", None):
            print("No drive selected for home. No action necessary")
            return
        flag = False
        drives = ap.check_disk_state()
        parts = []
        for each in drives:
            if each["name"] == home_drive_dropdown:
                if "children" in each:
                    for each1 in each["children"]:
                        parts.append(each1)
        setting = home_drive_dropdown
        self.home_parts.setCurrentText(None)
        for each in range(self.home_parts.count() - 1, -1, -1):
            self.home_parts.removeItem(each)
        for each in parts:
            if each["fstype"] in ("ext4", "ext3", "btrfs", "xfs", "f2fs",
                                  "jfs", "ext2"):
                if each["size"] >= ap.gb_to_bytes(8):
                    if each["name"] != self.root_parts.currentText():
                        self.home_parts.addItem(each["name"], each["name"])
                    if each["name"] == setting:
                        flag = True
        self.home_parts.addItem("Home Partition", "Home Partition")

        if flag:
            self.home_parts.setCurrentText(setting)
        elif self.data["HOME"] not in ("", None, "NULL"):
            self.home_parts.setCurrentText(self.data["HOME"])
        else:
            self.home_parts.setCurrentText("Home Partition")

    def update_possible_swap_parts(self, swap_drive_dropdown):
        """Update possible root partitions based on given drive"""
        if self.swap.currentText() in ("", None):
            print("No drive selected for swap. No action necessary")
            return
        flag = False
        drives = ap.check_disk_state()
        parts = []
        for each in drives:
            if each["name"] == swap_drive_dropdown:
                if "children" in each:
                    parts = each["children"]
        setting = swap_drive_dropdown
        self.swap_parts.setCurrentText(None)
        for each in range(self.swap_parts.count() - 1, -1, -1):
            self.swap_parts.removeItem(each)
        for each in parts:
            if each["fstype"] in ("linux-swap", "swap"):
                self.swap_parts.addItem(each["name"], each["name"])
            if each["name"] == setting:
                flag = True
        self.swap_parts.addItem("Swap Partition", "Swap Partition")

        if flag:
            self.swap_parts.setCurrentText(setting)
        elif self.data["SWAP"] not in ("", None, "NULL"):
            self.swap_parts.setCurrentText(self.data["SWAP"])
        else:
            self.swap_parts.setCurrentText("Swap Partition")

    def update_possible_efi_parts(self, efi_drive_dropdown):
        """Update possible root partitions based on given drive"""
        if self.efi.currentText() in ("", None):
            print("No drive selected for EFI. No action necessary")
            return
        flag = False
        drives = ap.check_disk_state()
        parts = []
        for each in drives:
            if each["name"] == efi_drive_dropdown:
                if "children" in each:
                    parts = each["children"]
        if parts == []:
            return
        setting = efi_drive_dropdown
        self.efi_parts.setCurrentText(None)
        for each in range(self.efi_parts.count() - 1, -1, -1):
            self.efi_parts.removeItem(each)
        for each in parts:
            if each["fstype"] in ("exfat", "vfat", "fat32", "fat16", "fat12"):
                if each["size"] >= ap.mb_to_bytes(125):
                    self.efi_parts.addItem(each["name"], each["name"])
                if each["name"] == setting:
                    flag = True
        self.efi_parts.addItem("EFI Partition", "EFI Partition")

        if flag:
            self.efi_parts.setCurrentText(setting)
        elif self.data["EFI"] not in ("", None, "NULL"):
            self.efi_parts.setCurrentText(self.data["EFI"])
        else:
            self.efi_parts.setCurrentText("EFI Partition")

    def scan_for_usable_drives(self, widget):
        """Add available drives to drive dropdowns"""
        root_dropdown = self.root
        home_dropdown = self.home
        swap_dropdown = self.swap
        if hasattr(self, "efi"):
            efi_dropdown = self.efi
        else:
            efi_dropdown = None
        # get drive names
        drives_dict = ap.check_disk_state()
        drives = []
        for each in drives_dict:
            if each["type"] == "disk":
                drives.append(each["name"])

        # get previous settings
        root_selected = root_dropdown.currentText()
        home_selected = home_dropdown.currentText()
        swap_selected = swap_dropdown.currentText()
        try:
            if efi_dropdown is not None:
                efi_selected = efi_dropdown.currentText()
        except AttributeError:
            efi_selected = None

        # confirm previous settings
        if root_selected in ("", None):
            root_selected = ap.part_to_drive(self.data["ROOT"])
        if home_selected in ("", None):
            home_selected = ap.part_to_drive(self.data["HOME"])
        if swap_selected in ("", None):
            swap_selected = ap.part_to_drive(self.data["SWAP"])
        try:
            if efi_dropdown is not None:
                if efi_selected in ("", None):
                    efi_selected = ap.part_to_drive(self.data["EFI"])
        except AttributeError:
            pass

        # wipe current dropdowns
        for each in range(self.root.count() - 1, -1, -1):
            self.root.removeItem(each)
        for each in range(self.home.count() - 1, -1, -1):
            self.home.removeItem(each)
        for each in range(self.swap.count() - 1, -1, -1):
            self.swap.removeItem(each)
        try:
            if efi_dropdown is not None:
                for each in range(self.efi.count() - 1, -1, -1):
                    self.efi.removeItem(each)
        except AttributeError:
            pass

        # repopulate
        for each in drives:
            root_dropdown.addItem(each, each)
            home_dropdown.addItem(each, each)
            swap_dropdown.addItem(each, each)
            try:
                if efi_dropdown is not None:
                    efi_dropdown.addItem(each, each)
            except AttributeError:
                pass

        # custom attributes
        home_dropdown.addItem("(none)", "(none)")
        home_dropdown.addItem("Drive with Home Partition", "Drive with Home Partition")
        swap_dropdown.addItem("FILE", "FILE")
        swap_dropdown.addItem("Drive with Swap Partition", "Drive with Swap Partition")
        root_dropdown.addItem("Drive with Root Partition", "Drive with Root Partition")
        try:
            if efi_dropdown is not None:
                efi_dropdown.addItem("Drive with EFI Partition", "Drive with EFI Partition")
        except (AttributeError, NameError):
            pass

        # re-apply settings
        drives = set(drives)
        if root_selected in drives:
            root_dropdown.setCurrentText(root_selected)
        else:
            root_dropdown.setCurrentText("Drive with Root Partition")
        if home_selected in drives:
            home_dropdown.setCurrentText(home_selected)
        else:
            home_dropdown.setCurrentText("Drive with Home Partition")
        if swap_selected in drives:
            swap_dropdown.setCurrentText(swap_selected)
        else:
            swap_dropdown.setCurrentText("Drive with Swap Partition")
        try:
            if efi_dropdown is not None:
                if efi_selected in drives:
                    efi_dropdown.setCurrentText(efi_selected)
                else:
                    efi_dropdown.setCurrentText("Drive with EFI Partition")
        except AttributeError:
            pass

    def explain_root(self, button):
        """Explain Root Partition requierments and limitations"""
        self.clear_window()

        label = QtWidgets.QLabel("**Info on Root Partition**")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label = QtWidgets.QLabel("What is an Root Partition?")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 2, 1, 1, 1)

        label = QtWidgets.QLabel("""
The Root Partition is the partition where your operating system is\n
going to be installed, as well as the vast majority of apps you install\n
throughout the lifetime of the OS.\n""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 3, 1, 1, 1)

        label = QtWidgets.QLabel("Root Partition Requirements")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 2, 2, 1, 1)

        label = QtWidgets.QLabel("""
Root Partitions are expected to be no smaller than 32 GB, and can be any\n
file system type except FAT32, FAT16, NTFS, or exFAT/vFAT.\n
\n
We suggest having a Root Partition of at least 64 GB, with a btrfs\n
file system. This will provide you with the ability to back up your OS in\n
case of a potentially risky upgrade or configuration change, while also\n
providing great file system performance.\n""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 3, 2, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 2, 1, 1)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.input_part)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 1, 1, 1)

    def explain_efi(self, button):
        """Explain efi Partition requierments and limitations"""
        self.clear_window()

        label = QtWidgets.QLabel("**Info on EFI Partition**")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label = QtWidgets.QLabel("What is an EFI Partition?")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 2, 1, 1, 1)

        label = QtWidgets.QLabel("""
An EFI or UEFI Partition is a small partition which\n
contains the bootloader and related files for a system\n
using UEFI firmware.\n
\n
Since you booted your system in UEFI mode, you are\n
required to have one of these partitions.\n""")
        label4.setAlignment(QtCore.Qt.AlignCenter)
        label4.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 3, 1, 1, 1)

        label = QtWidgets.QLabel("EFI Partition Requirements")
        label4.setAlignment(QtCore.Qt.AlignCenter)
        label4.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 2, 2, 1, 1)

        label = QtWidgets.QLabel("""
EFI Partitions are expected to be no smaller than 200 MB,\n
(although we suggest about 1 GB) and use a FAT32 or FAT16\n
file system. We suggest using a FAT32 file system as it\n
is the most widely supported.\n
\n
This partition must also have the \"boot\" and \"esp\" flags set.\n""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 3, 2, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 2, 1, 1)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.input_part)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 1, 1, 1)

    def explain_home(self, button):
        """Explain home Partition requierments and limitations"""
        self.clear_window()

        label = QtWidgets.QLabel("**Info on Home Partition**")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label = QtWidgets.QLabel("What is a Home Partition?")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 2, 1, 1, 1)

        label = QtWidgets.QLabel("""
A Home Partition is a partition which contains all or\n
most of your user info. Having one of these is completely\n
optional. If you do opt for one, it can help keep your data\n
safe from data loss, or if the partition is on another drive,\n
it can ensure quick access times to data in your home\n
directory.\n""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 3, 1, 1, 1)

        label = QtWidgets.QLabel("Home Partition Requirements")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 2, 2, 1, 1)

        label = QtWidgets.QLabel("""
Home Partitions are expected to be no smaller than 500 MB,\n
and can be any file system except FAT32, FAT16, exFAT/vFAT, or NTFS.\n
We suggest using a btrfs file system as it has features useful for\n
backing up your data, as well as is capable of optimizing itself for\n
solid-state drives.""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 3, 2, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 2, 1, 1)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.input_part)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 1, 1, 1)

    def explain_swap(self, button):
        """Explain swap partitions and files"""
        self.clear_window()

        label = QtWidgets.QLabel("**Info on SWAP Partition**")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label = QtWidgets.QLabel("What is an SWAP Partition?")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 2, 1, 1, 1)

        label = QtWidgets.QLabel("""
A SWAP Partition is a partition which your system may use to\n
extend system memory. It is useful for when your system memory is\n
extremely low.\n

Because it is on your internal drive, it is capable of retaining\n
data between reboots and even total powerloss events. Thanks to this,\n
it also enables the usage of the Hibernate and Hybrid Suspend features.\n

SWAP can also be used as a file. This can allow you to easily create more\n
SWAP later, should you deem it necessary.\n

Having SWAP is mandatory on this operating system. As such, if you do not\n
create a SWAP partition, a SWAP file will be created for you.""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 3, 1, 1, 1)

        label = QtWidgets.QLabel("SWAP Partition Requirements")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 2, 2, 1, 1)

        label = QtWidgets.QLabel("""
SWAP Partitions are expected to be no smaller than 100 MB,\n
and use linux-swap file system.\n

If you are not sure how big you should make your SWAP partition,\n
simply leave that field empty and a SWAP file of the appropriate
size will be generated for you.""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 3, 2, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 2, 1, 1)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.input_part)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 1, 1, 1)

    def check_man_part_settings(self, button):
        """Check device paths provided for manual partitioner"""
        try:
            efi = self.efi_parts.currentText()
        except (AttributeError, NameError):
            efi = ""
        try:
            swap = self.swap_parts.currentText()
        except (AttributeError, NameError):
            swap = ""
        if self.root_parts.currentText() in ("", None):
            label = self.set_up_partitioner_label("ERROR: / NOT SET")
            try:
                self.grid.itemAtPosition(1, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label, 1, 1, 1, 3)
            return
        elif (efi in ("", None)) and ap.is_EFI():
            label = self.set_up_partitioner_label(
                "ERROR: System is running EFI. An EFI partition must be set.")
            try:
                self.grid.itemAtPosition(1, 1).widget().setParent(None)
            except (TypeError, AttributeError):
                pass
            self.grid.addWidget(label, 1, 1, 1, 3)
            return
        if ((swap.upper() == "FILE") or (swap == "")):
            if ap.size_of_part(self.root_parts.currentText()) < ap.get_min_root_size(bytes=False):
                label_string = \
        f"""/ is too small. Minimum Root Partition size is { round(ap.get_min_root_size(bytes=False)) } GB
Make a swap partition to reduce this minimum to { round(ap.get_min_root_size(swap=False, bytes=False)) } GB"""
                label = self.set_up_partitioner_label(label_string)
                try:
                    self.grid.itemAtPosition(1, 1).widget().setParent(None)
                except (TypeError, AttributeError):
                    pass
                self.grid.addWidget(label, 1, 1, 1, 3)
                return
        else:
            if ap.size_of_part(self.root_parts.currentText()) < ap.get_min_root_size(swap=False, bytes=False):
                label_string = f"/ is too small. Minimum Root Partition size is { round(ap.get_min_root_size(swap=False, bytes=False)) } GB"
                label = self.set_up_partitioner_label(label_string)
                try:
                    self.grid.itemAtPosition(1, 1).widget().setParent(None)
                except (TypeError, AttributeError):
                    pass
                self.grid.addWidget(label, 1, 1, 1, 3)
                return
        label = self.set_up_partitioner_label()
        try:
            self.grid.itemAtPosition(1, 1).widget().setParent(None)
        except (TypeError, AttributeError):
            pass
        self.grid.addWidget(label, 1, 1, 1, 3)
        self.data["ROOT"] = self.root_parts.currentText()

        if efi in ("", " ", None):
            self.data["EFI"] = "NULL"
        else:
            self.data["EFI"] = efi
        if self.home_parts.currentText() in ("", " ", None, "Home Partition"):
            self.data["HOME"] = "NULL"
        else:
            self.data["HOME"] = self.home_parts.currentText()
        if ((swap in ("", " ", None)) or (swap.upper() == "FILE")):
            self.data["SWAP"] = "FILE"
        else:
            self.data["SWAP"] = swap
        global PART_COMPLETION
        PART_COMPLETION = "COMPLETED"
        self.main_menu("clicked")

    def opengparted(self, button):
        """Open GParted"""
        subprocess.Popen("gparted", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.data["AUTO_PART"] = False
        self.input_part("clicked")

    def options(self, button):
        """Extraneous options menu"""
        self.clear_window()

        label = QtWidgets.QLabel("""**Extra Options**\n
The below options require a network connection, unless otherwise stated.\n
Please ensure you are connected before selecting any of these options.""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label1 = QtWidgets.QLabel("""Install third-party packages, such as NVIDIA drivers, if necessary\t\t""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 2)

        self.extras = QtWidgets.QCheckBox("Install Restricted Extras")
        if self.data["EXTRAS"]:
            self.extras.setChecked(True)
        self.extras = self._set_default_margins(self.extras)
        self.grid.addWidget(self.extras, 3, 1, 1, 2)

        label2 = QtWidgets.QLabel("""Update the system during installation""")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setTextFormat(QtCore.Qt.MarkdownText)
        label2 = self._set_default_margins(label2)
        self.grid.addWidget(label2, 4, 1, 1, 2)

        self.updates = QtWidgets.QCheckBox("Update during Installation")
        if self.data["UPDATES"]:
            self.updates.setChecked(True)
        self.updates = self._set_default_margins(self.updates)
        self.grid.addWidget(self.updates, 5, 1, 1, 2)

        label2 = QtWidgets.QLabel("""Automatically login upon boot up. Does **NOT** require internet.""")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setTextFormat(QtCore.Qt.MarkdownText)
        label2 = self._set_default_margins(label2)
        self.grid.addWidget(label2, 6, 1, 1, 2)

        self.login = QtWidgets.QCheckBox("Enable Auto-Login")
        if self.data["LOGIN"]:
            self.login.setChecked(True)
        self.login = self._set_default_margins(self.login)
        self.grid.addWidget(self.login, 7, 1, 1, 2)

        self.compat_mode = QtWidgets.QCheckBox("Enable Bootloader Compatibility Mode")
        if self.data["COMPAT_MODE"]:
            self.compat_mode.setChecked(True)
        self.compat_mode = self._set_default_margins(self.compat_mode)

        if ap.is_EFI():
            label2 = QtWidgets.QLabel("""Enable compatibility mode to improve installation reliability\n
with some UEFI systems. Does **NOT** require internet.""")
            label2.setAlignment(QtCore.Qt.AlignCenter)
            label2.setTextFormat(QtCore.Qt.MarkdownText)
            label2 = self._set_default_margins(label2)
            self.grid.addWidget(label2, 8, 1, 1, 2)

            self.grid.addWidget(self.compat_mode, 9, 1, 1, 2)

        button1 = QtWidgets.QPushButton("Okay -->")
        button1.clicked.connect(self.options_next)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 10, 2, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.main_menu)
        buton3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 10, 1, 1, 1)

    def options_next(self, button):
        """Set update and extras settings"""
        self.data["EXTRAS"] = self.extras.isChecked()
        self.data["UPDATES"] = self.updates.isChecked()
        self.data["LOGIN"] = self.login.isChecked()
        self.data["COMPAT_MODE"] = self.compat_mode.isChecked()
        global OPTIONS_COMPLETION
        OPTIONS_COMPLETION = "COMPLETED"
        self.main_menu("clicked")

    def locale(self, button):
        """Language and Time Zone settings menu"""
        self.clear_window()

        label = QtWidgets.QLabel("""**Choose your Language and Time Zone**""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        label2 = QtWidgets.QLabel("""Language""")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setTextFormat(QtCore.Qt.MarkdownText)
        label2 = self._set_default_margins(label2)
        self.grid.addWidget(label2, 2, 2, 1, 1)

        self.lang_menu = QtWidgets.QComboBox()

        for each in self.langs:
            self.lang_menu.addItem(each, self.langs[each])
        self.lang_menu.addItem("Other, User will need to set up manually.", "other")
        if self.data["LANG"] != "":
            self.lang_menu.setCurrentText(self.data["LANG"])
        self.lang_menu = self._set_default_margins(self.lang_menu)
        self.grid.addWidget(self.lang_menu, 3, 2, 1, 1)

        label3 = QtWidgets.QLabel("""Region""")
        label3.setAlignment(QtCore.Qt.AlignCenter)
        label3.setTextFormat(QtCore.Qt.MarkdownText)
        label3 = self._set_default_margins(label3)
        self.grid.addWidget(label3, 4, 2, 1, 1)

        time_zone = self.data["TIME_ZONE"].split("/")
        self.time_menu = QtWidgets.QComboBox()
        zones_pre = os.listdir("/usr/share/zoneinfo")
        zones_pre.sort()
        zones = []
        for each in zones_pre:
            if os.path.isdir(f"/usr/share/zoneinfo/{each}"):
                if each not in ("right", "posix"):
                    self.time_menu.addItem(each, each)
        if len(time_zone) > 0:
            self.time_menu.setCurrentText(time_zone[0])
        self.time_menu.currentTextChanged.connect(self.update_subregion)
        self.time_menu = self._set_default_margins(self.time_menu)
        self.grid.addWidget(self.time_menu, 5, 2, 1, 1)

        label4 = QtWidgets.QLabel("""Sub-Region""")
        label4.setAlignment(QtCore.Qt.AlignCenter)
        label4.setTextFormat(QtCore.Qt.MarkdownText)
        label4 = self._set_default_margins(label4)
        self.grid.addWidget(label4, 6, 2, 1, 1)

        self.sub_region = QtWidgets.QComboBox()
        self.sub_region = self._set_default_margins(self.sub_region)
        self.grid.addWidget(self.sub_region, 7, 2, 1, 1)

        button1 = QtWidgets.QPushButton("Okay -->")
        button1.clicked.connect(self.on_locale_completed)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 8, 4, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 8, 2, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 8, 1, 1, 1)

        self.update_subregion(self.time_menu)

    def update_subregion(self, widget):
        """Narrow subregions to possible areas
        It makes no sense to be in New York, China, when New York is in the
        USA
        """
        if widget is None:
            return
        try:
            zones = sorted(os.listdir("/usr/share/zoneinfo/" + widget))
        except TypeError:
            zones = sorted(os.listdir("/usr/share/zoneinfo/" + widget.currentText()))
        for each in range(self.sub_region.count() - 1, -1, -1):
            self.sub_region.removeItem(each)
        zones.sort()
        for each7 in zones:
            self.sub_region.addItem(each7, each7)
        time_zone = self.data["TIME_ZONE"].split("/")
        if len(time_zone) > 1:
            self.sub_region.setCurrentText(time_zone[1])

    def on_locale_completed(self, button):
        """Set default language and time zone if user did not set them"""
        if self.lang_menu.currentText() is not None:
            self.data["LANG"] = self.lang_menu.currentText()
        else:
            self.data["LANG"] = "en"

        if ((self.time_menu.currentText() is not None) and (
                self.sub_region.currentText() is not None)):
            self.data["TIME_ZONE"] = self.time_menu.currentText()
            self.data["TIME_ZONE"] = self.data["TIME_ZONE"] + "/"
            self.data["TIME_ZONE"] = self.data["TIME_ZONE"] + self.sub_region.currentText()
        else:
            self.data["TIME_ZONE"] = "America/New_York"

        global LOCALE_COMPLETION
        LOCALE_COMPLETION = "COMPLETED"
        self.main_menu("clicked")

    def keyboard(self, button):
        """Keyboard Settings Dialog"""
        self.clear_window()

        label = QtWidgets.QLabel("""**Choose your Keyboard layout**""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 4)

        model_label = QtWidgets.QLabel("""Model: """)
        model_label.setAlignment(QtCore.Qt.AlignCenter)
        model_label.setTextFormat(QtCore.Qt.MarkdownText)
        model_label = self._set_default_margins(model_label)
        self.grid.addWidget(model_label, 2, 1, 1, 1)

        self.model_menu = QtWidgets.QComboBox()
        with open("/etc/edamame/keyboards.json", "r") as file:
            keyboards = json.load(file)
        layout_list = keyboards["layouts"]
        model = keyboards["models"]
        for each8 in model:
            self.model_menu.addItem(each8, model[each8])
        if self.data["MODEL"] != "":
                index = self.model_menu.findText(self.data["MODEL"], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.model_menu.setCurrentIndex(index)
        else:
            index = self.model_menu.findText("pc105", QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.model_menu.setCurrentText("pc105")
        self.model_menu = self._set_default_margins(self.model_menu)
        self.grid.addWidget(self.model_menu, 2, 2, 1, 3)

        layout_label = QtWidgets.QLabel("""Layout: """)
        layout_label.setAlignment(QtCore.Qt.AlignCenter)
        layout_label.setTextFormat(QtCore.Qt.MarkdownText)
        layout_label = self._set_default_margins(layout_label)
        self.grid.addWidget(layout_label, 3, 1, 1, 1)

        self.layout_menu = QtWidgets.QComboBox()
        for each8 in layout_list:
            self.layout_menu.addItem(each8, layout_list[each8])
        if self.data["LAYOUT"] != "":
            index = self.layout_menu.findText(self.data["LAYOUT"], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.layout_menu.setCurrentIndex(index)
        self.layout_menu.currentTextChanged.connect(self.varient_narrower)
        self.layout_menu = self._set_default_margins(self.layout_menu)
        self.grid.addWidget(self.layout_menu, 3, 2, 1, 3)

        varient_label = QtWidgets.QLabel("""Variant: """)
        varient_label.setAlignment(QtCore.Qt.AlignCenter)
        varient_label.setTextFormat(QtCore.Qt.MarkdownText)
        varient_label = self._set_default_margins(varient_label)
        self.grid.addWidget(varient_label, 4, 1, 1, 1)

        self.varient_menu = QtWidgets.QComboBox()
        self.varients = keyboards["varints"]
        for each8 in self.varients:
            for each9 in self.varients[each8]:
                self.varient_menu.addItem(each9, self.varients[each8][each9])
        if self.data["VARIENT"] != "":
            index = self.varient_menu.findText(self.data["VARIENT"], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.varient_menu.setCurrentIndex(index)
        self.varient_menu = self._set_default_margins(self.varient_menu)
        self.grid.addWidget(self.varient_menu, 4, 2, 1, 3)

        button1 = QtWidgets.QPushButton("Okay -->")
        button1.clicked.connect(self.on_keyboard_completed)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 4, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 3, 1, 1)

        button3 = QtWidgets.QPushButton("<-- Back")
        button3.clicked.connect(self.main_menu)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 6, 1, 1, 1)

    def varient_narrower(self, widget):
        """Narrow down possible keyboard varients"""
        term = self.layout_menu.currentData()
        for each in range(self.varient_menu.count() - 1, -1, -1):
            self.varient_menu.removeItem(each)

        for each9 in self.varients[term]:
            self.varient_menu.addItem(each9, self.varients[term][each9])
        if self.data["VARIENT"] != "":
            self.varient_menu.setCurrentText(self.data["VARIENT"])
        self.varient_menu = self._set_default_margins(self.varient_menu)

    def on_keyboard_completed(self, button):
        """Set default keyboard layout if user did not specify one"""
        if self.model_menu.currentText() is not None:
            self.data["MODEL"] = self.model_menu.currentText()
        else:
            self.data["MODEL"] = "Generic 105-key PC (intl.)"
        if self.layout_menu.currentText() is not None:
            self.data["LAYOUT"] = self.layout_menu.currentText()
        elif "kernel keymap" in self.data["MODEL"]:
            self.data["LAYOUT"] = ""
        else:
            self.data["LAYOUT"] = "English (US)"
        if self.varient_menu.currentText() is not None:
            self.data["VARIENT"] = self.varient_menu.currentText()
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
        if "COMPLETED" not in (KEYBOARD_COMPLETION, LOCALE_COMPLETION,
                               OPTIONS_COMPLETION, PART_COMPLETION,
                               USER_COMPLETION):
            self.label.setText("""Feel free to complete any of the below segments in any order.\n
However, all segments must be completed.\n
\n
**One or more segments have not been completed**\n
Please complete these segments, then try again.\n
Or, exit installation.\n""")
        else:
            self.complete()

    def complete(self):
        """Set settings var"""
        self.close()
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

        label = QtWidgets.QLabel("""\n**Are you sure you want to exit?**

Exiting now will cause all your settings to be lost.""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        yes = QtWidgets.QPushButton("Exit")
        yes.clicked.connect(self._exit)
        yes = self._set_default_margins(yes)
        self.grid.addWidget(yes, 2, 1, 1, 1)

        no = QtWidgets.QPushButton("Return")
        no.clicked.connect(self.main_menu)
        no = self._set_default_margins(no)
        self.grid.addWidget(no, 2, 2, 1, 1)

    def _exit(self, button):
        """Exit"""
        self.close()
        self.data = 1
        return 1

    def clear_window(self):
        """Clear Window"""
        for i in range(self.grid.rowCount() - 1, -1, -1):
            for i2 in range(self.grid.columnCount() - 1, -1, -1):
                try:
                    self.grid.itemAtPosition(i, i2).widget().setParent(None)
                except (TypeError, AttributeError):
                    pass


def show_main(boot_time=False):
    """Show Main UI"""
    make_kbd_names()
    app = QtWidgets.QApplication([sys.argv[0]])
    window = Main(app.primaryScreen().size())
    if boot_time:
        window = QCommon.set_window_undecorated(window)
    window = QCommon.set_window_nonresizeable(window)
    # window.set_resizable(False)
    window.show()
    app.exec()
    window.complete()
    return window.data


def make_kbd_names():
    """Get Keyboard Names faster"""
    if os.path.isfile("/etc/edamame/keyboards.json"):
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
    os.chdir("/etc/edamame")
    with open("keyboards.json", "w+") as file:
        file.write(data)


if __name__ == '__main__':
    print(show_main())
