#!shebang
# -*- coding: utf-8 -*-
#
#  confirm.py
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
"""Confirm UI for Edamame"""
from __future__ import print_function
import sys
import json
from qtpy import QtGui, QtWidgets, QtCore
try:
    import UI.Qt_UI.qt_common as QCommon
except ImportError:
    import qt_common as QCommon
import auto_partitioner as ap


class Main(QtWidgets.QWidget):
    """UI Confirmation Class"""

    def __init__(self, settings):
        """set up confirmation UI"""
        super().__init__()
        self.setWindowTitle("Edamame")
        self.install = False
        self.setWindowIcon(QtGui.QIcon.fromTheme("system-installer"))
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        label = QtWidgets.QLabel()
        label.setText("""
# FINAL CONFIRMATION
## Please read the below summary carefully.\n
## This is your final chance to cancel installation.\n
---
        """)
        label.setTextFormat(QtCore.Qt.MarkdownText)
        label.setAlignment(QtCore.Qt.AlignCenter)
        # label = self._set_default_margins(label)
        self.grid.addWidget(label, 1, 1, 1, 11)

        label1 = QtWidgets.QLabel()
        label1.setTextFormat(QtCore.Qt.MarkdownText)
        label1.setText("""
### PARTITIONS
        """)
        label1.setAlignment(QtCore.Qt.AlignCenter)
        # label1 = self._set_default_margins(label1)
        self.grid.addWidget(label1, 2, 1, 1, 2)

        label5 = QtWidgets.QLabel()
        label5.setTextFormat(QtCore.Qt.MarkdownText)

        if settings["AUTO_PART"]:
            label = f"""**AUTO PARTITIONING ENABLED**\t

**INSTALLATION DRIVE:** {settings["ROOT"]}"""
            if settings["raid_array"]["raid_type"] not in ("OEM", None):
                label = label + f"""

**RAID Type:** {settings["raid_array"]["raid_type"]}

**Drive 1:**   {settings["raid_array"]["disks"]["1"]}

**Drive 2:**   {settings["raid_array"]["disks"]["2"]}"""
                if settings["raid_array"]["raid_type"].lower() == "raid10":
                    label = label + f"""

**Drive 3:**   {settings["raid_array"]["disks"]["3"]}

**Drive 4:**   {settings["raid_array"]["disks"]["4"]}"""
            else:
                label = label + f"""
**HOME:**      {settings["HOME"]}"""
        else:
            label = f"""**ROOT:**       {settings["ROOT"]}

**EFI:**       {settings["EFI"]}

**SWAP:**      {settings["SWAP"]}

**HOME:**     {settings["HOME"]}"""

        label5.setText(label)
        label5.setAlignment(QtCore.Qt.AlignCenter)
        # label5 = self._set_default_margins(label5)
        self.grid.addWidget(label5, 3, 1, round(len(label.split("\n")) / 2), 2)

        if "OEM" not in settings.values():
            # Attach the same separator in multiple places
            # sep = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
            # self.grid.addWidget(sep, 3, 2, 1, 6)

            label6 = QtWidgets.QLabel()
            label6.setTextFormat(QtCore.Qt.MarkdownText)
            label6.setText("""
### SYSTEM
        """)
            label6.setAlignment(QtCore.Qt.AlignCenter)
            # label6 = self._set_default_margins(label6)
            self.grid.addWidget(label6, 2, 4, 1, 2)

            label7 = QtWidgets.QLabel()
            label7.setTextFormat(QtCore.Qt.MarkdownText)
            label7.setText("""  **Language:**   """)
            label7.setAlignment(QtCore.Qt.AlignCenter)
            # label7 = self._set_default_margins(label7)
            self.grid.addWidget(label7, 3, 4, 1, 1)

            label8 = QtWidgets.QLabel()
            label8.setTextFormat(QtCore.Qt.MarkdownText)
            label8.setText(settings["LANG"])
            label8.setAlignment(QtCore.Qt.AlignCenter)
            # label8 = self._set_default_margins(label8)
            self.grid.addWidget(label8, 3, 5, 1, 1)

            label9 = QtWidgets.QLabel()
            label9.setTextFormat(QtCore.Qt.MarkdownText)
            label9.setText("""  **Time Zone:**  """)
            label9.setAlignment(QtCore.Qt.AlignCenter)
            # label9 = self._set_default_margins(label9)
            self.grid.addWidget(label9, 4, 4, 1, 1)

            label10 = QtWidgets.QLabel()
            label10.setTextFormat(QtCore.Qt.MarkdownText)
            label10.setText(settings["TIME_ZONE"])
            label10.setAlignment(QtCore.Qt.AlignCenter)
            # label10 = self._set_default_margins(label10)
            self.grid.addWidget(label10, 4, 5, 1, 1)

            label11 = QtWidgets.QLabel()
            label11.setTextFormat(QtCore.Qt.MarkdownText)
            label11.setText("   **Computer Name:**  ")
            label11.setAlignment(QtCore.Qt.AlignCenter)
            # label11 = self._set_default_margins(label11)
            self.grid.addWidget(label11, 5, 4, 1, 1)

            label12 = QtWidgets.QLabel()
            label12.setTextFormat(QtCore.Qt.MarkdownText)
            label12.setText(settings["COMPUTER_NAME"])
            label12.setAlignment(QtCore.Qt.AlignCenter)
            # label12 = self._set_default_margins(label12)
            self.grid.addWidget(label12, 5, 5, 1, 1)

            if ap.is_EFI():
                label31 = QtWidgets.QLabel()
                label31.setTextFormat(QtCore.Qt.MarkdownText)
                label31.setText("   **Compatibility Mode:**  ")
                label31.setAlignment(QtCore.Qt.AlignCenter)
                # label31 = self._set_default_margins(label31)
                self.grid.addWidget(label31, 6, 4, 1, 1)

                label32 = QtWidgets.QLabel()
                label32.setTextFormat(QtCore.Qt.MarkdownText)
                label32.setText(str(settings["COMPAT_MODE"]))
                label32.setAlignment(QtCore.Qt.AlignCenter)
                # label32 = self._set_default_margins(label32)
                self.grid.addWidget(label32, 6, 5, 1, 1)

            # sep1 = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
            # self.grid.addWidget(sep1, 6, 2, 1, 6)

            label13 = QtWidgets.QLabel()
            label13.setTextFormat(QtCore.Qt.MarkdownText)
            label13.setText("""
### USER
        """)
            label13.setAlignment(QtCore.Qt.AlignCenter)
            # label13 = self._set_default_margins(label13)
            self.grid.addWidget(label13, 2, 7, 1, 2)

            label14 = QtWidgets.QLabel()
            label14.setTextFormat(QtCore.Qt.MarkdownText)
            label14.setText(""" **Username:**   """)
            label14.setAlignment(QtCore.Qt.AlignCenter)
            # label14 = self._set_default_margins(label14)
            self.grid.addWidget(label14, 3, 7, 1, 1)

            label15 = QtWidgets.QLabel()
            label15.setTextFormat(QtCore.Qt.MarkdownText)
            label15.setText(settings["USERNAME"])
            label15.setAlignment(QtCore.Qt.AlignCenter)
            # label15 = self._set_default_margins(label15)
            self.grid.addWidget(label15, 3, 8, 1, 1)

            label16 = QtWidgets.QLabel()
            label16.setTextFormat(QtCore.Qt.MarkdownText)
            label16.setText(""" **Password:**   """)
            label16.setAlignment(QtCore.Qt.AlignCenter)
            # label16 = self._set_default_margins(label16)
            self.grid.addWidget(label16, 4, 7, 1, 1)

            label17 = QtWidgets.QLabel()
            label17.setTextFormat(QtCore.Qt.MarkdownText)
            label17.setText(settings["PASSWORD"])
            label17.setAlignment(QtCore.Qt.AlignCenter)
            # label17 = self._set_default_margins(label17)
            self.grid.addWidget(label17, 4, 8, 1, 1)

            label23 = QtWidgets.QLabel()
            label23.setTextFormat(QtCore.Qt.MarkdownText)
            label23.setText(""" **Auto-Login:** """)
            label23.setAlignment(QtCore.Qt.AlignCenter)
            # label23 = self._set_default_margins(label23)
            self.grid.addWidget(label23, 5, 7, 1, 1)

            label24 = QtWidgets.QLabel()
            label24.setTextFormat(QtCore.Qt.MarkdownText)
            label24.setText(str(settings["LOGIN"]))
            label24.setAlignment(QtCore.Qt.AlignCenter)
            # label24 = self._set_default_margins(label24)
            self.grid.addWidget(label24, 5, 8, 1, 1)

            # sep2 = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
            # self.grid.addWidget(sep2, 9, 2, 1, 6)

            label18 = QtWidgets.QLabel()
            label18.setTextFormat(QtCore.Qt.MarkdownText)
            label18.setText("""
### OTHER
        """)
            label18.setAlignment(QtCore.Qt.AlignCenter)
            # label18 = self._set_default_margins(label18)
            self.grid.addWidget(label18, 2, 10, 1, 2)

            label19 = QtWidgets.QLabel()
            label19.setTextFormat(QtCore.Qt.MarkdownText)
            label19.setText(""" **Install Extras:** """)
            label19.setAlignment(QtCore.Qt.AlignCenter)
            # label19 = self._set_default_margins(label19)
            self.grid.addWidget(label19, 3, 10, 1, 1)

            label20 = QtWidgets.QLabel()
            label20.setTextFormat(QtCore.Qt.MarkdownText)
            label20.setText(str(settings["EXTRAS"]))
            label20.setAlignment(QtCore.Qt.AlignCenter)
            # label20 = self._set_default_margins(label20)
            self.grid.addWidget(label20, 3, 11, 1, 1)

            label21 = QtWidgets.QLabel()
            label21.setTextFormat(QtCore.Qt.MarkdownText)
            label21.setText(""" **Install Updates:**    """)
            label21.setAlignment(QtCore.Qt.AlignCenter)
            # label21 = self._set_default_margins(label21)
            self.grid.addWidget(label21, 4, 10, 1, 1)

            label22 = QtWidgets.QLabel()
            label22.setTextFormat(QtCore.Qt.MarkdownText)
            label22.setText(str(settings["UPDATES"]))
            label22.setAlignment(QtCore.Qt.AlignCenter)
            # label22 = self._set_default_margins(label22)
            self.grid.addWidget(label22, 4, 11, 1, 1)

            label25 = QtWidgets.QLabel()
            label25.setTextFormat(QtCore.Qt.MarkdownText)
            label25.setText(""" **Keyboard Model:** """)
            label25.setAlignment(QtCore.Qt.AlignCenter)
            # label25 = self._set_default_margins(label25)
            self.grid.addWidget(label25, 5, 10, 1, 1)

            label26 = QtWidgets.QLabel()
            label26.setTextFormat(QtCore.Qt.MarkdownText)
            label26.setText(settings["MODEL"])
            label26.setAlignment(QtCore.Qt.AlignCenter)
            # label26 = self._set_default_margins(label26)
            self.grid.addWidget(label26, 5, 11, 1, 1)

            label27 = QtWidgets.QLabel()
            label27.setTextFormat(QtCore.Qt.MarkdownText)
            label27.setText(""" **Keyboard Layout:**    """)
            label27.setAlignment(QtCore.Qt.AlignCenter)
            # label27 = self._set_default_margins(label27)
            self.grid.addWidget(label27, 6, 10, 1, 1)

            label28 = QtWidgets.QLabel()
            label28.setTextFormat(QtCore.Qt.MarkdownText)
            label28.setText(settings["LAYOUT"])
            label28.setAlignment(QtCore.Qt.AlignCenter)
            # label28 = self._set_default_margins(label28)
            self.grid.addWidget(label28, 6, 11, 1, 1)

            label29 = QtWidgets.QLabel()
            label29.setTextFormat(QtCore.Qt.MarkdownText)
            label29.setText(""" **Keyboard Variant:**   """)
            label29.setAlignment(QtCore.Qt.AlignCenter)
            # label29 = self._set_default_margins(label29)
            self.grid.addWidget(label29, 7, 10, 1, 1)

            label30 = QtWidgets.QLabel()
            label30.setTextFormat(QtCore.Qt.MarkdownText)
            label30.setText(settings["VARIENT"])
            label30.setAlignment(QtCore.Qt.AlignCenter)
            # label30 = self._set_default_margins(label30)
            self.grid.addWidget(label30, 7, 11, 1, 1)

        button1 = QtWidgets.QPushButton("INSTALL NOW -->")
        button1.clicked.connect(self.onnextclicked)
        # button1 = self._set_default_margins(button1)
        self.grid.addWidget(button1, 8, 11, 1, 1)

        button2 = QtWidgets.QPushButton("Exit")
        button2.clicked.connect(self.exit)
        # button2 = self._set_default_margins(button2)
        self.grid.addWidget(button2, 8, 1, 1, 1)

        # self.set_position(Gtk.WindowPosition.CENTER)

        # self.show_all()

    def onnextclicked(self, button):
        """set install to True"""
        self.install = True
        self.exit("clicked")

    # def _set_default_margins(self, widget):
    #     """Set default margin size"""
    #     widget.set_margin_start(10)
    #     widget.set_margin_end(10)
    #     widget.set_margin_top(10)
    #     widget.set_margin_bottom(10)
    #     return widget

    def exit(self, button):
        """exit"""
        self.close()
        print(1)
        return 1


def show_confirm(settings, boot_time=False):
    """Show confirmation dialog"""
    app = QtWidgets.QApplication([sys.argv[0]])
    window = Main(settings)
    if boot_time:
        window = QCommon.set_window_undecorated(window)
    window.show()
    app.exec()
    return window.install


if __name__ == "__main__":
    settings = json.loads(sys.argv[1])
    print(show_confirm(settings))
