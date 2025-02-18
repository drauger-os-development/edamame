#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_install_extras.py
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
"""Test auto_login_set Library"""
import os
from modules import auto_login_set as als


def test_determine_dm_allowed():
    """Check to ensure we are detecting an allowed DisplayManager"""
    dm = als.determine_display_manager()
    assert dm in ("gdm3", "lightdm", "sddm", "lxdm", "wdm", "xdm")


def test_determine_dm_correct():
    """Check we got the correct DM"""
    dm = als.determine_display_manager()
    if os.path.exists('/etc/X11/default-display-manager'):
        with open('/etc/X11/default-display-manager', 'r') as f:
            display_manager = f.readline().strip().split('/')[-1]
    assert dm.lower() == display_manager.lower()
