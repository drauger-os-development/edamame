#!/bin/bash
VERSION=$(cat DEBIAN/edamame-qt.control | grep 'Version: ' | sed 's/Version: //g')
PAK=$(cat DEBIAN/edamame-qt.control | grep 'Package: ' | sed 's/Package: //g')
ARCH=$(cat DEBIAN/edamame-qt.control | grep 'Architecture: '| sed 's/Architecture: //g')
FOLDER="$PAK\_$VERSION\_$ARCH"
FOLDER=$(echo "$FOLDER" | sed 's/\\//g')
SETTINGS=$(grep -v "^#" build.conf | sed 's/=/ /g')
mkdir ../"$FOLDER"
##############################################################
#							                                 #
#							                                 #
#  COMPILE ANYTHING NECSSARY HERE			                 #
#							                                 #
#							                                 #
##############################################################

files_to_edit=$(find "$PWD" -maxdepth 10 -type f -name '*.py' -print | grep -v "test")
shebang='\#\!/usr/bin/env'
py_ver="python3"
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
copy=$(<DEBIAN/edamame-qt.install)
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
# delete Python cache files
if [[ "$vert" != "dnc" ]]; then
	find "$FOLDER" -maxdepth 10 -type d -name __pycache__ -exec rm -rfv {} \;
fi
# Insert other deps into control file
sed -i "s/<\!--python_vert-->/$py_vert/g" "$FOLDER/DEBIAN/edamame-qt.control"
sed -i "s/ , //g" "$FOLDER/DEBIAN/edamame-qt.control"
#build the shit
mv "$FOLDER/DEBIAN/edamame-qt.control" "$FOLDER/DEBIAN/control"
# mv "$FOLDER/DEBIAN/edamame-common.install" "$FOLDER/DEBIAN/install"
dpkg-deb --build "$FOLDER"
rm -rfv "$FOLDER"
cd "$base"
for each in $files_to_edit; do
	sed -i "s:$shebang:\#\!shebang:" $each
done
cd "$base"
mkdir build
mv -v ../edamame-qt*.deb ./build/
echo "$PAK Version: $VERSION built!"
