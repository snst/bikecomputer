#echo "pwd: `pwd`"
#echo "\$0: $0"
#echo "basename: `basename $0`"
#echo "dirname: `dirname $0`"
#echo "dirname/readlink: $(dirname $(readlink -f $0))"

d="$(dirname $(readlink -f $0))"

in="$d/signs"
out="$d/modules"

#echo "$in"

for file in "$in"/s*.png; do
  python3 $d/tools/png2bitmap.py $file $out
done

for file in "$in"/k*.png; do
  python3 $d/tools/png2bitmap.py $file $out
done
