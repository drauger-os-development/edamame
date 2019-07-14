#!/bin/bash
VERSION=$(cat DEBIAN/control | grep 'Version: ' | sed 's/Version: //g')
PAK=$(cat DEBIAN/control | grep 'Package: ' | sed 's/Package: //g')
mkdir ../"$PAK"_"$VERSION"_all
cp -R etc ../"$PAK"_"$VERSION"_all/etc
cp -R usr ../"$PAK"_"$VERSION"_all/usr
cp -R DEBIAN ../"$PAK"_"$VERSION"_all/DEBIAN
cd ..
#gzip "$PAK"_"$VERSION"_all/usr/share/doc/$PAK/changelog
#cd "$PAK"_"$VERSION"_all/usr/share/man/man1
#gzip $(ls)
#cd ../../../../..
sleep 0.5s
dpkg-deb --build "$PAK"_"$VERSION"_all
rm -rf "$PAK"_"$VERSION"_all
