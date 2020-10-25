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
    
def write_bin(name, f, pixel_list):
    f.write("_img_%s = b'" % (name))
    for pix in pixel_list:
        r = (pix[0] >> 3) & 0x1F
        g = (pix[1] >> 2) & 0x3F
        b = (pix[2] >> 3) & 0x1F
        a = struct.pack('H', (r << 11) + (g << 5) + b)
        val = (r << 11) + (g << 5) + b
        f.write("\\x%.2x\\x%.2x" % (val>>8, val&0xff))
    f.write("'\n")
    f.write("img_%s = memoryview(_img_%s)" % (name, name))

##
if __name__ == '__main__':
    print("??")
    args = sys.argv
    if len(args) != 2: usage()
    in_path = args[1]
    #"/media/stsc/data/work/micropython/apps/bikecomputer/tools/a.png"
    if os.path.exists(in_path) == False: error('not exists: ' + in_path)
    
    name, _ = os.path.splitext(in_path)
    out_path = name + '.py'
    filename = Path(in_path).stem

    img = Image.open(in_path).convert('RGB')
    pixels = list(img.getdata())
    
    with open(out_path, 'w') as f:
        write_bin(filename, f, pixels)