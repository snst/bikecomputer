d="$(dirname $(readlink -f $0))"
#source $d/venv/bin/activate
#export ESPIDF=$d/esp-idf
#export PATH="$d/toolchain/xtensa-esp32-elf/bin:$PATH"
#export IDF_PATH="$d/esp-idf"
#cd $d/micropython/mpy-cross
#make
#cd $d/micropython/ports/esp32
#source $d/esp-idf/export.sh
#make USER_C_MODULES=../../../st7789_mpy/ all

source $d/esp-idf/export.sh

if [ "$1" = "clean" ]
then
    cd $d/micropython/ports/esp32
    make clean
    exit 0
fi

if [ "$1" = "erase" ]
then
    cd $d/micropython/ports/esp32
    make erase
    exit 0
fi

if [ "$1" = "deploy" ]
then
    cd $d/micropython/ports/esp32
    make deploy
    exit 0
fi

cd $d/micropython/mpy-cross
make
cd $d/micropython/ports/esp32
make USER_C_MODULES=/home/stsc/bikecomputer5/bikecomputer/micropython/examples/usercmodule/micropython.cmake
