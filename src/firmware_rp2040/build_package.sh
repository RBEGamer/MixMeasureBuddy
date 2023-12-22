#!/bin/bash
cd "$(dirname "$0")"
#cd ./microfreezer
#python3 ./microfreezer.py -s ../ -d ../build/

# generate manifest file by adding all .py files in src into a new manufest file:
# module("foo.py", base_path="src/drivers")