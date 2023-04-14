#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pre_install.py
#
#  Copyright 2023 Thomas Castleman <contact@draugeros.org>
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
import subprocess
import auto_partitioner
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


def has_special_character(input_string):
    """Check for special characters"""
    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(input_string) is None:
        return False
    return True


class Main(Gtk.Window):
    """Main UI Window"""
    def __init__(self):
        """Initialize the Window"""
        Gtk.Window.__init__(self, title="System Installer")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("system-installer")

        # Initialize setting values
        self.data = {"HOME": "", "ROOT": "", "EFI": "",
                     "raid_array": {"raid_type": None,
                                    "disks": {"1": None,
                                              "2": None,
                                              "3": None,
                                              "4": None}}}

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
        self.auto_partition("clicked")

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

    def auto_partition(self, button):
        """Auto Partitioning Settings Window"""
        self.clear_window()

        self.set_position(Gtk.WindowPosition.CENTER)

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
        self.grid.attach(button1, 4, 6, 1, 1)

        button5 = Gtk.Button.new_with_label("Make RAID Array")
        button5.connect("clicked", self.define_array)
        button5 = self._set_default_margins(button5)
        self.grid.attach(button5, 3, 6, 1, 1)

        button2 = Gtk.Button.new_with_label("Exit")
        button2.connect("clicked", self.exit)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 2, 6, 1, 1)

        self.show_all()

    def define_array(self, widget, error=None):
        """Define btrfs RAID Array settings"""
        self.clear_window()

        self.set_position(Gtk.WindowPosition.CENTER)

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

        button3 = Gtk.Button.new_with_label("<-- Back")
        button3.connect("clicked", self.auto_partition)
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
                    elif device["fstype"] != None:
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

            home_cmbbox = Gtk.ComboBoxText.new()

            # properly format device names and add to combo box
            for device in new_dev_list:
                if device["name"][:5] != "/dev/":
                    device['name'] = "/dev/%s" % device['name']

                home_cmbbox.append(device['name'], "%s    Size: %s" % (device['name'], device['size']))

            if self.data["HOME"] != "":
                home_cmbbox.set_active_id(self.data["HOME"])
            home_cmbbox.connect("changed", self.select_home_part)
            parts = self._set_default_margins(home_cmbbox)
            self.grid.attach(home_cmbbox, 1, 5, 2, 1)
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
        if auto_partitioner.is_EFI():
            self.data["EFI"] = True
        else:
            self.data["EFI"] = False
        if self.data["HOME"] == "":
            self.data["HOME"] = "NULL"
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
            self.complete("clicked")

    def complete(self, widget):
        """Set settings var"""
        Gtk.main_quit("delete-event")
        self.destroy()
        if isinstance(self.data, dict):
            if "" in self.data.values():
                self.data = 1
        else:
            self.data = 1

    def exit(self, button):
        """Exit dialog"""
        self.clear_window()

        self.set_position(Gtk.WindowPosition.CENTER)

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
        no.connect("clicked", self.auto_partition)
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


def show_main():
    """Show Main UI"""
    window = Main()
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Main._exit)
    window.show_all()
    Gtk.main()
    data = window.return_data()
    window.exit("clicked")
    window.destroy()
    return data



if __name__ == '__main__':
    print(show_main())
