FROM ubuntu





RUN apt update
RUN apt install -y python3
RUN apt install -y git gcc-arm-none-eabi libstdc++-arm-none-eabi-newlib libnewlib-arm-none-eabi build-essential cmake nano


WORKDIR /var/mmb
RUN git clone https://github.com/micropython/micropython.git /var/mmb/micropython
RUN cd micropython
RUN git submodule update --init lib/mbedtls


RUN cd micropython
RUN make -C mpy-cross
RUN cd ..