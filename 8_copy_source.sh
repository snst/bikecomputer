d="$(dirname $(readlink -f $0))"

dest="$d/micropython/ports/esp32/modules/"

cp -rf $d/modules/*.py $dest
cp -rf $d/src/*.py $dest
echo "cp $d to $dest"