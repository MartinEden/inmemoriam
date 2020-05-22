#!/usr/bin/env bash
set -ex
./build.sh
cp CNAME output/
cd output && surge .
