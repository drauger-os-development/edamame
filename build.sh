#!/bin/bash
VERSION=$(cat DEBIAN/control | grep 'Version: ' | sed 's/Version: //g')
PAK=$(cat DEBIAN/control | grep 'Package: ' | sed 's/Package: //g')
ARCH=$(cat DEBIAN/control | grep 'Architecture: '| sed 's/Architecture: //g')
FOLDER="$PAK\_$VERSION\_$ARCH"
FOLDER=$(echo "$FOLDER" | sed 's/\\//g')
OPTIONS="$1"
SETTINGS=$(grep -v "^#" build.conf | sed 's/=/ /g')
META_URL=$(echo "$SETTINGS" | grep "META_URL" | awk '{print $2}')
PACK_URL=$(echo "$SETTINGS" | grep "PACK_URL" | awk '{print $2}')
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
	rsync -vr "$PACK_URL" kernel
	rsync -vr "$META_URL" kernel
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
	cd ../../..
fi

# Pshyc - we're compiling shit now
cd usr/bin
echo "Would you like to build with Python 3.10 or 3.11?"
read -p "Python 3.10 [1], Python 3.11 [2], Exit [0]: " ans
if $(echo "${ans,,}" | grep -qE "1|one|first|3.10"); then
	vert="3.10"
elif $(echo "${ans,,}" | grep -qE "2|two|second|3.11"); then
	vert="3.11"
elif $(echo "${ans,,}" | grep -qE "exit|quit|leave|e|q|x|0|no|zero"); then
	echo "Exiting as requested..."
	exit 1
else
	echo "Input not recognized. Defaulting to Python 3.10"
fi
{
	g++ -fPIE -m64 -o system-installer system-installer.cxx $(python"${vert}"-config --ldflags --cflags --embed)
} || {
	echo "Build failed. Try making sure you have 'python${vert}-dev' and 'libpython${vert}-dev' installed" 1>&2
	exit 2
}
cd ../..
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
	rm "$base"/usr/share/system-installer/kernel.tar.xz
fi
# delete binary files from repo
rm "$base"/usr/bin/system-installer
# delete C++ source from package
rm "$FOLDER"/usr/bin/system-installer.cxx
# delete Python cache files
find "$FOLDER" -maxdepth 10 -type d -name __pycache__ -exec rm -rfv {} \;
#build the shit
dpkg-deb --build "$FOLDER"
rm -rf "$FOLDER"
