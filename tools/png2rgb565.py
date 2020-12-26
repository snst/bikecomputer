#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import struct, os, sys
from pathlib import Path

def usage():
    print ('./png2rgb565.py theimage.png')
    sys.exit(1)
    
def error(msg):
    print(msg)
    sys.exit(-1)
    
def write_bin_565(name, f, img):
    pixels = list(img.getdata())

    f.write("_img_%s = b'" % (name))
    for pix in pixels:
        r = (pix[0] >> 3) & 0x1F
        g = (pix[1] >> 2) & 0x3F
        b = (pix[2] >> 3) & 0x1F
        a = struct.pack('H', (r << 11) + (g << 5) + b)
        val = (r << 11) + (g << 5) + b
        f.write("\\x%.2x\\x%.2x" % (val>>8, val&0xff))
    f.write("'\n")
    f.write("img_%s = memoryview(_img_%s)" % (name, name))

def write_bin_bit(name, f, img):
    pixels = list(img.getdata())

    f.write("WIDTH = %d\n" \
            "HEIGHT = %d\n" \
            "_BITMAP = \\\nb'" % (img.width, img.height) )

    val = 0
    k = 0
    
    for h in range(0, img.height):
        for w in range(0, img.width):
            pix = pixels[w + h * img.width]
            b = 1 if (pix[0] == 0 and pix[1] == 0 and pix[2] == 0) else 0
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
            val = val << r
            f.write("\\x%.2x" % (val&0xFF))
            val = 0
            k = 0

    f.write("'\n")
    f.write("BITMAP = memoryview(_BITMAP)\n")


if __name__ == '__main__':
    args = sys.argv
    #if len(args) != 2: usage()
    #in_path = args[1]
    in_path = "/media/stsc/data/work/micropython/apps/bikecomputer/tools/k3.png"
    if os.path.exists(in_path) == False: error('not exists: ' + in_path)
    
    name, _ = os.path.splitext(in_path)
    out_path = name + '.py'
    filename = Path(in_path).stem

    img = Image.open(in_path).convert('RGB')
   
    with open(out_path, 'w') as f:
        #write_bin_565(filename, f, pixels)
        write_bin_bit(filename, f, img)        