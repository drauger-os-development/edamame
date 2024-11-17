#!shebang
# -*- coding: utf-8 -*-
#
#  progress.py
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
"""Progress Window GUI"""
import sys
import signal
import json
from os import remove
from qtpy import QtCore, QtWidgets, QtGui
try:
    import UI.QT_UI.qt_common as QCommon
except ImportError:
    import qt_common as QCommon

window = None


class Main(QtWidgets.QWidget):
    """Progress UI Window"""
    signal = QtCore.Signal()

    def __init__(self, app, distro="Linux"):
        """Progress UI main set-up"""
        super().__init__()
        self.setWindowTitle("Edamame")
        self.install = False
        self.setWindowIcon(QtGui.QIcon.fromTheme("system-installer"))
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.distro = distro

        self.label = QtWidgets.QLabel()
        self.label.setText(f"""
# Installing {self.distro} to your internal hard drive.
This may take some time. If you have an error, please send
the log file (located at /tmp/edamame.log) to: contact@draugeros.org""")
        self.label.setTextFormat(QtCore.Qt.MarkdownText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # self.label = self._set_default_margins(self.label)
        self.grid.addWidget(self.label, 1, 1, 1, 1)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setTextVisible(True)
        self.progress.setMaximum(100)
        self.progress.setMinimum(0)
        self.progress.setValue(0)
        # self.progress = self._set_default_margins(self.progress)
        self.grid.addWidget(self.progress, 3, 1, 1, 1)

        self.file_contents = QtWidgets.QTextEdit()
        self.file_contents.setReadOnly(True)
        self.file_contents.setCursorWidth(0)
        self.file_contents.setCurrentFont(QtGui.QFont("Ubuntu Mono"))
        self.file_contents.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        # self.text = self._set_default_margins(self.text)
        self.grid.addWidget(self.file_contents, 5, 1, 1, 1)

        # self.set_position(Gtk.WindowPosition.CENTER)

        self.signal.connect(self.pulse)
        self.startTimer(33)

    # def _set_default_margins(self, widget):
    #     """Set default margin size"""
    #     widget.set_margin_start(10)
    #     widget.set_margin_end(10)
    #     widget.set_margin_top(10)
    #     widget.set_margin_bottom(10)
    #     return widget

    def read_file(self):
        """Read Progress log"""
        text = ""
        try:
            with open("/tmp/edamame.log", "r") as read_file:
                text = read_file.read()
            if len(text.split("\n")) > 10:
                text = text.split("\n")
                text = text[-9:]
                for each in enumerate(text):
                    if len(text[each[0]]) > 90:
                        text[each[0]] = text[each[0]][:90]
                    elif len(text[each[0]]) < 90:
                        multiplyer = 90 - len(text[each[0]])
                        text[each[0]] = text[each[0]] + (" " * multiplyer)
                text = "\n".join(text)
            self.file_contents.setText(text)
        except FileNotFoundError:
            self.file_contents.setText("")
        return True


    def pulse(self):
        """Update progress indicator and log output in GUI"""
        fraction = ""
        try:
            with open("/tmp/edamame-progress.log", "r") as prog_file:
                fraction = int(prog_file.read())
        except FileNotFoundError:
            fraction = 0
        try:
            self.progress.setValue(fraction)
        except ValueError:
            self.progress.setValue(0)
        if fraction == 100:
            remove("/tmp/edamame-progress.log")
            remove("/mnt/tmp/edamame-progress.log")
            self.close()
            self.source_id = None
            return False

        self.read_file()
        return True

    def timerEvent(self, *args, **kwargs):
        self.signal.emit()


def show_progress():
    """Show Progress UI"""
    try:
        with open("/etc/edamame/settings.json", "r") as file:
            distro = json.load(file)["distro"]
    except (FileNotFoundError, KeyError):
        distro = "Linux"
    signal.signal(signal.SIGTERM, handle_sig_term)
    app = QtWidgets.QApplication([sys.argv[0]])
    global window
    window = Main(distro)
    window = QCommon.set_window_undecorated(window)
    window = QCommon.set_window_nonresizeable(window)
    window.show()
    app.exec()


def handle_sig_term(signum, frame):
    global window
    window.close()
    print("progress.py received SIGTERM! Installation is likely complete...")
    sys.exit()


if __name__ == '__main__':
    show_progress()
