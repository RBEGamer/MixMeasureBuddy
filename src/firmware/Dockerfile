FROM ubuntu


ENV MICROPYTHON_BASE_DIR=/var/micropython
ENV PICOTOOL_BASE_DIR=/var/pictool
ENV CUSTOM_SRC_DIR=/var/build/src
ENV BUILD_OUTPUT_DIR=$CUSTOM_SRC_DIR/build
ENV BUILD_TEMP_DIR=$CUSTOM_SRC_DIR/tmp
ENV PICO_SDK_PATH=/var/pico-sdk
ENV DIR2UF2_BASE_DIR=/var/dir2uf2

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y nano git gcc-arm-none-eabi libstdc++-arm-none-eabi-newlib libnewlib-arm-none-eabi build-essential cmake python3 python3-pip pkg-config libusb-1.0-0-dev


# CLONE PICO-SDK
RUN git clone  --depth 1 https://github.com/raspberrypi/pico-sdk.git ${PICO_SDK_PATH}

# CLONE AND BUILD PICOTOOL
RUN git clone  --depth 1 https://github.com/raspberrypi/picotool.git ${PICOTOOL_BASE_DIR}
RUN cd ${PICOTOOL_BASE_DIR} && cmake . && make && make install

# CLONE AND BUILD MICROPYTHON
RUN git clone --depth 1 https://github.com/micropython/micropython.git ${MICROPYTHON_BASE_DIR}
RUN cd ${MICROPYTHON_BASE_DIR} && git submodule update --init
RUN cd ${MICROPYTHON_BASE_DIR} && make -C mpy-cross


# CLONE
RUN pip3 install littlefs-python --break-system-packages
RUN git clone --depth 1 https://github.com/Gadgetoid/dir2uf2.git ${DIR2UF2_BASE_DIR}
# COPY PROJECT FILES OVER
COPY . ${CUSTOM_SRC_DIR}



# RUN chmod +x ${CUSTOM_SRC_DIR}/prepare_manifest.sh
# RUN chmod +x ${CUSTOM_SRC_DIR}/prepare_vfatfs_content.sh
# RUN chmod +x ${CUSTOM_SRC_DIR}/build_firmware.sh


WORKDIR ${CUSTOM_SRC_DIR}
#RUN ls ${CUSTOM_SRC_DIR}
ENTRYPOINT ["./build_firmware.sh"]
