#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  success.py
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
"""Success Reporting UI"""
from shutil import rmtree, copytree, move, copyfile
import subprocess
import os
import sys
import json
import xmltodict
import tarfile as tar
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
try:
    import UI.report as report
except ModuleNotFoundError:
    import report


class Main(report.Main):
    """Success UI Class"""
    def __init__(self, settings):
        """Initialize data"""
        super(Main, self).__init__()
        self.scrolling = False
        self.settings = settings

        try:
            with open("/etc/system-installer/settings.json", "r") as file:
                self.distro = json.load(file)["distro"]
        except (FileNotFoundError, KeyError):
            self.distro = "Linux"
        self.main_menu("clicked")

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

    def main_menu(self, widget):
        """Main Success Window"""
        self.clear_window()

        if hasattr(self, 'text_buffer'):
            self.text_buffer.set_text("", length=0)

        text = """
\t<b>%s has been successfully installed on your computer!</b>\t
""" % (self.distro)
        if "OEM" not in self.settings.values():
            text = text + """\tPlease consider sending an installation report to our team,
            \tusing the "Send Installation Report" button below.\t\n\n"""
        label = Gtk.Label()
        label.set_markup(text)
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 4, 1)

        if "OEM" in self.settings.values():
            button1 = Gtk.Button.new_with_label("Power Off System")
            button1.connect("clicked", __poweroff__)
        else:
            button1 = Gtk.Button.new_with_label("Restart System")
            button1.connect("clicked", __reboot__)
        button1 = self._set_default_margins(button1)
        if "OEM" in self.settings.values():
            self.grid.attach(button1, 4, 6, 1, 1)
        else:
            self.grid.attach(button1, 2, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        if "OEM" in self.settings.values():
            self.grid.attach(button2, 1, 6, 2, 1)
        else:
            self.grid.attach(button2, 1, 6, 1, 1)

        if "OEM" not in self.settings.values():
            button3 = Gtk.Button.new_with_label("Advanced")
            button3.connect("clicked", self.onadvclicked)
            button3 = self._set_default_margins(button3)
            self.grid.attach(button3, 3, 6, 1, 1)

            button4 = Gtk.Button.new_with_label("Send Installation Report")
            button4.connect("clicked", self.main)
            button4 = self._set_default_margins(button4)
            self.grid.attach(button4, 4, 6, 1, 1)

        self.set_position(Gtk.WindowPosition.CENTER)

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
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        button1 = Gtk.Button.new_with_label("Dump Settings to File")
        button1.connect("clicked", self.dump_settings_dialog)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 3, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Delete Installation")
        button2.connect("clicked", self.ondeletewarn)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 1, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("Add PPA")
        button3.connect("clicked", self.add_ppa)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 2, 6, 1, 1)

        button4 = Gtk.Button.new_with_label("Exit")
        button4.connect("clicked", self.exit)
        button4 = self._set_default_margins(button4)
        self.grid.attach(button4, 3, 7, 1, 1)

        button5 = Gtk.Button.new_with_label("<-- Back")
        button5.connect("clicked", self.main_menu)
        button5 = self._set_default_margins(button5)
        self.grid.attach(button5, 1, 7, 1, 1)

        self.show_all()

    def ondeletewarn(self, button):
        """Warning about Deleting the installation"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
\tAre you sure you wish to delete the new installation?\t
\tNo data will be recoverable.\t
""")
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        button5 = Gtk.Button.new_with_label("DELETE")
        button5.connect("clicked", self.delete_install)
        button5 = self._set_default_margins(button5)
        self.grid.attach(button5, 2, 2, 1, 1)

        button4 = Gtk.Button.new_with_label("Exit")
        button4.connect("clicked", self.exit)
        button4 = self._set_default_margins(button4)
        self.grid.attach(button4, 3, 2, 1, 1)

        button6 = Gtk.Button.new_with_label("<-- Back")
        button6.connect("clicked", self.onadvclicked)
        button6 = self._set_default_margins(button6)
        self.grid.attach(button6, 1, 2, 1, 1)

        self.show_all()

    def delete_install(self, button):
        """Delete Installation from Drive
         This code is dangerous. Be wary
        """
        delete = os.listdir("/mnt")
        for each in delete:
            try:
                os.remove("/mnt/" + each)
            except IsADirectoryError:
                rmtree("/mnt/" + each)
        self.exit("clicked")

    def add_ppa(self, button):
        """UI to add PPA to installation"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""\n\tWhat PPAs would you like to add?\t\n""")
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        label1 = Gtk.Label()
        label1.set_markup("""\tPPA:""")
        label1.set_justify(Gtk.Justification.RIGHT)
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 1, 1)

        self.ppa_entry = Gtk.Entry()
        self.ppa_entry.set_visibility(True)
        self.ppa_entry = self._set_default_margins(self.ppa_entry)
        self.grid.attach(self.ppa_entry, 2, 2, 1, 1)

        button4 = Gtk.Button.new_with_label("Add PPA")
        button4.connect("clicked", self.add_ppa_backend)
        button4 = self._set_default_margins(button4)
        self.grid.attach(button4, 2, 3, 1, 1)

        button6 = Gtk.Button.new_with_label("Exit")
        button6.connect("clicked", self.exit)
        button6 = self._set_default_margins(button6)
        self.grid.attach(button6, 3, 3, 1, 1)

        button5 = Gtk.Button.new_with_label("<-- Back")
        button5.connect("clicked", self.onadvclicked)
        button5 = self._set_default_margins(button5)
        self.grid.attach(button5, 1, 3, 1, 1)

        self.show_all()

    def add_ppa_backend(self, button):
        """Unfunction to add PPAs"""
        self.grid.remove(self.grid.get_child_at(1, 1))
        try:
            subprocess.Popen(["add-apt-repository", "--yes", "PPA:%s" %
                              ((self.ppa_entry.get_text()).lower())])

            label = Gtk.Label()
            label.set_markup("""\n\tWhat PPAs would you like to add?\t
\t<b>%s added successfully!</b>\t\n""" % (self.ppa_entry.get_text()))
            label.set_justify(Gtk.Justification.CENTER)
            label = self._set_default_margins(label)
            self.grid.attach(label, 1, 1, 2, 1)

        except subprocess.CalledProcessError:
            label = Gtk.Label()
            label.set_markup("""\n\tWhat PPAs would you like to add?\t
\t<b>adding %s failed.</b>\t\n""" % (self.ppa_entry.get_text()))
            label.set_justify(Gtk.Justification.CENTER)
            label = self._set_default_margins(label)
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
        """Get what to dump and what not to dump"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
\tSelect what you would like included in your Quick Install file.\t
""")
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 4, 1)

        self.settings_toggle = Gtk.CheckButton.new_with_label("Installation Settings")
        self.settings_toggle.set_active(True)
        self.settings_toggle = self._set_default_margins(self.settings_toggle)
        self.grid.attach(self.settings_toggle, 1, 2, 4, 1)

        self.network_toggle = Gtk.CheckButton.new_with_label("Network Settings")
        self.network_toggle.set_active(True)
        self.network_toggle = self._set_default_margins(self.network_toggle)
        self.grid.attach(self.network_toggle, 1, 3, 4, 1)

        self.wall_toggle = Gtk.CheckButton.new_with_label("Wallpaper")
        self.wall_toggle.set_active(False)
        self.wall_toggle = self._set_default_margins(self.wall_toggle)
        self.grid.attach(self.wall_toggle, 1, 4, 4, 1)

        button4 = Gtk.Button.new_with_label("Exit")
        button4.connect("clicked", self.exit)
        button4 = self._set_default_margins(button4)
        self.grid.attach(button4, 4, 6, 1, 1)

        button5 = Gtk.Button.new_with_label("<-- Back")
        button5.connect("clicked", self.onadvclicked)
        button5 = self._set_default_margins(button5)
        self.grid.attach(button5, 1, 6, 1, 1)

        button3 = Gtk.Button.new_with_label("DUMP")
        button3.connect("clicked", self.dump_settings_file_dialog)
        button3 = self._set_default_margins(button3)
        self.grid.attach(button3, 1, 5, 4, 1)

        self.show_all()

    def dump_settings_file_dialog(self, button):
        """Dump Settings File Dialog"""
        dialog = Gtk.FileChooserDialog("System Installer", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE,
                                        Gtk.ResponseType.ACCEPT))
        dialog.set_action(Gtk.FileChooserAction.SAVE)
        try:
            if (self.network_toggle.get_active() or self.wall_toggle.get_active()):
                dialog.set_current_name("installation-settings.tar.xz")
            else:
                dialog.set_current_name("installation-settings.json")
        except NameError:
            dialog.set_current_name("installation-settings.json")
        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            if self.network_toggle.get_active():
                adv_dump_settings(self.settings, dialog.get_filename(),
                                  copy_net=self.network_toggle.get_active(),
                                  copy_set=self.settings_toggle.get_active(),
                                  copy_wall=self.wall_toggle.get_active())
            else:
                dump_settings(self.settings, dialog.get_filename())

        dialog.destroy()
        self.onadvclicked("clicked")


def dump_settings(settings, path):
    """Dump Settings to File"""
    with open(path, "w+") as dump_file:
        json.dump(settings, dump_file, indent=1)


def adv_dump_settings(settings, dump_path, copy_net=True, copy_set=True,
                      copy_wall=False):
    """Compress Install settings and
       Network settings to tar bar for later use
    """
    # Make our directory layout
    os.mkdir("/tmp/working_dir")
    os.mkdir("/tmp/working_dir/settings")
    os.mkdir("/tmp/working_dir/assets")
    # dump our installation settings and grab our network settings too
    if copy_set:
        dump_settings(settings,
                      "/tmp/working_dir/settings/installation-settings.json")
    if copy_net:
        # /etc/NetworkManager/system-connections has perms 755, so we can see the files in it
        # but those files have permissions 600, and we don't own them, so we can't read them.
        # Must temporarily change them to 644 so we can read them
        net_connections = "/etc/NetworkManager/system-connections"
        if len(os.listdir(net_connections)) > 0:
            subprocess.check_call("echo 'toor' | sudo -S chmod 644 " + net_connections + "/*",
                                  shell=True)
            copytree("/etc/NetworkManager/system-connections",
                     "/tmp/working_dir/settings/network-settings")
            subprocess.check_call("echo 'toor' | sudo -S chmod 600 " + net_connections + "/*",
                                  shell=True)
    if copy_wall:
        # Grab wallpaper
        home = os.getenv("HOME")
        wall_path = []
        monitors = []
        with open(home + "/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml", "r") as fb:
            xml = xmltodict.parse(fb.read())
        for each in xml["channel"]["property"][0]["property"][0]["property"]:
            monitors.append(each["@name"])
            for each1 in each["property"][0]["property"]:
                try:
                    if each1["@name"] == "last-image":
                        wall_path.append(each1["@value"])
                except (AttributeError, TypeError):
                    pass
        wall_path_unique = __unique__(wall_path)
        # Copy designated files into "assets"
        if len(wall_path_unique) == 1:
            # we only have one wallpaper, so copy that into assets/master
            # then, dump the list of screens to assets/screens.list
            # when read in, this will make it so that the wallpaper is used on
            # all the same screens as before
            os.mkdir("/tmp/working_dir/assets/master")
            with open("/tmp/working_dir/assets/screens.list", w) as screens_list:
                for each in monitors:
                    screens_list.write(each + "\n")
            file_type = wall_path[0].split("/")[-1].split(".")[-1]
            copyfile(wall_path[0],
                     "/tmp/working_dir/assets/master/wallpaper." + file_type)
        else:
            # We have different wallpapers on different screens
            # This has a trade-off of taking up more disk space in the tar ball
            # But, it should work out okay
            for each in range(len(wall_path)):
                os.mkdir("/tmp/working_dir/assets/" + monitors[each])
                file_type = wall_path[each].split("/")[-1].split(".")[-1]
                copyfile(wall_path[each],
                         "/tmp/working_dir/assets/" + monitors[each] + "/wallpaper." + file_type)
    # make our tar ball, with XZ compression
    os.chdir("/tmp/working_dir")
    tar_file = tar.open(name=dump_path.split("/")[-1], mode="w:xz")
    tar_file.add(name="settings")
    tar_file.add(name="assets")
    tar_file.close()
    # copy it to the desired location
    move(dump_path.split("/")[-1], dump_path)
    os.chmod(dump_path, 0o740)
    os.chown(dump_path, 1000, 1000)
    # clean up
    rmtree("/tmp/working_dir")


def __unique__(starting_list):

    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in starting_list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


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
    """Reboot the system"""
    subprocess.Popen(["/sbin/reboot"])
    sys.exit(0)


def __poweroff__(button):
    """Shutdown the system"""
    subprocess.Popen(["/sbin/poweroff"])
    sys.exit(0)


if __name__ == '__main__':
    show_success(sys.argv[1])
