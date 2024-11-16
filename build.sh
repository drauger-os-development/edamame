#!/bin/bash
echo "Building all Edamame packages!"
./build-common.sh "$1"
./build-qt.sh
./build-gtk.sh
mkdir build
cp ../edamame*.deb build/

echo "All Edamame packages build! Please check \`build' for build artifacts and distributables."
