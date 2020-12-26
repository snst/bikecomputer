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
    
def write_bin(name, f, img, first_ch, number_ch):

    pixels = list(img.getdata())
    ch_width = (int)(img.width / number_ch)
    ch_height = img.height

    f.write("WIDTH = %d\n" \
            "HEIGHT = %d\n" \
            "FIRST = %d\n" \
            "LAST = %d\n" \
            "_FONT = \\\nb'" % (ch_width, ch_height, first_ch, first_ch + number_ch) )

    i = 0
    val = 0
    k = 0
    
    for i_ch in range(0, number_ch):
        for h in range(0, ch_height):
            for w in range(0, ch_width):
                pix = pixels[i_ch*ch_width+w+h*img.width]
                b = 1 if (pix[0] == 0 and pix[1] == 0 and pix[2] == 0) else 0
                val = val | b
                if k < 7:
                    val = val << 1
                    k += 1
                else:
                    f.write("\\x%.2x" % (val&0xFF))
                    val = 0
                    k = 0
        i = i_ch * ch_width * ch_height
    f.write("'\n")
    f.write("FONT = memoryview(_FONT)\n")


##
if __name__ == '__main__':
    print("??")
    args = sys.argv
    #if len(args) != 2: usage()
    #in_path = args[1]
    na = "komoot_96"
    in_path = "/media/stsc/data/work/micropython/apps/bikecomputer/newfont/"+na+".png"
    if os.path.exists(in_path) == False: error('not exists: ' + in_path)
    
    name, _ = os.path.splitext(in_path)
    out_path = name + '.py'
    filename = Path(in_path).stem

    img = Image.open(in_path).convert('RGB')
    out_path = "/media/stsc/data/work/micropython/apps/bikecomputer/src/"+na+".py"
    with open(out_path, 'w') as f:
        write_bin(filename, f, img, 46, 28)