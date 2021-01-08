#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  get_pass.py
#
#  Copyright 2020 Thomas Castleman <contact@draugeros.org>
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
"""Generate Password for Installation Report Uploading using Temp Key"""
import curl
import hashlib
import secrets


def hash1(data, loops=1000):
    """Looping SHA1 Hasher"""
    output = data.encode()
    for each in range(loops):
        if type(output) == bytes:
            output = hashlib.sha1(output)
        else:
            output = hashlib.sha1(output.hexdigest().encode())
    return output.hexdigest()


def hash256(data, loops=1000):
    """Looping SHA256 Hasher"""
    output = data.encode()
    for each in range(loops):
        if type(output) == bytes:
            output = hashlib.sha256(output)
        else:
            output = hashlib.sha256(output.hexdigest().encode())
    return output.hexdigest()

def hash512(data, loops=1000):
    """Looping SHA512 Hasher"""
    output = data.encode()
    for each in range(loops):
        if type(output) == bytes:
            output = hashlib.sha512(output)
        else:
            output = hashlib.sha512(output.hexdigest().encode())
    return output.hexdigest()


def complex_hash(data):
    """Generate a complex hash of input"""
    hash_count = ord(data[-1]) * 16
    output = data
    for each in range(hash_count):
        loop_count = int((ord(output[35]) * 47) / 12)
        hash_algo = ord(output[17]) % 3
        if hash_algo == 0:
            output = hash1(output, loops=loop_count)
        elif hash_algo == 1:
            output = hash256(output, loops=loop_count)
        elif hash_algo == 2:
            output = hash512(output, loops=loop_count)
        if type(output) == hashlib._hashlib.HASH:
            output = output.hexdigest()
        elif type(output) == bytes:
            output = output.decode()
    return output

def get_key(url="https://download.draugeros.org/hash_files/.install_report_keys/temp_key.txt"):
    """Download Key"""
    cURL = curl.Curl()
    cURL.set_url(url)
    # We do the following because while we COULD do:
    #   return cURL.get()
    # If we return our data this way, later it will be slightly easier
    # to add processing beforehand.
    key = cURL.get()
    key = key.decode()
    return key

def generate_password():
    """Generate Password"""
    key = get_key()
    loop = 3
    password = key
    for each in range(loop):
        password = complex_hash(password)
    return password
