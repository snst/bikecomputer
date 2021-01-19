d="$(dirname $(readlink -f $0))"

mkdir fonts
cd fonts
wget https://dl.dafont.com/dl/?f=libel_suit -O libel.zip
unzip libel.zip
wget https://fonts.google.com/download?family=Oswald -O oswald.zip
unzip oswald.zip

A="$d/fonts/libel-suit-rg.ttf"
B="$d/fonts/Oswald-VariableFont_wght.ttf"
out="$d/modules"
gen="$d/tools/font_to_py.py"

$gen -x "$B" 52 "$out/f_wide_big.py" -c 0123456789:. -e 32
$gen -x "$B" 40 "$out/f_wide_normal.py" -c 0123456789:. -e 32
$gen -x "$B" 32 "$out/f_wide_smaller.py" -c 0123456789.: -e 32
$gen -x "$A" 42 "$out/f_narrow_normal.py" -c 0123456789:. -e 32
$gen -x "$A" 30 "$out/f_narrow_small.py"
$gen -x "$A" 47 "$out/f_narrow_text.py" -c abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.:-+ -e 32

#../start.sh
