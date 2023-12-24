#!/bin/bash
cd "$(dirname "$0")"

# SPECIFY TARGET BOARD PORT HERE like: stm32, rp2
PORT_TYPE="rp2"


# COPY DATA-FOLDER OVER
#cp -R $PWD/src/data
echo "MICROPYTHON_BASE_DIR=$MICROPYTHON_BASE_DIR"
echo "CUSTOM_SRC_DIR=$CUSTOM_SRC_DIR"
echo "MICROPYTHON_BOARD=$MICROPYTHON_BASE_DIR"
echo "BUILD_OUTPUT_DIR=$BUILD_OUTPUT_DIR"
echo "PORT_TYPE=$PORT_TYPE"

# PREPARE MANIFESTS FIRST
chmod +x $CUSTOM_SRC_DIR/prepare_manifest.sh
$CUSTOM_SRC_DIR/prepare_manifest.sh


chmod +x $CUSTOM_SRC_DIR/prepare_vfatfs_content.sh
$CUSTOM_SRC_DIR/prepare_vfatfs_content.sh

# PREPARE COMPILER
cd $MICROPYTHON_BASE_DIR/
make -C mpy-cross

# CREATE OUTPUT FOLDER
mkdir -p $BUILD_OUTPUT_DIR

# BUILD FIRMWARE FILES FOR EACH FOUND MANIFEST FILE
for i in $CUSTOM_SRC_DIR/manifest_*.py; do
    [ -f "$i" ] || break

    echo "MANIFEST_FILE=$i"

    fn=$(basename $i .py)
    fn_prefix="manifest_"
    BOARD_NAME=$(echo "$fn" | sed "s/$fn_prefix//")
    echo "BOARD_NAME=$BOARD_NAME"
    
    # CREATE CUSTOM BOOT PY IN MODULES
    cp -f $CUSTOM_SRC_DIR/boot.py $MICROPYTHON_BASE_DIR/ports/$PORT_TYPE/modules/boot.py
    ls $MICROPYTHON_BASE_DIR/ports/$PORT_TYPE/modules
    # BUILD FIRMWARE    
    cd $MICROPYTHON_BASE_DIR/ports/$PORT_TYPE
    # DOWNLOAD BOARD SPECIFIC SDK
    make submodules
    make clean
    make BOARD=$BOARD_NAME FROZEN_MANIFEST=$i


    # COPY OUTPUT RESULT TO RESULT-FOLDER
    ls $MICROPYTHON_BASE_DIR/ports/$PORT_TYPE/build-$BOARD_NAME/
    mkdir -p $BUILD_OUTPUT_DIR/build-$BOARD_NAME
    cp -f $MICROPYTHON_BASE_DIR/ports/$PORT_TYPE/build-$BOARD_NAME/firmware.* $BUILD_OUTPUT_DIR/build-$BOARD_NAME

done