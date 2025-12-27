#!shebang
# -*- coding: utf-8 -*-
#
#  report.py
#
#  Copyright 2025 Thomas Castleman <batcastle@draugeros.org>
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
from subprocess import check_output, CalledProcessError
from os import getenv, path
from shutil import copyfile
import time
import json
import gnupg
from qtpy import QtGui, QtWidgets, QtCore
import urllib3
import common

try:
    gpg = gnupg.GPG(gnupghome="/home/live/.gnupg")
except ValueError:
    try:
        gpg = gnupg.GPG(gnupghome=getenv("HOME") + "/.gnupg")
    except ValueError:
        gpg = gnupg.GPG(gnupghome="/home/drauger-user/.gnupg")


class Main(QtWidgets.QWidget):
    """Main UI and tools for reporting installations"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edamame")
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.setWindowIcon(QtGui.QIcon.fromTheme("system-installer"))
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
        for i in range(self.grid.count() - 1, -1, -1):
            self.grid.itemAt(i).widget().setParent(None)

    def _set_default_margins(self, widget):
        """Set default margin size"""
        try:
            margin = QtCore.QMargins(10, 10, 10, 10)
            widget.setContentsMargins(margin)
        except AttributeError:
            common.eprint("WARNING: QtCore.QMargins() does not exist. Spacing in UI might be a bit wonky.")
        return widget

    def cpu_toggle(self, widget):
        """Toggle sending CPU info"""
        if widget:
            self.cpu_setting = True
        else:
            self.cpu_setting = False

    def cpu_explaination(self, widget):
        """Explain why we need CPU info"""
        self.clear_window()

        label = QtWidgets.QLabel()
        label.setText("""
    **Why to report CPU info**\t""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label1 = QtWidgets.QLabel("""
    Knowing what CPUs most of our users use helps us to optimize Drauger OS.
    It allows us to know if we have more or less CPU cores to take
    advantage of, or if we need to focus on becoming even lighter weight.

    It also gives us valuable information such as CPU vulnerabilities that are
    common among our users. Knowing this helps us decide if we need to keep \t
    certain security measures enabled, or if we can disable some for better
    performance with little to no risk to security.
    \t""")
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 2)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.main)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 12, 1, 1, 1)

    def gpu_toggle(self, widget):
        """Toggle sending GPU/PCIe info"""
        if widget:
            self.gpu_setting = True
        else:
            self.gpu_setting = False

    def gpu_explaination(self, widget):
        """Explain why we need GPU/PCIe info"""
        self.clear_window()

        label = QtWidgets.QLabel("""
    **Why to report GPU / PCIe info**\t""")
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label1 = QtWidgets.QLabel("""
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
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 2)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.main)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 12, 1, 1, 1)

    def ram_toggle(self, widget):
        """Toggle sending RAM info"""
        if widget:
            self.ram_setting = True
        else:
            self.ram_setting = False

    def ram_explaination(self, widget):
        """Explain why we need RAM info"""
        self.clear_window()

        label = QtWidgets.QLabel("""
    **Why to report RAM/SWAP info**\t""")
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label1 = QtGui.QLabel("""
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
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 2)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.main)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 12, 1, 1, 1)

    def disk_toggle(self, widget):
        """Toggle Sending Disk Info"""
        if widget:
            self.disk_setting = True
        else:
            self.disk_setting = False

    def disk_explaination(self, widget):
        """Explain why we need Disk Info"""
        self.clear_window()

        label = QtWidgets.QLabel("""
    **Why to report Disk and Partitioning info**\t""")
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label1 = QtWidgets.QLabel("""
    Understanding our users partitioning and disk setups helps us know
    if our users are dual-booting Drauger OS. This, in turn with the added
    benefit of knowing immediatly whether our users are using the automatic\t
    or manual partitioning systems tells us where to focus our effort.

    This can mean we are more likely to catch bugs or add new features
    in one area or another.
    \t""")
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 2)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.main)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 12, 1, 1, 1)

    def log_toggle(self, widget):
        """Toggle sending the log"""
        if widget:
            self.log_setting = True
        else:
            self.log_setting = False

    def log_explaination(self, widget):
        """Explaination for why we need the installation log"""
        self.clear_window()

        label = QtWidgets.QLabel("""
    **Why to send the Installation Log**\t""")
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 2)

        label1 = QtWidgets.QLabel("""
    As soon as the installation of Drauger OS completed, the installation log
    was copied to your internal drive.

    Normally, if you have a bug that might be related to the installer, we
    would ask you to send us that log. By sending it now, we don't have to do
    that. Instead, we can give you a command to run in your terminal. The
    output of that command will tell us which installation log is yours
    so we can immediatly access it and track down bugs.

    <b>If you send nothing else, please send this.</b>
    \t""")
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 2)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.main)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 12, 1, 1, 1)

    def exit(self, button):
        """Exit"""
        self.close()
        return 1

    def message_handler(self, widget):
        """Generate Message then show it"""
        self.generate_message()
        self.preview_message("clicked")

    def send_report(self, widget):
        """Send installation Report"""
        self.clear_window()

        label = QtWidgets.QLabel("\n\n\t\tSending Report. Please Wait . . .\t\t\n\n")
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 1)


        try:
            copyfile(self.path, "/mnt/var/log/installation_report.txt")
        except:
            pass

        try:
            # Get keys
            http = urllib3.PoolManager()
            with open("/etc/edamame/settings.json",
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

            label = QtWidgets.QLabel("\n\n\t\tReport Sent Successfully!\t\t\n\n")
            label.setTextFormat(QtCore.Qt.MarkdownText)
            label = self._set_default_margins(label)
            self.grid.addWidget(label, 1, 1, 1, 2)

            button1 = QtWidgets.QPushButton("Okay!")
            button1.clicked.connect(self.main_menu)
            button1 = self._set_default_margins(button1)
            self.grid.addWidget(button1, 2, 2, 1, 1)

        except:
            self.clear_window()

            label = QtWidgets.QLabel("""

\t\tReport Failed to Send!
\t\tPlease make sure you have a working internet connection.\t\t

""")
            label.setTextFormat(QtCore.Qt.MarkdownText)
            label = self._set_default_margins(label)
            self.grid.addWidget(label, 1, 1, 1, 2)

            button1 = QtWidgets.QPushButton("Okay")
            button1.clicked.connect(self.main_menu)
            button1 = self._set_default_margins(button1)
            self.grid.addWidget(button1, 2, 2, 1, 1)

    def preview_message(self, widget):
        """Preview Installation Report"""
        self.clear_window()
        try:
            with open(self.path, "r") as mail:
                text = mail.read()
        except FileNotFoundError:
            # this is handled during file generation, so this should never be used
            path = getenv("HOME") + "/installation_report.txt"
            with open(path) as mail:
                text = mail.read()

        self.custom_message = QtWidgets.QTextEdit()
        self.custom_message.setPlainText(json.dumps(json.loads(text), indent=2))
        self.custom_message.setReadOnly(True)
        self.custom_message.setAcceptRichText(False)
        self.custom_message.setCursorWidth(0)
        self.custom_message = self._set_default_margins(self.custom_message)
        self.grid.addWidget(self.custom_message, 1, 1, 4, 4)

        button1 = QtWidgets.QPushButton("Send Report")
        button1.clicked.connect(self.send_report)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 5, 4, 1, 1)

        button2 = QtWidgets.QPushButton("Abort")
        button2.clicked.connect(self.main_menu)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 5, 1, 1, 1)

    def generate_message(self):
        """write installation report to disk"""
        report_code = time.time()
        output = {}
        self.path = f"/tmp/installation_report-{ report_code }.dosir"
        output['Installation Report Code'] = report_code
        try:
            ver = check_output(["edamame", "-v"]).decode().split("\n")
            ver = [each for each in ver if each != ""][0]
            output['edamame Version'] = ver
        except (FileNotFoundError, CalledProcessError):
            output['edamame Version'] = "VERSION UNKNOWN. LIKELY TESTING OR MAJOR ERROR."
        output['OS'] = get_info(["lsb_release", "-ds"])[0]
        if self.cpu.isChecked():
            output['CPU INFO'] = cpu_info()
        else:
            output['CPU INFO'] = 'OPT OUT'
        if self.gpu.isChecked():
            output['PCIe / GPU INFO'] = get_info(["lspci", "-nnq"])
        else:
            output['PCIe / GPU INFO'] = 'OPT OUT'
        if self.ram.isChecked():
            output['RAM / SWAP INFO'] = ram_info()
        else:
            output['RAM / SWAP INFO'] = 'OPT OUT'
        if self.disk.isChecked():
            output['DISK SETUP'] = disk_info()
        else:
            output['DISK SETUP'] = 'OPT OUT'
        if self.log.isChecked():
            try:
                with open("/tmp/edamame.log", "r") as log:
                    output['INSTALLATION LOG'] = log.read().split("\n")
            except FileNotFoundError:
                output['INSTALLATION LOG'] = 'Log does not exist.'
        else:
            output['INSTALLATION LOG'] = 'OPT OUT'
        if self.custom.isChecked():
            custom = self.text_buffer.toPlainText()
            # Make sure that custom messages are not the default message.
            # if they are, just put none so we don't see a bunch of
            # trash custom messages
            if custom == self.default_message:
                output['CUSTOM MESSAGE'] = "NONE"
            else:
                output['CUSTOM MESSAGE'] = custom.split("\n")
        else:
            output['CUSTOM MESSAGE'] = "NONE"
        try:
            with open(self.path, "w+") as message:
                json.dump(output, message, indent=1)
        except PermissionError:
            self.path = getenv("HOME") + "/installation_report.txt"
            with open(self.path, "w+") as message:
                json.dump(output, message, indent=1)

    def message_accept(self, widget):
        """Accept Message Input in GUI"""
        if self.custom.isChecked():
            self.custom_setting = True
            self.text_buffer = QtWidgets.QTextEdit()
            self.text_buffer.setText(self.default_message)
            self.text_buffer.setReadOnly(False)
            self.text_buffer.setTabChangesFocus(False)
            self.text_buffer = self._set_default_margins(self.text_buffer)
            self.grid.addWidget(self.text_buffer, 8, 1, 4, 8)

        else:
            self.grid.remove(self.text_buffer)
            self.custom_setting = False
            del self.text_buffer

    def main(self, widget):
        """UI to show if user opts in"""
        self.clear_window()

        label = QtWidgets.QLabel("""
Send installation and hardware report\t""")
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        self.cpu = QtWidgets.QCheckBox("CPU Info")
        self.cpu.setChecked(self.cpu_setting)
        self.cpu.toggled.connect(self.cpu_toggle)
        self.cpu = self._set_default_margins(self.cpu)
        self.grid.addWidget(self.cpu, 2, 2, 1, 2)

        cpu_explain = QtWidgets.QPushButton()
        cpu_explain.setIcon(QtGui.QIcon.fromTheme("help-about"))
        # cpu_explain.setIconSize(QtCore.QSize(3, 3))
        cpu_explain.clicked.connect(self.cpu_explaination)
        cpu_explain = self._set_default_margins(cpu_explain)
        self.grid.addWidget(cpu_explain, 2, 4, 1, 1)

        self.gpu = QtWidgets.QCheckBox("GPU/PCIe Info")
        self.gpu.setChecked(self.gpu_setting)
        self.gpu.toggled.connect(self.gpu_toggle)
        self.gpu = self._set_default_margins(self.gpu)
        self.grid.addWidget(self.gpu, 3, 2, 1, 2)

        gpu_explain = QtWidgets.QPushButton()
        gpu_explain.setIcon(QtGui.QIcon.fromTheme("help-about"))
        # gpu_explain.setIconSize(QtCore.QSize(3, 3))
        gpu_explain.clicked.connect(self.gpu_explaination)
        gpu_explain = self._set_default_margins(gpu_explain)
        self.grid.addWidget(gpu_explain, 3, 4, 1, 1)

        self.ram = QtWidgets.QCheckBox("RAM/SWAP Info")
        self.ram.setChecked(self.ram_setting)
        self.ram.toggled.connect(self.ram_toggle)
        self.ram = self._set_default_margins(self.ram)
        self.grid.addWidget(self.ram, 4, 2, 1, 2)

        ram_explain = QtWidgets.QPushButton()
        ram_explain.setIcon(QtGui.QIcon.fromTheme("help-about"))
        # ram_explain.setIconSize(QtCore.QSize(3, 3))
        ram_explain.clicked.connect(self.ram_explaination)
        ram_explain = self._set_default_margins(ram_explain)
        self.grid.addWidget(ram_explain, 4, 4, 1, 1)

        self.disk = QtWidgets.QCheckBox("Disk/Partitioning Info")
        self.disk.setChecked(self.disk_setting)
        self.disk.toggled.connect(self.disk_toggle)
        self.disk = self._set_default_margins(self.disk)
        self.grid.addWidget(self.disk, 5, 2, 1, 2)

        disk_explain = QtWidgets.QPushButton()
        disk_explain.setIcon(QtGui.QIcon.fromTheme("help-about"))
        # disk_explain.setIconSize(QtCore.QSize(3, 3))
        disk_explain.clicked.connect(self.disk_explaination)
        disk_explain = self._set_default_margins(disk_explain)
        self.grid.addWidget(disk_explain, 5, 4, 1, 1)

        self.log = QtWidgets.QCheckBox("Installation Log")
        self.log.setChecked(self.log_setting)
        self.log.toggled.connect(self.log_toggle)
        self.log = self._set_default_margins(self.log)
        self.grid.addWidget(self.log, 6, 2, 1, 2)

        log_explain = QtWidgets.QPushButton()
        log_explain.setIcon(QtGui.QIcon.fromTheme("help-about"))
        # log_explain.setIconSize(QtCore.QSize(3, 3))
        log_explain.clicked.connect(self.log_explaination)
        log_explain = self._set_default_margins(log_explain)
        self.grid.addWidget(log_explain, 6, 4, 1, 1)

        self.custom = QtWidgets.QCheckBox("Custom Message")
        self.custom.setChecked(self.custom_setting)
        self.custom.toggled.connect(self.message_accept)
        self.custom = self._set_default_margins(self.custom)
        self.grid.addWidget(self.custom, 7, 2, 1, 2)

        if hasattr(self, 'text_buffer'):
            self.grid.addWidget(self.text_buffer, 8, 1, 4, 8)

        button2 = QtWidgets.QPushButton("Preview Message")
        button2.clicked.connect(self.message_handler)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 12, 5, 1, 4)

        button1 = QtWidgets.QPushButton("<-- Back")
        button1.clicked.connect(self.main_menu)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 12, 1, 1, 1)


def cpu_info():
    """get CPU info"""
    info = check_output("lscpu").decode().split("\n")
    # We need to create a more intelligent parser for this data as positions can
    # change depending on the system that is being used.
    sentenal = 0
    output = {}
    backup_speed = None
    count = 0
    while sentenal < 7:
        for each in info:
            if sentenal == 0:
                if "Model name:" in each:
                    add = [each1 for each1 in each.split("  ") if each1 != ""]
                    if add[0][-1] == ":":
                        add[0] = add[0][:-1]
                    output[add[0]] = add[1]
                    sentenal += 1
            elif sentenal == 1:
                if "Thread(s) per core:" in each:
                    add = [each1 for each1 in each.split("  ") if each1 != ""]
                    if add[0][-1] == ":":
                        add[0] = add[0][:-1]
                    output[add[0]] = int(add[1])
                    sentenal += 1
            elif sentenal == 2:
                if "Core(s) per socket:" in each:
                    add = [each1 for each1 in each.split("  ") if each1 != ""]
                    if add[0][-1] == ":":
                        add[0] = add[0][:-1]
                    output[add[0]] = int(add[1])
                    sentenal += 1
            elif sentenal == 3:
                if "CPU max MHz:" in each:
                    add = [each1 for each1 in each.split("  ") if each1 != ""]
                    if add[0][-1] == ":":
                        add[0] = add[0][:-1]
                    output[add[0]] = float(add[1])
                    sentenal += 1
                    count = 0
                elif count == len(info):
                    count = 0
                    sentenal += 1
                    output["CPU max MHz"] = "Unknown"
                else:
                    count += 1
            elif sentenal == 4:
                if "L2 cache:" in each:
                    add = [each1 for each1 in each.split("  ") if each1 != ""]
                    if add[0][-1] == ":":
                        add[0] = add[0][:-1]
                    output[add[0]] = add[1]
                    sentenal += 1
                    count = 0
                elif count == len(info):
                    count = 0
                    sentenal += 1
                    output["L2 cache"] = "Unknown"
                else:
                    count += 1
            elif sentenal == 5:
                if "L3 cache:" in each:
                    add = [each1 for each1 in each.split("  ") if each1 != ""]
                    if add[0][-1] == ":":
                        add[0] = add[0][:-1]
                    output[add[0]] = add[1]
                    sentenal += 1
                    count = 0
                elif count == len(info):
                    count = 0
                    sentenal += 1
                    output["L3 cache"] = "Unknown"
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
    # speed = float(speed)
    output["CPU base MHz"] = speed
    return output


def ram_info():
    """Get RAM info"""
    ram_capacity = check_output(["lsmem", "--summary=only"]).decode().split("\n")
    for each in enumerate(ram_capacity):
        ram_capacity[each[0]] = [each1 for each1 in each[1].split("  ") if each1 != ""]
    for each in range(len(ram_capacity) - 1, -1, -1):
        if ram_capacity[each] == []:
            del ram_capacity[each]
    swap_capacity = check_output(["swapon", "--show"]).decode().split("\n")
    return {"RAM": dict(ram_capacity), "SWAP": swap_capacity}


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
