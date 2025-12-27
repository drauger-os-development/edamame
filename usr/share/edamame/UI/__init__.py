#!shebang
# -*- coding: utf-8 -*-
#
#  __init__.py
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
"""UI for Edamame"""
import os
import importlib


def load_UI(ui_type: str):
    """Load the specified UI type"""
    ui = ui_type.upper()
    if os.path.exists(f"UI/{ui}_UI"):
        return importlib.import_module(f"UI.{ui}_UI")
    raise ImportError(f"Module {ui}_UI is not present!")


def available_UIs() -> list:
    """List available GUIs/toolkits"""
    uis = os.listdir("UI")
    output = [each.split("_")[0] for each in uis if "_UI" == each[-3:]]
    return output


def UI_in_use() -> str:
    """Tell what UI toolkit is in use."""
    desktop = os.getenv("XDG_CURRENT_DESKTOP")
    if desktop.lower() in ("kde", "lxqt", "dde", "lomiri", "ukui"):
        return "QT"
    if desktop.lower() in ("gnome", "mate", "xfce", "lxde", "cinnamon", "unity", "budgie", "pantheon", "sugar", "phosh"):
        return "GTK"


def auto_load_ui():
    """This function is equivlent to:
        UI.load_UI(UI.UI_in_use())

        If the UI for the currently in use toolkit does not exist, the same error as that one liner will be thrown.
    """
    return load_UI(UI_in_use())
