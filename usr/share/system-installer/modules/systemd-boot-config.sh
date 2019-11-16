#!/bin/bash
# -*- coding: utf-8 -*-
#
#  systemd-boot-config.sh
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
ROOT="$1"
mkdir -p /etc/kernel/postinstall.d /etc/kernel/postrm.d
echo "#!/bin/bash
#
# This is a simple kernel hook to populate the systemd-boot entries
# whenever kernels are added or removed.
#



# The UUID of your disk.
UUID=\"$(lsblk -dno UUID $(echo $ROOT))\"

# The LUKS volume slug you want to use, which will result in the
# partition being mounted to /dev/mapper/CHANGEME.
#VOLUME=\"CHANGEME\"

# Any rootflags you wish to set.
ROOTFLAGS=\"quiet splash\"



# Our kernels.
KERNELS=()
FIND=\$(ls -A /boot | grep \"vmlinuz-*\")
for each in \$FIND; do
	KERNELS+=\"/boot/\$each \"
done

# There has to be at least one kernel.
if [ \${#KERNELS[@]} -lt 1 ]; then
	echo -e \"\e[2msystemd-boot\e[0m \e[1;31mNo kernels found.\e[0m\"
	exit 1
fi



# Perform a nuclear clean to ensure everything is always in perfect sync.
rm /boot/efi/loader/entries/*.conf
rm -rf /boot/efi/Drauger_OS
mkdir /boot/efi/Drauger_OS



# Copy the latest kernel files to a consistent place so we can keep
# using the same loader configuration.
LATEST=\"\$(echo \$KERNELS | sed 's/\/boot\/vmlinuz//g' | sed 's/ /\n/g' | sed 's/.old//g' | sed '/^[[:space:]]*$/d' | sort -nr | head -n1)\"
echo -e \"\e[2msystemd-boot\e[0m\e[1;32m\${LATEST}\e[0m\"
for FILE in config initrd.img System.map vmlinuz; do
    cp \"/boot/\${FILE}\${LATEST}\" \"/boot/efi/Drauger_OS/\${FILE}\"
    cat << EOF > /boot/efi/loader/entries/Drauger_OS.conf
title   Drauger OS
linux   /Drauger_OS/vmlinuz
initrd  /Drauger_OS/initrd.img
options ro rootflags=\${ROOTFLAGS}
EOF
done



# Copy any legacy kernels over too, but maintain their version-based
# names to avoid collisions.
if [ \${#KERNELS[@]} -gt 1 ]; then
	LEGACY=\"\$(echo \$KERNELS | sed 's/\/boot\/vmlinuz//g' | sed 's/ /\n/g' | sed 's/.old//g' | sed '/^[[:space:]]*$/d' | sort -nr | sed s/\$LATEST//g)\"
	for VERSION in \${LEGACY[@]}; do
	    echo -e \"\e[2msystemd-boot\e[0m\e[1;32m\${VERSION}\e[0m\"
	    for FILE in config initrd.img System.map vmlinuz; do
	        cp \"/boot/\${FILE}\${VERSION}\" \"/boot/efi/Drauger_OS/\${FILE}\${VERSION}\"
	        cat << EOF > /boot/efi/loader/entries/Drauger_OS\${VERSION}.conf
title   Drauger OS \${VERSION}
linux   /Drauger_OS/vmlinuz\${VERSION}
initrd  /Drauger_OS/initrd.img\${VERSION}
options ro rootflags=\${ROOTFLAGS}
EOF
	    done
	done
fi



# Success!
exit 0" > /etc/kernel/postinstall.d/zz-update-systemd-boot
cp /etc/kernel/postinstall.d/zz-update-systemd-boot /etc/kernel/postrm.d/zz-update-systemd-boot
# Set the right owner.
chown root: /etc/kernel/postinstall.d/zz-update-systemd-boot
chown root: /etc/kernel/postrm.d/zz-update-systemd-boot
# Set the right permissions.
chmod 0755 /etc/kernel/postinstall.d/zz-update-systemd-boot
chmod 0755 /etc/kernel/postrm.d/zz-update-systemd-boot
#copy over the kernel and initramfs
cp /etc/kernel/postinstall.d/zz-update-systemd-boot /etc/kernel/postrm.d/zz-update-systemd-boot
