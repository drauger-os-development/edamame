#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  report.py
#
#  Copyright 2022 Thomas Castleman <contact@draugeros.org>
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
"""Installation Reporting UI"""
from subprocess import Popen, check_output, PIPE, STDOUT, CalledProcessError
from os import getenv, remove, chmod, path
from datetime import datetime
from shutil import copyfile
import time
import json
import gnupg
import gi
import urllib3

# Configuration required to use some of these libs
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
try:
    gpg = gnupg.GPG(gnupghome="/home/live/.gnupg")
except ValueError:
    try:
        gpg = gnupg.GPG(gnupghome=getenv("HOME") + "/.gnupg")
    except ValueError:
        gpg = gnupg.GPG(gnupghome="/home/drauger-user/.gnupg")


class Main(Gtk.Window):
    """Main UI and tools for reporting installations"""
    def __init__(self):
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

        self.default_message = """
Write a custom message to our developers and contributors!
If you would like a response, please leave:
* Your name (if this is not left we will use your username)
* A way to get in contact with you through one or more of:
* Email
* Telegram
* Discord
* Mastodon
* Twitter
"""

    def clear_window(self):
        """Clear Window"""
        children = self.grid.get_children()
        for each in children:
            self.grid.remove(each)
        if self.scrolling:
            self.scrolled_window.remove(self.grid)
            self.remove(self.scrolled_window)
            self.add(self.grid)
            self.scrolling = False
            self.set_default_size(-1, -1)

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

    def cpu_toggle(self, widget):
        """Toggle sending CPU info"""
        if widget.get_active():
            self.cpu_setting = True
        else:
            self.cpu_setting = False

    def cpu_explaination(self, widget):
        """Explain why we need CPU info"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>Why to report CPU info</b>\t""")
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 2, 1)

        label1 = Gtk.Label()
        label1.set_markup("""
    Knowing what CPUs most of our users use helps us to optimize Drauger OS.
    It allows us to know if we have more or less CPU cores to take
    advantage of, or if we need to focus on becoming even lighter weight.

    It also gives us valuable information such as CPU vulnerabilities that are
    common among our users. Knowing this helps us decide if we need to keep \t
    certain security measures enabled, or if we can disable some for better
    performance with little to no risk to security.
    \t""")
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 2, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 1, 12, 1, 1)

        self.show_all()

    def gpu_toggle(self, widget):
        """Toggle sending GPU/PCIe info"""
        if widget.get_active():
            self.gpu_setting = True
        else:
            self.gpu_setting = False

    def gpu_explaination(self, widget):
        """Explain why we need GPU/PCIe info"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>Why to report GPU / PCIe info</b>\t""")
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 2, 1)

        label1 = Gtk.Label()
        label1.set_markup("""
    Knowing what GPUs most of our users use helps us to optimize Drauger OS.
    It can help us know if we need to put more work into Nvidia and/or AMD
    support.

    It can also help us know if we need to lighten the grpahical load on our
    users GPUs based on the age and/or power of these GPUs. Or, if we can
    afford a little eye candy.

    As for PCIe info, this can help us ensure support for common Wi-Fi cards is
    built into the kernel, and drivers that aren't needed aren't included. This
    can save space on your system, as well as speed up updates and increase \t
    hardware support.
    \t""")
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 2, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 1, 12, 1, 1)
        self.show_all()

    def ram_toggle(self, widget):
        """Toggle sending RAM info"""
        if widget.get_active():
            self.ram_setting = True
        else:
            self.ram_setting = False

    def ram_explaination(self, widget):
        """Explain why we need RAM info"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>Why to report RAM/SWAP info</b>\t""")
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 2, 1)

        label1 = Gtk.Label()
        label1.set_markup("""
    Knowing how much RAM our users systems have helps us determine if\t
    Drauger OS is using too much RAM.

    Knowing how much SWAP our users have helps us understand if users
    understand the neccessity of SWAP, and also what kind of device
    they may be using. That way, we can optimize to run better on laptops\t
    or desktops as needed.

    Right now, all this gives us is the AMOUNT of RAM and SWAP that you
    have. In the future, we do plan to get RAM type (DDR2, DDR3, etc.),
    and RAM speed. This will help us better understand the age of your
    system, how responsive it is, and how well lower end systems can
    handle eye candy.
    \t""")
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 2, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 1, 12, 1, 1)

        self.show_all()

    def disk_toggle(self, widget):
        """Toggle Sending Disk Info"""
        if widget.get_active():
            self.disk_setting = True
        else:
            self.disk_setting = False

    def disk_explaination(self, widget):
        """Explain why we need Disk Info"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>Why to report Disk and Partitioning info</b>\t""")
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 2, 1)

        label1 = Gtk.Label()
        label1.set_markup("""
    Understanding our users partitioning and disk setups helps us know
    if our users are dual-booting Drauger OS. This, in turn with the added
    benefit of knowing immediatly whether our users are using the automatic\t
    or manual partitioning systems tells us where to focus our effort.

    This can mean we are more likely to catch bugs or add new features
    in one area or another.
    \t""")
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 2, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 1, 12, 1, 1)

        self.show_all()

    def log_toggle(self, widget):
        """Toggle sending the log"""
        if widget.get_active():
            self.log_setting = True
        else:
            self.log_setting = False

    def log_explaination(self, widget):
        """Explaination for why we need the installation log"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    <b>Why to send the Installation Log</b>\t""")
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 2, 1)

        label1 = Gtk.Label()
        label1.set_markup("""
    As soon as the installation of Drauger OS completed, the installation log
    was copied to your internal drive.

    Normally, if you have a bug that might be related to the installer, we
    would ask you to send us that log. By sending it now, we don't have to do
    that. Instead, we can give you a command to run in your terminal. The
    output of that command will tell us which installation log is yours
    so we can immediatly access it and track down bugs.

    <b>If you send nothing else, please send this.</b>
    \t""")
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 1, 2, 2, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 1, 12, 1, 1)

        self.show_all()

    def exit(self, button):
        """Exit"""
        Gtk.main_quit("delete-event")
        self.destroy()
        return 1

    def message_handler(self, widget):
        """Generate Message then show it"""
        self.generate_message()
        self.preview_message("clicked")

    def send_report(self, widget):
        """Send installation Report"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("\n\n\t\tSending Report. Please Wait . . .\t\t\n\n")
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 1, 1)
        self.show_all()

        try:
            copyfile(self.path, "/mnt/var/log/installation_report.txt")
        except:
            pass

        try:
            # Get keys
            http = urllib3.PoolManager()
            with open("/etc/system-installer/settings.json",
                      "r") as config:
                URL = json.load(config)["report"]
            data = http.request("GET", URL["recv_keys"]).data
            key = data.decode()
            # Import keys
            result = gpg.import_keys(key)
            # Encrypt file using newly imported keys
            with open(self.path, "rb") as signing:
                signed_data = gpg.encrypt_file(signing, result.fingerprints,
                                               always_trust=True)
            with open(self.path, "w") as signed:
                signed.write(str(signed_data))
            # Upload newly encrypted file
            check_output(["rsync", self.path,
                          URL["upload"]])

            self.clear_window()

            label = Gtk.Label()
            label.set_markup("\n\n\t\tReport Sent Successfully!\t\t\n\n")
            label = self._set_default_margins(label)
            self.grid.attach(label, 1, 1, 2, 1)

            button1 = Gtk.Button.new_with_label("Okay!")
            button1.connect("clicked", self.main_menu)
            button1 = self._set_default_margins(button1)
            self.grid.attach(button1, 2, 2, 1, 1)

            self.show_all()

        except:
            self.clear_window()

            label = Gtk.Label()
            label.set_markup("""

\t\tReport Failed to Send!
\t\tPlease make sure you have a working internet connection.\t\t

""")
            label = self._set_default_margins(label)
            self.grid.attach(label, 1, 1, 2, 1)

            button1 = Gtk.Button.new_with_label("Okay")
            button1.connect("clicked", self.main_menu)
            button1 = self._set_default_margins(button1)
            self.grid.attach(button1, 2, 2, 1, 1)

            self.show_all()

    def preview_message(self, widget):
        """Preview Installation Report"""
        self.clear_window()
        with open(self.path, "r") as mail:
            text = mail.read()
        if len(text.split("\n")) > 36:
            self.scrolling = True
            self.set_default_size(775, 700)

            self.remove(self.grid)

            self.scrolled_window = Gtk.ScrolledWindow()
            self.scrolled_window.set_border_width(10)
            # there is always the scrollbar (otherwise: AUTOMATIC -
            # only if needed
            # - or NEVER)
            self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC,
                                            Gtk.PolicyType.AUTOMATIC)
            self.add(self.scrolled_window)
            # self.scrolled_window.add_with_viewport(self.grid)
            self.scrolled_window.add(self.grid)

        # self.text_buffer = Gtk.TextBuffer()

        # self.text_buffer.set_text(text, len(text))
        # self.custom_message = Gtk.TextView.new_with_buffer(self.text_buffer)
        # self.custom_message.set_editable(False)
        self.custom_message = Gtk.Label()
        self.custom_message.set_text(text)
        self.custom_message = self._set_default_margins(self.custom_message)
        self.grid.attach(self.custom_message, 1, 1, 4, 4)

        button1 = Gtk.Button.new_with_label("Send Report")
        button1.connect("clicked", self.send_report)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 4, 5, 1, 1)

        button2 = Gtk.Button.new_with_label("Abort")
        button2.connect("clicked", self.main_menu)
        button2 = self._set_default_margins(button2)
        self.grid.attach(button2, 1, 5, 1, 1)

        self.show_all()

    def generate_message(self):
        """write installation report to disk"""
        report_code = time.time()
        output = {}
        self.path = "/var/log/installation_report-%s.dosir" % (report_code)
        output['Installation Report Code'] = report_code
        try:
            output['system-installer Version'] = check_output(["system-installer", "-v"]).decode()
        except (FileNotFoundError, CalledProcessError):
            output['system-installer Version'] = "VERSION UNKNOWN. LIKELY TESTING OR MAJOR ERROR."
        output['OS'] = get_info(["lsb_release", "-ds"])[0]
        if self.cpu.get_active():
            output['CPU INFO'] = cpu_info()
        else:
            output['CPU INFO'] = 'OPT OUT'
        if self.gpu.get_active():
            output['PCIe / GPU INFO'] = get_info(["lspci", "-nnq"])
        else:
            output['PCIe / GPU INFO'] = 'OPT OUT'
        if self.ram.get_active():
            output['RAM / SWAP INFO'] = ram_info()
        else:
            output['RAM / SWAP INFO'] = 'OPT OUT'
        if self.disk.get_active():
            output['DISK SETUP'] = disk_info()
        else:
            output['DISK SETUP'] = 'OPT OUT'
        if self.log.get_active():
            try:
                with open("/tmp/system-installer.log", "r") as log:
                    output['INSTALLATION LOG'] = log.read().split("\n")
            except FileNotFoundError:
                output['INSTALLATION LOG'] = 'Log does not exist.'
        else:
            output['INSTALLATION LOG'] = 'OPT OUT'
        if self.custom.get_active():
            custom = self.text_buffer.get_text(self.text_buffer.get_start_iter(),
                                               self.text_buffer.get_end_iter(),
                                               False)
            # Make sure that custom messages are not the default message.
            # if they are, just put none so we don't see a bunch of
            # trash custom messages
            if custom == self.default_message:
                output['CUSTOM MESSAGE'] = "NONE"
            else:
                output['CUSTOM MESSAGE'] = custom
        else:
            output['CUSTOM MESSAGE'] = "NONE"
        try:
            with open(self.path, "w+") as message:
                json.dump(output, message, indent=1)
        except PermissionError:
            with open(getenv("HOME") + "/installation_report.txt", "w+") as message:
                json.dump(output, message, indent=1)

    def message_accept(self, widget):
        """Accept Message Input in GUI"""
        if self.custom.get_active():
            self.custom_setting = True
            self.text_buffer = Gtk.TextBuffer()
            self.text_buffer.set_text(self.default_message,
                                      len(self.default_message))
            self.custom_message = Gtk.TextView.new_with_buffer(self.text_buffer)
            self.custom_message.set_editable(True)
            self.custom_message.set_accepts_tab(True)
            self.custom_message = self._set_default_margins(self.custom_message)
            self.grid.attach(self.custom_message, 1, 8, 8, 4)

        else:
            self.grid.remove(self.custom_message)
            self.custom_setting = False

        self.show_all()

    def toggle_ui(self, widget, other):
        """UI to show if user opts in"""
        if self.opt.get_active():

            self.cpu = Gtk.CheckButton.new_with_label("CPU Info")
            self.cpu.set_active(self.cpu_setting)
            self.cpu.connect("toggled", self.cpu_toggle)
            self.cpu = self._set_default_margins(self.cpu)
            self.grid.attach(self.cpu, 2, 2, 2, 1)

            cpu_explain = Gtk.Button.new_from_icon_name("info", 3)
            cpu_explain.connect("clicked", self.cpu_explaination)
            cpu_explain = self._set_default_margins(cpu_explain)
            self.grid.attach(cpu_explain, 4, 2, 1, 1)

            self.gpu = Gtk.CheckButton.new_with_label("GPU/PCIe Info")
            self.gpu.set_active(self.gpu_setting)
            self.gpu.connect("toggled", self.gpu_toggle)
            self.gpu = self._set_default_margins(self.gpu)
            self.grid.attach(self.gpu, 2, 3, 2, 1)

            gpu_explain = Gtk.Button.new_from_icon_name("info", 3)
            gpu_explain.connect("clicked", self.gpu_explaination)
            gpu_explain = self._set_default_margins(gpu_explain)
            self.grid.attach(gpu_explain, 4, 3, 1, 1)

            self.ram = Gtk.CheckButton.new_with_label("RAM/SWAP Info")
            self.ram.set_active(self.ram_setting)
            self.ram.connect("toggled", self.ram_toggle)
            self.ram = self._set_default_margins(self.ram)
            self.grid.attach(self.ram, 2, 4, 2, 1)

            ram_explain = Gtk.Button.new_from_icon_name("info", 3)
            ram_explain.connect("clicked", self.ram_explaination)
            ram_explain = self._set_default_margins(ram_explain)
            self.grid.attach(ram_explain, 4, 4, 1, 1)

            self.disk = Gtk.CheckButton.new_with_label("Disk/Partitioning Info")
            self.disk.set_active(self.disk_setting)
            self.disk.connect("toggled", self.disk_toggle)
            self.disk = self._set_default_margins(self.disk)
            self.grid.attach(self.disk, 2, 5, 2, 1)

            disk_explain = Gtk.Button.new_from_icon_name("info", 3)
            disk_explain.connect("clicked", self.disk_explaination)
            disk_explain = self._set_default_margins(disk_explain)
            self.grid.attach(disk_explain, 4, 5, 1, 1)

            self.log = Gtk.CheckButton.new_with_label("Installation Log")
            self.log.set_active(self.log_setting)
            self.log.connect("toggled", self.log_toggle)
            self.log = self._set_default_margins(self.log)
            self.grid.attach(self.log, 2, 6, 2, 1)

            log_explain = Gtk.Button.new_from_icon_name("info", 3)
            log_explain.connect("clicked", self.log_explaination)
            log_explain = self._set_default_margins(log_explain)
            self.grid.attach(log_explain, 4, 6, 1, 1)

            self.custom = Gtk.CheckButton.new_with_label("Custom Message")
            self.custom.set_active(self.custom_setting)
            self.custom.connect("toggled", self.message_accept)
            self.custom = self._set_default_margins(self.custom)
            self.grid.attach(self.custom, 2, 7, 2, 1)

            if hasattr(self, 'text_buffer'):
                self.grid.attach(self.custom_message, 1, 8, 8, 4)

            button2 = Gtk.Button.new_with_label("Preview Message")
            button2.connect("clicked", self.message_handler)
            button2 = self._set_default_margins(button2)
            self.grid.attach(button2, 5, 12, 4, 1)

            self.show_all()

        else:
            self.main("clicked")

    def main(self, widget):
        """Opt in Window for Installation Report"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
        Send installation and hardware report\t""")
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 3, 1)

        self.opt = Gtk.Switch()
        self.opt.set_state(self.opt_setting)
        self.opt.connect("state-set", self.toggle_ui)
        self.opt = self._set_default_margins(self.opt)
        self.grid.attach(self.opt, 5, 1, 1, 1)

        button1 = Gtk.Button.new_with_label("<-- Back")
        button1.connect("clicked", self.main_menu)
        button1 = self._set_default_margins(button1)
        self.grid.attach(button1, 1, 12, 1, 1)

        self.show_all()


def cpu_info():
    """get CPU info"""
    info = check_output("lscpu").decode().split("\n")
    # We need to create a more intelligent parser for this data as positions can
    # change depending on the system that is being used.
    sentenal = 0
    output = []
    backup_speed = None
    count = 0
    while sentenal < 7:
        for each in info:
            if sentenal == 0:
                if "Model name:" in each:
                    output.append(each)
                    sentenal += 1
            elif sentenal == 1:
                if "Thread(s) per core:" in each:
                    output.append(each)
                    sentenal += 1
            elif sentenal == 2:
                if "Core(s) per socket:" in each:
                    output.append(each)
                    sentenal += 1
            elif sentenal == 3:
                if "CPU max MHz:" in each:
                    output.append(each)
                    sentenal += 1
                    count = 0
                elif count == len(info):
                    count = 0
                    sentenal += 1
                    output.append("CPU max MHz:\t\t\tUnknown")
                else:
                    count += 1
            elif sentenal == 4:
                if "L2 cache:" in each:
                    output.append(each)
                    sentenal += 1
                    count = 0
                elif count == len(info):
                    count = 0
                    sentenal += 1
                    output.append("L2 cache:\t\t\tUnknown")
                else:
                    count += 1
            elif sentenal == 5:
                if "L3 cache:" in each:
                    output.append(each)
                    sentenal += 1
                    count = 0
                elif count == len(info):
                    count = 0
                    sentenal += 1
                    output.append("L3 cache:\t\t\tUnknown")
                else:
                    count += 1
            elif sentenal == 6:
                if "CPU MHz:" in each:
                    backup_speed = each
                    sentenal += 1
                    count = 0
                elif count == len(info):
                    count = 0
                    sentenal += 1
                    backup_speed = "Unknown"
                else:
                    count += 1
    speed_dir = "/sys/devices/system/cpu/cpu0/cpufreq/"
    if path.exists(speed_dir):
        if path.exists(speed_dir + "bios_limit"):
            with open(speed_dir + "bios_limit", "r") as file:
                speed = int(file.read()) / 1000
        else:
            with open(speed_dir + "scaling_max_freq", "r") as file:
                speed = int(file.read()) / 1000
    else:
        speed = backup_speed
    speed = f"CPU base MHz                     { speed }"
    output.insert(3, speed)
    return "\n".join(output)


def ram_info():
    """Get RAM info"""
    ram_capacity = check_output(["lsmem", "--summary=only"]).decode().split("\n")
    swap_capacity = check_output(["swapon", "--show"]).decode().split("\n")
    return {"RAM": ram_capacity, "SWAP": swap_capacity}


def disk_info():
    """Get disk info"""
    info = json.loads(check_output(["lsblk", "--json", "--output",
                                    "name,size,type,mountpoint"]).decode())
    for each in range(len(info["blockdevices"]) - 1, -1, -1):
        if "loop" == info["blockdevices"][each]["type"]:
            del info["blockdevices"][each]
    return info["blockdevices"]


def get_info(cmd):
    """Get arbitrary info from commands"""
    info = check_output(cmd).decode()
    if info[-1] == "\n":
        info = list(info)
        del info[-1]
        info = "".join(info)
    info = info.split("\n")
    return info


def send_to():
    try:
        return json.loads("/etc/system-installer/settings.json")["report_to"]
    except (FileNotFoundError, PermissionError, KeyError):
        return "installation-reports@draugeros.org"
