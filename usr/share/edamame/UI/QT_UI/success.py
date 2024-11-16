#!shebang
# -*- coding: utf-8 -*-
#
#  success.py
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
"""Success Reporting UI"""
from shutil import rmtree, copytree, move, copyfile
import subprocess
import os
import sys
import json
import pathlib
import xmltodict
import tarfile as tar
import urllib.parse as urlp
from qtpy import QtGui, QtWidgets, QtCore
try:
    from UI.QT_UI import report
except ImportError:
    try:
        from QT_UI import report
    except ImportError:
        import report
import common
try:
    import UI.QT_UI.qt_common as QCommon
except ImportError:
    import qt_common as QCommon


class Main(report.Main):
    """Success UI Class"""
    def __init__(self, settings):
        """Initialize data"""
        super().__init__()
        self.settings = settings

        try:
            with open("/etc/edamame/settings.json", "r") as file:
                self.distro = json.load(file)["distro"]
        except (FileNotFoundError, KeyError):
            self.distro = "Linux"
        self.main_menu("clicked")

    def _set_default_margins(self, widget):
        """Set default margin size"""
        try:
            margin = QtCore.QMargins(10, 10, 10, 10)
            widget.setContentsMargins(margin)
        except AttributeError:
            common.eprint("WARNING: QtCore.QMargins() does not exist. Spacing in UI might be a bit wonky.")
        return widget

    def main_menu(self, widget):
        """Main Success Window"""
        self.clear_window()

        text = """
## %s has been successfully installed on your computer!\n
""" % (self.distro)
        if "OEM" not in self.settings.values():
            text = text + """Please consider sending an installation report to our team,\n
using the "Send Installation Report" button below.\t\n\n"""
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 4)

        if "OEM" in self.settings.values():
            button1 = QtWidgets.QPushButton("Power Off System")
            button1.clicked.connect(__poweroff__)
        else:
            button1 = QtWidgets.QPushButton("Restart System")
            button1.clicked.connect(__reboot__)
        button1 = self._set_default_margins(button1)
        if "OEM" in self.settings.values():
            self.grid.addWidget(button1, 6, 4, 1, 1)
        else:
            self.grid.addWidget(button1, 6, 2, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        button2 = self._set_default_margins(button2)
        if "OEM" in self.settings.values():
            self.grid.addWidget(button2, 6, 1, 1, 2)
        else:
            self.grid.addWidget(button2, 6, 1, 1, 1)

        if "OEM" not in self.settings.values():
            button3 = QtWidgets.QPushButton("Advanced")
            button3.clicked.connect(self.onadvclicked)
            button3 = self._set_default_margins(button3)
            self.grid.addWidget(button3, 6, 3, 1, 1)

            button4 = QtWidgets.QPushButton("Send Installation Report")
            button4.clicked.connect(self.main)
            button4 = self._set_default_margins(button4)
            self.grid.addWidget(button4, 6, 4, 1, 1)

    def onadvclicked(self, button):
        """Advanced Settings and Functions"""
        self.clear_window()

        label = QtWidgets.QLabel("""
The below options are meant exclusivly for advanced users.\n\n
**User discretion is advised.**\n\n
 """)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        button1 = QtWidgets.QPushButton("Dump Settings to File")
        button1.clicked.connect(self.dump_settings_dialog)
        button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 6, 3, 1, 1)

        button2 = QtWidgets.QPushButton("Delete Installation")
        button2.clicked.connect(self.ondeletewarn)
        button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 6, 1, 1, 1)

        button4 = QtWidgets.QPushButton("Exit")
        button4.clicked.connect(self.exit)
        button4 = self._set_default_margins(button4)
        self.grid.addWidget(button4, 7, 3, 1, 1)

        button5 = QtWidgets.QPushButton("<-- Back")
        button5.clicked.connect(self.main_menu)
        button5 = self._set_default_margins(button5)
        self.grid.addWidget(button5, 7, 1, 1, 1)

    def ondeletewarn(self, button):
        """Warning about Deleting the installation"""
        self.clear_window()

        label = QtWidgets.QLabel("""
\tAre you sure you wish to delete the new installation?\t\n
\tNo data will be recoverable.\t
""")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 3)

        button5 = QtWidgets.QPushButton("DELETE")
        button5.clicked.connect(self.delete_install)
        button5 = self._set_default_margins(button5)
        self.grid.addWidget(button5, 2, 2, 1, 1)

        button4 = QtWidgets.QPushButton("Exit")
        button4.clicked.connect(self.exit)
        button4 = self._set_default_margins(button4)
        self.grid.addWidget(button4, 2, 3, 1, 1)

        button6 = QtWidgets.QPushButton("<-- Back")
        button6.clicked.connect(self.onadvclicked)
        button6 = self._set_default_margins(button6)
        self.grid.addWidget(button6, 2, 1, 1, 1)

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

    def exit(self, button):
        """Exit"""
        self.close()
        return 0

    def clear_window(self):
        """Clear Window"""
        for i in range(self.grid.count() - 1, -1, -1):
            self.grid.itemAt(i).widget().setParent(None)


    def dump_settings_dialog(self, button):
        """Get what to dump and what not to dump"""
        self.clear_window()

        label = QtWidgets.QLabel("""
\tSelect what you would like included in your Quick Install file.\t
""")
        label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 4)

        self.settings_toggle = QtWidgets.QCheckBox("Installation Settings")
        self.settings_toggle.setChecked(True)
        self.settings_toggle = self._set_default_margins(self.settings_toggle)
        self.grid.addWidget(self.settings_toggle, 2, 1, 1, 4)

        self.network_toggle = QtWidgets.QCheckBox("Network Settings")
        self.network_toggle.setChecked(True)
        self.network_toggle = self._set_default_margins(self.network_toggle)
        self.grid.addWidget(self.network_toggle, 3, 1, 1, 4)

        self.wall_toggle = QtWidgets.QCheckBox("Wallpaper")
        self.wall_toggle.setChecked(False)
        self.wall_toggle = self._set_default_margins(self.wall_toggle)
        self.grid.addWidget(self.wall_toggle, 4, 1, 1, 4)

        button4 = QtWidgets.QPushButton("Exit")
        button4.clicked.connect(self.exit)
        button4 = self._set_default_margins(button4)
        self.grid.addWidget(button4, 6, 4, 1, 1)

        button5 = QtWidgets.QPushButton("<-- Back")
        button5.clicked.connect(self.onadvclicked)
        button5 = self._set_default_margins(button5)
        self.grid.addWidget(button5, 6, 1, 1, 1)

        button3 = QtWidgets.QPushButton("DUMP")
        button3.clicked.connect(self.dump_settings_file_dialog)
        button3 = self._set_default_margins(button3)
        self.grid.addWidget(button3, 5, 1, 1, 4)

    def dump_settings_file_dialog(self, button):
        """Dump Settings File Dialog"""
        filter = None
        try:
            if (self.network_toggle.isChecked() or self.wall_toggle.isChecked()):
                filter = ["application/x-tar"]
            else:
                filter = ["application/json"]
        except NameError:
            filter = ["application/json"]


        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(os.getenv("HOME"))
        dialog.setMimeTypeFilters(filter)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dialog.exec()
        response = dialog.selectedFiles()[0]

        if response != "":
            if self.network_toggle.isChecked():
                if response[-3:] != ".xz":
                    response = f"{response}.xz"
                adv_dump_settings(self.settings, response,
                                  copy_net=self.network_toggle.isChecked(),
                                  copy_set=self.settings_toggle.isChecked(),
                                  copy_wall=self.wall_toggle.isChecked())
            else:
                dump_settings(self.settings, response)

        # dialog.close()
        self.onadvclicked("clicked")


def dump_settings(settings, path):
    """Dump Settings to File"""
    with open(path, "w+") as dump_file:
        json.dump(settings, dump_file, indent=2)


def adv_dump_settings(settings, dump_path, copy_net=True, copy_set=True,
                      copy_wall=False):
    """Compress Install settings and
       Network settings to tar bar for later use
    """
    # Make our directory layout
    try:
        os.mkdir("/tmp/working_dir")
    except FileExistsError:
        pass
    try:
        os.mkdir("/tmp/working_dir/settings")
    except FileExistsError:
        pass
    try:
        os.mkdir("/tmp/working_dir/assets")
    except FileExistsError:
        pass
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
        wall_path_unique = common.unique(wall_path)
        # Copy designated files into "assets"
        if len(wall_path_unique) == 1:
            # we only have one wallpaper, so copy that into assets/master
            # then, dump the list of screens to assets/screens.list
            # when read in, this will make it so that the wallpaper is used on
            # all the same screens as before
            try:
                os.mkdir("/tmp/working_dir/assets/master")
            except FileExistsError:
                pass
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
                try:
                    os.mkdir("/tmp/working_dir/assets/" + monitors[each])
                except FileExistsError:
                    pass
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


def show_success(settings):
    """Show Success UI"""
    app = QtWidgets.QApplication([sys.argv[0]])
    window = Main(settings)
    window = QCommon.set_window_nonresizeable(window)
    # window.set_resizable(False)
    # window.set_position(Gtk.WindowPosition.CENTER)
    window.show()
    app.exec()


def __reboot__(button):
    """Reboot the system"""
    subprocess.Popen(["/sbin/reboot"])
    sys.exit(0)


def __poweroff__(button):
    """Shutdown the system"""
    subprocess.Popen(["/sbin/poweroff"])
    sys.exit(0)


if __name__ == '__main__':
    settings = json.loads(sys.argv[1])
    show_success(settings)
