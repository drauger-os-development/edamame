#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  set_locale.py
#
#  Copyright 2023 Thomas Castleman <batcastle@draugeros.org>
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
"""Set system locale for a given langauage name"""
from __future__ import print_function
from sys import argv, stderr
from os import remove
from subprocess import check_call, CalledProcessError


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def set_locale(lang_set):
    """Figure out locale code for a given language name"""
    eprint("    ###    set_locale.py STARTED    ###    ")
    # figure out what LANG to set
    with open("/etc/locale.gen", "r") as locale_file:
        data = locale_file.read()
    data = data.split("\n")
    for each in range(len(data) - 1, -1, -1):
        if "UTF-8" not in data[each][-5:]:
            del data[each]
            continue
        data[each] = data[each].split(" ")
        if data[each][0] == "#":
            data[each] = data[each][1][:-6]
        else:
            data[each] = data[each][0][:-6]
    for each in range(len(data) - 1, -1, -1):
        if (("@" in data[each]) or ("_" not in data[each]) or (data[each] == "")):
            del data[each]
    for each in range(len(data) - 1, -1, -1):
        if lang_set + "_" not in data[each]:
            del data[each]
    _setlocale(data[0])

    eprint("    ###    set_locale.py STOPPED    ###    ")


def _setlocale(locale):
    """Handle setting locale for a given locale code"""
    # Edit /etc/locale.gen
    with open("/etc/locale.gen", "r") as gen_file:
        contents = gen_file.read()
    contents = contents.split("\n")
    code = locale.split("_")[0]
    for each in enumerate(contents):
        if ((code + "_" in contents[each[0]]
            ) and (".UTF-8 UTF-8" in contents[each[0]])):
            if contents[each[0]][0] == "#":
                contents[each[0]] = contents[each[0]].split(" ")
                del contents[each[0]][0]
                contents[each[0]] = " ".join(contents[each[0]])
    # for each in enumerate(contents):
        # if contents[each[0]] == ("# " + locale + ".UTF-8 UTF-8"):
            # contents[each[0]] = locale + ".UTF-8 UTF-8"
            # break
    remove("/etc/locale.gen")
    contents = "\n".join(contents)
    with open("/etc/locale.gen", "w+") as new_gen:
        new_gen.write(contents)
    try:
        check_call(["locale-gen"], stdout=stderr.buffer)
    except CalledProcessError:
        eprint("WARNING: `locale-gen' failed.")
    try:
        check_call(["update-locale", "LANG=%s.UTF-8" % (locale), "LANGUAGE"])
    except CalledProcessError:
        eprint("WARNING: `update-locale' failed.")


if __name__ == '__main__':
    set_locale(argv[1])
