in="/media/stsc/data/work/micropython/apps/bikecomputer/signs"
out="/media/stsc/data/work/micropython/apps/bikecomputer/modules"

for file in "$in"/s*.png; do
  python3 ../tools/png2bitmap.py $file $out
done
