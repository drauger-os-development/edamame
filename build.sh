#!/bin/bash
VERSION=$(cat DEBIAN/control | grep 'Version: ' | sed 's/Version: //g')
PAK=$(cat DEBIAN/control | grep 'Package: ' | sed 's/Package: //g')
ARCH=$(cat DEBIAN/control | grep 'Architecture: '| sed 's/Architecture: //g')
FOLDER="$PAK\_$VERSION\_$ARCH"
FOLDER=$(echo "$FOLDER" | sed 's/\\//g')
OPTIONS="$1"
mkdir ../"$FOLDER"
##############################################################
#							     #
#							     #
#  COMPILE ANYTHING NECSSARY HERE			     #
#							     #
#							     #
##############################################################

# Instead of compiling, we are building a tar.xz archive of the latest kernel package
# Don't make the archive if --pool passed
if [ "$OPTIONS" != "--pool" ]; then
	cd usr/share/system-installer
	echo -e "\t###\tDOWNLOADING\t###\t"
	rsync -vr rsync://apt.draugeros.org/aptsync/pool/main/l/linux-upstream kernel
	rsync -vr rsync://apt.draugeros.org/aptsync/pool/main/l/linux-meta kernel
	echo -e "\t###\tDELETING CRUFT\t###\t"
	list=$(ls kernel)
	for each in $list; do
		remove=$(ls kernel/$each | grep -v 'amd64.deb$')
		for each2 in $remove; do
			rm -rfv kernel/$each/$each2
		done
	done
	meta=$(echo kernel/linux-meta/$(ls kernel/linux-meta | sort -Vr | head -1))
	dep=$(dpkg-deb --field $meta Depends | sed 's/, /\\|/g')
	cd kernel/linux-upstream
	rm -rfv $(ls | sed "/\($dep\)/d")
	dep=$(echo "$dep" | sed 's/\\|/ /g' | awk '{print $1}' | sed 's/\(image-\|headers-\)/xanmod_/g')
	rm -rfv $(ls | grep "edge")
	rm -rfv $(ls | grep "cacule")
	cd ../linux-meta
	rm -rfv $(ls | grep -v "$dep")
	rm -rfv $(ls | grep "edge")
	rm -rfv $(ls | grep "cacule")
	cd ..
	dep=$(echo "$dep" | sed 's/xanmod_//g')
	mv linux-upstream "$dep"
	cd ..
	# delete empty folders
	find . -type d -empty -print -delete
	echo -e "\t###\tCOMPRESSING\t###\t"
	tar --verbose --create --xz -f kernel.tar.xz kernel
	echo -e "\t###\tCLEANING\t###\t"
	rm -rfv kernel
	cd ../../../..
fi

# Pshyc - we're compiling shit now
cd usr/bin
g++ -o system-installer system-installer.cxx $(python3.9-config --ldflags --cflags --embed)
cd ../share/system-installer
g++ -c -Wall -Werror -fpic common.cxx $(python3.9-config --cflags)
g++ -shared -o libcommon.so common.o $(python3.9-config --ldflags)
cd ../../..
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
mkdir -p usr/share/doc/$PAK
git log > usr/share/doc/$PAK/changelog
cd usr/share/doc/$PAK
tar --verbose --create --xz -f changelog.gz changelog 1>/dev/null
rm changelog
cd ../../../..
base="$PWD"
cd ..
#DELETE STUFF HERE
if [ "$OPTIONS" != "--pool" ]; then
	rm system-installer/usr/share/system-installer/modules/kernel.tar.xz
fi
# delete binary files from repo
rm "$base"/usr/bin/system-installer
rm "$base"/usr/share/system-installer/libcommon.so
# delete object files from the repo
rm "$base"/use/share/system-installer/common.o
# delete C++ source from package
rm "$FOLDER"/usr/bin/system-installer.cxx
#build the shit
dpkg-deb --build "$FOLDER"
rm -rf "$FOLDER"
