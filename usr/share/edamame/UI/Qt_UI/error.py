#!shebang
# -*- coding: utf-8 -*-
#
#  error.py
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
"""Error dialog for Edamame"""
from sys import argv
from qtpy import QtGui, QtWidgets, QtCore
try:
    from UI.Qt_UI import report
except ImportError:
    try:
        from Qt_UI import report
    except ImportError:
        import report


class Main(report.Main):
    """UI Error Class"""
    def __init__(self, display, report_setting):
        """set up Error UI"""
        super().__init__()
        self.display = display
        self.enable_reporting = report_setting
        self.scrolling = False
        self.main_menu("clicked")

    def main_menu(self, widget):
        """Main Menu"""
        self.clear_window()

        self.label = QtWidgets.QLabel("**" + self.display + "**")
        self.label.setTextFormat(QtCore.Qt.MarkdownText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label = self._set_default_margins(self.label)
        self.grid.addWidget(self.label, 1, 1, 1, 3)

        if self.enable_reporting:
            self.label2 = QtWidgets.QLabel("""
If you wish to notify the developers of this failed installation,\n
you can send an installation report below.
    """)
            self.label2.setAlignment(QtCore.Qt.AlignCenter)
            self.label2.setTextFormat(QtCore.Qt.MarkdownText)
            self.label2 = self._set_default_margins(self.label2)
            self.grid.addWidget(self.label2, 2, 1, 1, 3)

            self.button = QtWidgets.QPushButton("Send Installation report")
            self.button.clicked.connect(self.main)
            self.button = self._set_default_margins(self.button)
            self.grid.addWidget(self.button, 3, 3, 1, 1)

        self.button2 = QtWidgets.QPushButton("Exit")
        self.button2.clicked.connect(self.exit)
        self.button2 = self._set_default_margins(self.button2)
        self.grid.addWidget(self.button2, 3, 1, 1, 1)


def show_error(display: str, report_setting: bool = True):
    """Show Error Dialog

    `display` is displayed to the user as the main error text,
    along with instructions on how to send an installation report.
    `report` controls whether or not the user can send an installation report"""
    app = QtWidgets.QApplication([argv[0]])
    window = Main(display, report_setting)
    # window.set_position(Gtk.WindowPosition.CENTER)
    # window.clicked.connect("delete-event", Main.exit)
    window.show()
    app.exec()


if __name__ == '__main__':
    DISPLAY = str(argv[1])
    show_error(DISPLAY)
