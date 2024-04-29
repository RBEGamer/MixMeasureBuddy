#!/bin/bash
cd "$(dirname "$0")"

mkdir -p $BUILD_TEMP_DIR

# CREATE BINARY STRING FROM FILE
cd $CUSTOM_SRC_DIR
python3 ./prepare_vfatfs_content.py $CUSTOM_SRC_DIR/src $CUSTOM_SRC_DIR/fsdatareconstructor.py.TEMPLATE $CUSTOM_SRC_DIR/lib/fsdatareconstructor.py