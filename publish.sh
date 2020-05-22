#!/usr/bin/env bash
set -x
rm -r output

set -e
mkdir  output
./inmemoriam.py > output/output.html
cp resources/* output/
