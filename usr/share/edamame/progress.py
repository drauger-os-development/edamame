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
import UI
import sys

try:
    if "--gui=" in sys.argv[1]:
        gui = sys.argv[1].split("=")[-1].upper()
        ui = UI.load_UI(gui)
    else:
        ui = UI.load_UI("GTK")
except IndexError:
    ui = UI.load_UI("GTK")

ui.progress.show_progress()
