#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import struct, os, sys
from pathlib import Path

def usage():
    print ('./png2bitmap.py theimage.png')
    sys.exit(1)
    
def error(msg):
    print(msg)
    sys.exit(-1)

def write_bin_bit(f, img):
    pixels = list(img.getdata())

    f.write("WIDTH = %d\n" \
            "HEIGHT = %d\n" \
            "_BITMAP = \\\nb'" % (img.width, img.height) )

    val = 0
    k = 0
    
    for h in range(0, img.height):
        for w in range(0, img.width):
            pix = pixels[w + h * img.width]
            b = 0 if (pix[0] == 255 and pix[1] == 255 and pix[2] == 255) else 1
            val = val | b
            if k < 7:
                val = val << 1
                k += 1
            else:
                f.write("\\x%.2x" % (val&0xFF))
                val = 0
                k = 0
        r = img.width % 8
        if r > 0:
            val = val << (8-r)
            f.write("\\x%.2x" % (val&0xFF))
            val = 0
            k = 0

    f.write("'\n")
    f.write("BITMAP = memoryview(_BITMAP)\n")


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3: usage()
    in_path = args[1]
    out_path = args[2]
    #print("%s %s" %(in_path, out_path))
    #in_path = "/media/stsc/data/work/micropython/apps/bikecomputer/signs/k3.png"
    #out_path = "/media/stsc/data/work/micropython/apps/bikecomputer/modules"

    if os.path.exists(in_path) == False: error('not exists: ' + in_path)
    
    name = os.path.basename(in_path)
    name, _ = os.path.splitext(name)
    out_path = os.path.join(out_path, name + '.py')

    print("in: %s  out: %s" %(in_path, out_path))

    img = Image.open(in_path).convert('RGB')
   
    with open(out_path, 'w') as f:
        write_bin_bit(f, img)        