#!/bin/bash
VERSION=$(cat DEBIAN/control | grep 'Version: ' | sed 's/Version: //g')
PAK=$(cat DEBIAN/control | grep 'Package: ' | sed 's/Package: //g')
ARCH=$(cat DEBIAN/control | grep 'Architecture: '| sed 's/Architecture: //g')
FOLDER="$PAK\_$VERSION\_$ARCH"
FOLDER=$(echo "$FOLDER" | sed 's/\\//g')
mkdir ../"$FOLDER"
##############################################################
#							     #
#							     #
#  COMPILE ANYTHING NECSSARY HERE			     #
#							     #
#							     #
##############################################################

# Instead of compiling, we are building a tar.xz archive of the latest kernel package
cd usr/share/system-installer/modules
rsync -vr rsync://apt.draugeros.org/aptsync/pool/main/l/linux-5.[8-9].*-xanmod* kernel
rsync -vr rsync://apt.draugeros.org/aptsync/pool/main/l/linux-meta-xanmod kernel
list=$(ls kernel)
for each in $list; do
	remove=$(ls kernel/$each | grep -v 'amd64.deb$')
	for each2 in $remove; do
		rm -rf kernel/$each/$each2
	done
done
meta="kernel/linux-meta-xanmod/$(ls kernel/linux-meta-xanmod)"
dep=$(dpkg-deb --field $meta Depends | sed 's/,/ /g' | awk '{print $1}' | sed 's/-headers//g')
cd kernel
rm -rf $(ls | grep -Ev "^linux-meta-xanmod$|^$dep\$")
cd ..
# delete empty folders
find . -type d -empty -print -delete
tar --verbose --create --xz -f kernel.tar.xz kernel
rm -rf kernel
cd ../../../..
##############################################################
#							     #
#							     #
#  REMEMBER TO DELETE SOURCE FILES FROM TMP		     #
#  FOLDER BEFORE BUILD					     #
#							     #
#							     #
##############################################################
if [ -d bin ]; then
	cp -R bin ../"$FOLDER"/bin
fi
if [ -d etc ]; then
	cp -R etc ../"$FOLDER"/etc
fi
if [ -d usr ]; then
	cp -R usr ../"$FOLDER"/usr
fi
if [ -d lib ]; then
	cp -R lib ../"$FOLDER"/lib
fi
if [ -d lib32 ]; then
	cp -R lib32 ../"$FOLDER"/lib32
fi
if [ -d lib64 ]; then
	cp -R lib64 ../"$FOLDER"/lib64
fi
if [ -d libx32 ]; then
	cp -R libx32 ../"$FOLDER"/libx32
fi
if [ -d sbin ]; then
	cp -R sbin ../"$FOLDER"/sbin
fi
if [ -d var ]; then
	cp -R var ../"$FOLDER"/var
fi
if [ -d opt ]; then
	cp -R opt ../"$FOLDER"/opt
fi
if [ -d srv ]; then
	cp -R srv ../"$FOLDER"/srv
fi
cp -R DEBIAN ../"$FOLDER"/DEBIAN
cd ..
#DELETE STUFF HERE
rm system-installer/usr/share/system-installer/modules/kernel.tar.xz
#build the shit
dpkg-deb --build "$FOLDER"
rm -rf "$FOLDER"
