#!shebang
# -*- coding: utf-8 -*-
#
#  immersion.py
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
"""Enable DE/WM or DE/WM features"""
import subprocess as subproc
import psutil
import de_control._common as com


class Immersion():
    """Control Immersion mode with a desktop environment"""
    def __init__(self):
        self.init_size = None
        self.de = com.get_de()

    def enable(self):
        """Enable Immersion within DE.

        This may involve disabling desktop icons, removing panels, and more.
        """
        if self.de == "XFCE":
            subproc.Popen(["xfconf-query", "--channel", "xfce4-desktop",
                              "--property", "/desktop-icons/style", "--set", "0"])
            # Kill Xfce4 Panel, makes this more emersive
            for proc in psutil.process_iter():
                # check whether the process name matches
                if proc.name() == "xfce4-panel":
                    proc.terminate()
        elif self.de == "KDE":
            self.init_size = subproc.check_output("qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript 'print(panels()[0].height)'", shell=True).decode()
            subproc.check_call("qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript 'panels()[0].height = -1'", shell=True)

    def disable(self):
        """disable Immersion within DE.

        This may involve enabling desktop icons, re-adding panels, and more.
        """
        if self.de == "XFCE":
            # restart panel
            subproc.Popen(["xfce4-panel"])
            # bring back desktop icons
            subproc.Popen(["xfconf-query", "--channel", "xfce4-desktop",
                              "--property", "/desktop-icons/style", "--set", "2"])
        elif self.de == "KDE":
            if self.init_size is not None:
                subproc.check_call(f"qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript 'panels()[0].height = {self.init_size}'", shell=True)
