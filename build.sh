#!/usr/bin/env bash
set -x
rm -r output

set -e
mkdir  output
./inmemoriam.py > output/index.html
cp resources/* output/
cp CNAME output/