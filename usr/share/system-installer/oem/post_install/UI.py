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
import multiprocessing
from subprocess import Popen, check_output, DEVNULL
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import configure


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
    Welcome to %s!

    This tool will help you set up your new system in just a few short minutes.

    Click Next to continue to the Main Menu.
    """ % (DISTRO)


class Main(Gtk.Window):
    """Main UI Window"""
    def __init__(self):
        """Initialize the Window"""
        Gtk.Window.__init__(self, title="System Installer")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("system-installer")

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

        # Open initial window
        self.reset("clicked")

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

    def reset(self, button):
        """Main Splash Window"""
        global DEFAULT
        self.clear_window()

        label = Gtk.Label()
        label.set_markup(DEFAULT)
        label.set_justify(Gtk.Justification.LEFT)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 4, 1)

        button1 = Gtk.Button.new_with_label("Next -->")
        button1.connect("clicked", self.keyboard)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 4, 2, 1, 1)

        self.set_position(Gtk.WindowPosition.CENTER)

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
        self.username = self._set_default_margins(self.username)
        self.grid.attach(self.username, 3, 3, 1, 1)

        label2 = Gtk.Label()
        label2.set_markup("    Computer\'s Name:   ")
        label2.set_justify(Gtk.Justification.RIGHT)
        label2 = self._set_default_margins(label2)
        self.grid.attach(label2, 1, 4, 2, 1)

        self.compname = Gtk.Entry()
        self.compname.set_text("drauger-oem-system")
        self.compname = self._set_default_margins(self.compname)
        self.grid.attach(self.compname, 3, 4, 1, 1)

        label3 = Gtk.Label()
        label3.set_markup("    Password:   ")
        label3.set_justify(Gtk.Justification.RIGHT)
        label3 = self._set_default_margins(label3)
        self.grid.attach(label3, 1, 5, 2, 1)

        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.password = self._set_default_margins(self.password)
        self.grid.attach(self.password, 3, 5, 1, 1)

        label4 = Gtk.Label()
        label4.set_markup("    Confirm Pasword:    ")
        label4.set_justify(Gtk.Justification.RIGHT)
        label4 = self._set_default_margins(label4)
        self.grid.attach(label4, 1, 6, 2, 1)

        self.passconf = Gtk.Entry()
        self.passconf.set_visibility(False)
        self.passconf = self._set_default_margins(self.passconf)
        self.grid.attach(self.passconf, 3, 6, 1, 1)

        self.login = Gtk.CheckButton.new_with_label("Enable Auto-Login")
        self.login.set_active(True)
        self.login = self._set_default_margins(self.login)
        self.grid.attach(self.login, 2, 7, 2, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.on_user_completed)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 3, 8, 1, 1)

        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

    def on_user_completed(self, button):
        """Password, Username, and hostname Checker"""
        password = self.password.get_text()
        pass2 = self.passconf.get_text()
        username = self.username.get_text()
        username = username.lower()
        comp_name = self.compname.get_text()
        if password != pass2:
            label5 = Gtk.Label()
            label5.set_markup("Passwords do not match")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif len(password) < 4:
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
        elif has_special_character(username):
            label5 = Gtk.Label()
            label5.set_markup("Username contains special characters")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif " " in username:
            label5 = Gtk.Label()
            label5.set_markup("Username contains space")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif len(username) < 1:
            label5 = Gtk.Label()
            label5.set_markup("Username empty")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif has_special_character(comp_name):
            label5 = Gtk.Label()
            label5.set_markup("Computer Name contains non-hyphen special character")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif " " in comp_name:
            label5 = Gtk.Label()
            label5.set_markup("Computer Name contains space")
            label5.set_justify(Gtk.Justification.CENTER)
            label5 = self._set_default_margins(label5)
            try:
                self.grid.remove(self.grid.get_child_at(1, 7))
            except TypeError:
                pass
            self.grid.attach(label5, 1, 7, 3, 1)
        elif len(comp_name) < 1:
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
            self.complete()

        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

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
        self.lang_menu = self._set_default_margins(self.lang_menu)
        self.grid.attach(self.lang_menu, 2, 3, 1, 1)

        label3 = Gtk.Label()
        label3.set_markup("""

Region""")
        label3.set_justify(Gtk.Justification.LEFT)
        label3 = self._set_default_margins(label3)
        self.grid.attach(label3, 2, 4, 1, 1)

        self.time_menu = Gtk.ComboBoxText.new()
        zones = ["Africa", "America", "Antarctica", "Arctic", "Asia",
                 "Atlantic", "Australia", "Brazil", "Canada", "Chile",
                 "Europe", "Indian", "Mexico", "Pacific", "US"]
        for each6 in zones:
            self.time_menu.append(each6, each6)
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

        self.update_subregion(self.time_menu)
        self.set_position(Gtk.WindowPosition.CENTER)

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
            lang = self.lang_menu.get_active_id()
        else:
            lang = "en"

        if ((self.time_menu.get_active_id() is not None) and (
                self.sub_region.get_active_id() is not None)):
            tz = self.time_menu.get_active_id()
            tz = tz + "/"
            tz = tz + self.sub_region.get_active_id()
        else:
            tz = "America/New_York"

        # Usually we watch these processes to make sure they complete and
        # To close them out cleanly when they get done. However it's unlikely
        # This system will go long without a reboot after first boot
        # That will kill this process, if the kernel or Python exiting
        # Doesn't do it first.
        multiprocessing.Process(target=configure_locale,
                                args=[tz, lang]).start()

        self.user("clicked")

    def keyboard(self, button):
        """Keyboard Settings Dialog"""
        self.clear_window()

        self.label = Gtk.Label()
        self.label.set_markup("""
    <b>Choose your Keyboard layout</b>\t
    """)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label = self._set_default_margins(self.label)
        self.grid.attach(self.label, 1, 1, 4, 1)

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
        self.varient_menu = self._set_default_margins(self.varient_menu)
        self.grid.attach(self.varient_menu, 2, 4, 3, 1)

        button1 = Gtk.Button.new_with_label("Okay -->")
        button1.connect("clicked", self.on_keyboard_completed)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 4, 6, 1, 1)

        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

    def varient_narrower(self, widget):
        """Narrow down possible keyboard varients"""
        term = self.layout_menu.get_active_id()
        self.varient_menu.remove_all()

        for each9 in self.varients[term]:
            self.varient_menu.append(self.varients[term][each9], each9)
        self.varient_menu = self._set_default_margins(self.varient_menu)

        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()


    def on_keyboard_completed(self, button):
        """Set default keyboard layout if user did not specify one"""
        model = self.model_menu.get_active_id()
        layout = self.layout_menu.get_active_id()
        varient = self.varient_menu.get_active_id()
        if model is None:
            model = "Generic 105-key PC (intl.)"
        if layout is None:
            if "kernel keymap" in model:
                layout = ""
            else:
                layout = "English (US)"
        if varient is None:
            if "kernel keymap" in model:
                varient = ""
            else:
                varient = "euro"

        multiprocessing.Process(target=configure_keyboard,
                                args=[model, layout, varient]).start()

        self.locale("clicked")

    def complete(self):
        """Set settings var"""
        Gtk.main_quit("delete-event")
        self.destroy()

    def clear_window(self):
        """Clear Window"""
        children = self.grid.get_children()
        for each0 in children:
            self.grid.remove(each0)


def show_main():
    """Show Main UI"""
    make_kbd_names()
    window = Main()
    window.set_decorated(False)
    window.set_resizable(False)
    window.show_all()
    Gtk.main()
    window.exit("clicked")
    window.destroy()
    return data


def configure_locale(tz, lang):
    """Configure time zone and lang"""
    time_proc = multiprocessing.Process(target=configure.set_time.set_time,
                                        args=[tz])
    time_proc.start()
    lang_proc = multiprocessing.Process(target=configure.set_locale.set_locale,
                                        args=[lang])
    lang_proc.start()
    monitor_procs([time_proc, lang_proc])


def configure_keyboard(model, layout, varient):
    """Configure Keyboard"""
    key_proc = multiprocessing.Process(target=configure.keyboard.configure,
                                        args=[model, layout, varient])
    key_proc.start()
    monitor_procs([key_proc])


def monitor_procs(procs_to_monitor):
    """Monitor Procs"""
    procs = []
    for each in procs_to_monitor:
        procs.append([each, True])
    while True in [procs[i][1] for i in range(len(procs))]:
        for each in procs:
            if ((not each[0].is_alive()) and (each[1] is True)):
                each.join()
                each[1] = False


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
