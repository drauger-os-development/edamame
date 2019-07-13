#!/bin/bash
# -*- coding: utf-8 -*-
#
#  make_swap.sh
#
#  Copyright 2019 Thomas Castleman <contact@draugeros.org>
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
SWAP="$1"
KB=(( $SWAP * 1024 ))
#STEP 1: allocate file
dd if=/dev/zero of=/.swapfile bs="$SWAP" count="$KB"
#STEP 2: Set permissions
chmod 600 /.swapfile
#STEP 3: Make the file a swapspace
mkswap /.swapfile

