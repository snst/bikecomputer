in="/media/stsc/data/work/micropython/apps/bikecomputer/signs"
out="/media/stsc/data/work/micropython/apps/bikecomputer/modules"

for file in "$in"/s*.png; do
  python3 ./png2bitmap.py $file $out
done
