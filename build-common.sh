#!/bin/bash
VERSION=$(cat DEBIAN/edamame-common.control | grep 'Version: ' | sed 's/Version: //g')
PAK=$(cat DEBIAN/edamame-common.control | grep 'Package: ' | sed 's/Package: //g')
ARCH=$(cat DEBIAN/edamame-common.control | grep 'Architecture: '| sed 's/Architecture: //g')
FOLDER="$PAK\_$VERSION\_$ARCH"
FOLDER=$(echo "$FOLDER" | sed 's/\\//g')
OPTIONS="$1"
SETTINGS=$(grep -v "^#" build.conf | sed 's/=/ /g')
META_URL=$(echo "$SETTINGS" | grep "META_URL" | awk '{print $2}')
PACK_URL=$(echo "$SETTINGS" | grep "PACK_URL" | awk '{print $2}')
mkdir ../"$FOLDER"
##############################################################
#							                                 #
#							                                 #
#  COMPILE ANYTHING NECSSARY HERE			                 #
#							                                 #
#							                                 #
##############################################################

# Instead of compiling, we are building a tar.xz archive of the latest kernel package
# Don't make the archive if --pool passed
if [ "$OPTIONS" != "--pool" ]; then
	cd usr/share/edamame
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
echo "Would you like to build with Python 3.11, or 3.12?"
read -p "Exit [0], Do Not Compile [1], Python 3.11 [2], Python 3.12 [3], : " ans
if $(echo "${ans,,}" | grep -qE "1|one|first"); then
	vert="dnc"
elif $(echo "${ans,,}" | grep -qE "2|two|second|3.11"); then
	vert="3.11"
elif $(echo "${ans,,}" | grep -qE "3|three|third|3.12"); then
	vert="3.12"
elif $(echo "${ans,,}" | grep -qE "exit|quit|leave|e|q|x|0|no|zero"); then
	echo "Exiting as requested..."
	exit 1
else
	echo "Input not recognized. Defaulting to Python 3.11"
fi
{
	g++ -pie -m64 -O3 -s -o edamame edamame.cxx
} || {
	echo "Build failed. Try making sure you have 'python${vert}-dev' and 'libpython${vert}-dev' installed" 1>&2
	exit 2
}
cd ../..
files_to_edit=$(find "." -maxdepth 10 -type f -name '*.py' -print)
shebang='\#\!/usr/bin/env'
py_ver=""
if [ "$vert" == "dnc" ]; then
	py_ver="python3"
elif [ "$vert" == "3.11" ]; then
	py_ver="python3.11"
elif [ "$vert" == "3.12" ]; then
	py_ver="python3.12"
fi
shebang="$shebang $py_ver"
for each in $files_to_edit; do
	sed -i "s:\#\!shebang:$shebang:" $each
done
##############################################################
#							                                 #
#							                                 #
#  REMEMBER TO DELETE SOURCE FILES FROM TMP		             #
#  FOLDER BEFORE BUILD					                     #
#							                                 #
#							                                 #
##############################################################

# COPY FILES TO "$FOLDER"
copy=$(<DEBIAN/edamame-common.install)
for each in $copy; do
    if [ ! -d ../"$FOLDER"/${each%/*} ]; then
        mkdir -pv ../"$FOLDER"/${each%/*}
    fi
    cp -rv "$each" ../"$FOLDER"/${each%/*}
done

# BUILD SHIT
cp -Rv DEBIAN ../"$FOLDER"/DEBIAN
mkdir -pv usr/share/doc/$PAK
git log > usr/share/doc/$PAK/changelog
cd usr/share/doc/$PAK
tar --verbose --create --xz -f changelog.gz changelog 1>/dev/null
rm -v changelog
cd ../../../..
base="$PWD"
cp -Rv usr/share/doc/$PAK ../"$FOLDER"/usr/share/doc/$PAK
cd ..

# Clean up
# delete binary files from repo
rm -v "$base"/usr/bin/edamame
# delete C++ source from package
rm -v "$FOLDER"/usr/bin/edamame.cxx
# delete Python cache files
if [[ "$vert" != "dnc" ]]; then
	find "$FOLDER" -maxdepth 10 -type d -name __pycache__ -exec rm -rfv {} \;
fi
# Insert other deps into control file
sed -i "s/<\!--python_vert-->/$py_vert/g" "$FOLDER/DEBIAN/edamame-common.control"
sed -i "s/ , //g" "$FOLDER/DEBIAN/edamame-common.control"
#build the shit
mv "$FOLDER/DEBIAN/edamame-common.control" "$FOLDER/DEBIAN/control"
# mv "$FOLDER/DEBIAN/edamame-common.install" "$FOLDER/DEBIAN/install"
dpkg-deb --build "$FOLDER"
rm -rfv "$FOLDER"
cd "$base"
mkdir build
mv -v ../edamame-common*.deb ./build/
echo "$PAK Version: $VERSION built!"
