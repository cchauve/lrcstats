#!/bin/bash

echo "Building aligner..."
cd src/aligner
make
echo "Done."

echo "Building fastUtils..."
cd ../preprocessing/utils
make
echo "Done."

echo "Installation complete. You may now use LRCStats."
