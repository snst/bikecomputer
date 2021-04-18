#mkdir ./esp-idf/
#cd ./esp-idf/
git clone -b v4.2 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
#git checkout 4c81978a3e2220674a432a588292a4c860eef27b 
## the above hash is defined by the variable ESPIDF_SUPHASH_V4 in the file:
# https://github.com/micropython/micropython/blob/master/ports/esp32/Makefile

git submodule update --init --recursive
## if you don't clone the submodules (recursive)
# you'll get the following error while compiling MicroPython: 
# xtensa-esp32-elf/bin/ld: cannot find -lrtc