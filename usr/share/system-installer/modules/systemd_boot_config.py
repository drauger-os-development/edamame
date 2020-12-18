#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  systemd_boot_config.py
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
"""Configure Systemd-Boot"""
from os import mkdir, chown, chmod
from sys import stderr, argv
from subprocess import check_output


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=stderr, **kwargs)


def systemd_boot_config(root):
    """Configure Systemd-Boot"""
    eprint("\t###\tsystemd-boot-config.py STARTED\t###\t")
    try:
        mkdir("/etc/kernel/postinst.d")
    except FileExistsError:
        eprint("postinst.d already exists")
    try:
        mkdir("/etc/kernel/postrm.d")
    except FileExistsError:
        eprint("postrm.d already exists")
    uuid = check_output(["blkid", "-s", "PARTUUID", "-o", "value", root]).decode()[:-1]
    # Parse out all the stuff we don't need
    contents = r"""#!/bin/bash
#
# This is a simple kernel hook to populate the systemd-boot entries
# whenever kernels are added or removed.
#



# The UUID of your disk.
UUID=$(</etc/systemd-boot/uuid.conf)

# The LUKS volume slug you want to use, which will result in the
# partition being mounted to /dev/mapper/CHANGEME.
#VOLUME="CHANGEME"

# Any rootflags you wish to set.
ROOTFLAGS="quiet splash"
RECOVERY_FLAGS="ro recovery nomodeset"



# Our kernels.
KERNELS=()
FIND=$(ls -A /boot | grep "vmlinuz-*")
for each in $FIND; do
    KERNELS+="/boot/$each "
done

# There has to be at least one kernel.
if [ ${#KERNELS[@]} -lt 1 ]; then
    echo -e "\e[2msystemd-boot\e[0m \e[1;31mNo kernels found.\e[0m"
    exit 1
fi



# Perform a nuclear clean to ensure everything is always in perfect sync.
rm /boot/efi/loader/entries/*.conf
rm -rf /boot/efi/Drauger_OS
mkdir /boot/efi/Drauger_OS



# Copy the latest kernel files to a consistent place so we can keep
# using the same loader configuration.
LATEST="$(echo $KERNELS | sed 's/\/boot\/vmlinuz//g' | sed 's/ /\n/g' | sed 's/.old//g' | sed '/^[[:space:]]*$/d' | sed 's/-//' | sort -Vr | head -n1)"
LATEST="$(echo $LATEST | sed 's/vmlinuz//')"
echo -e "\e[2msystemd-boot\e[0m \e[1;32m${LATEST}\e[0m"
for FILE in config initrd.img System.map vmlinuz; do
    cp "/boot/${FILE}-${LATEST}" "/boot/efi/Drauger_OS/${FILE}"
    cat << EOF > /boot/efi/loader/entries/Drauger_OS.conf
title   Drauger OS
linux   /Drauger_OS/vmlinuz
initrd  /Drauger_OS/initrd.img
options root=PARTUUID=$UUID ${ROOTFLAGS}
EOF
    cat << EOF > /boot/efi/loader/entries/Drauger_OS_Recovery.conf
title   Drauger OS Recovery
linux   /Drauger_OS/vmlinuz
initrd  /Drauger_OS/initrd.img
options root=PARTUUID=$UUID ${RECOVERY_FLAGS}
EOF
done



# Copy any legacy kernels over too, but maintain their version-based
# names to avoid collisions.
if [ ${#KERNELS[@]} -gt 1 ]; then
    LEGACY="$(echo $KERNELS | sed 's/\/boot\/vmlinuz//g' | sed 's/ /\n/g' | sed 's/.old//g' | sed '/^[[:space:]]*$/d' | sed 's/-//' | sort -Vr | sed s/$LATEST//g)"
    for VERSION in ${LEGACY[@]}; do
        echo -e "\e[2msystemd-boot\e[0m \e[1;32m${VERSION}\e[0m"
        for FILE in config initrd.img System.map vmlinuz; do
            cp "/boot/${FILE}-${VERSION}" "/boot/efi/Drauger_OS/${FILE}${VERSION}"
            cat << EOF > /boot/efi/loader/entries/Drauger_OS-${VERSION}.conf
title   Drauger OS ${VERSION}
linux   /Drauger_OS/vmlinuz-${VERSION}
initrd  /Drauger_OS/initrd.img-${VERSION}
options root=PARTUUID=$UUID ${ROOTFLAGS}
EOF
            cat << EOF > /boot/efi/loader/entries/Drauger_OS_Recovery.conf
title   Drauger OS ${VERSION} Recovery
linux   /Drauger_OS/vmlinuz-${VERSION}
initrd  /Drauger_OS/initrd.img-${VERSION}
options root=PARTUUID=$UUID ${RECOVERY_FLAGS}
EOF
        done
    done
fi



# Success!"""
    with open("/etc/kernel/postinst.d/zz-update-systemd-boot", "w+") as postinst:
        postinst.write(contents)
    with open("/etc/kernel/postrm.d/zz-update-systemd-boot", "w+") as postrm:
        postrm.write(contents)
    chown("/etc/kernel/postinst.d/zz-update-systemd-boot", 0, 0)
    chown("/etc/kernel/postrm.d/zz-update-systemd-boot", 0, 0)
    chmod("/etc/kernel/postinst.d/zz-update-systemd-boot", 0o755)
    chmod("/etc/kernel/postrm.d/zz-update-systemd-boot", 0o755)
    mkdir("/etc/systemd-boot")
    with open("/etc/systemd-boot/uuid.conf", "w+") as conf:
        conf.write(uuid)
    eprint("\t###\tsystemd-boot-config.py CLOSED\t###\t")
    return 0


if __name__ == '__main__':
    systemd_boot_config(argv[1])
