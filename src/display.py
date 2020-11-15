import math
from const import *

class Display:
    width = 135
    height = 240
    def __init__(self, tft):
        self._tft = tft

    def draw_aligned_text_old(self, font, text, x, y, align = Align.left):
    
        if align == Align.left:
            pass
        else:
            w = len(text) * font.WIDTH    
            if align == Align.center:
                x = (int)((Display.width-w) / 2)
            else:
                x = Display.width - w - x
        self._tft.text(font, text, x, y, Color.white, Color.black)


    def draw_multi_line_old(self, font, text, y, align = Align.center):
        w = font.WIDTH * len(text)
        lines = math.ceil(w / Display.width)
        n = int(math.ceil(len(text) / lines))
        txt = [text[i:i+n] for i in range(0, len(text), n)]

        k=0
        for t in txt:
            self.draw_aligned_text(font, t, 0, y + k*font.HEIGHT, align)
            k += 1        

    def fill(self, color):
        self._tft.fill(color)

    def fill_rect(self, x, y, width, height, color):
        self._tft.fill_rect(x, y, width, height, color)


    def get_text_center_pos_old(self, font, n):
        space = 2
        w = n * (font.WIDTH + space)
        x = (int)((Display.width - w) / 2)
        return x

    # komoot sign
    def text(self, font, text, x, y, fg = Color.white, bg = Color.black):
        space = 2
        w = 0
        cx = 0

        if x < 0: # center
            x = self.get_text_center_pos(font, len(text))

        for char in text:
            ch = ord(char)
            if font.FIRST <= ch < font.LAST:
                self._tft.text(font, "%c" % char, x+cx, y, fg, bg)
                w = space
                cx += font.WIDTH
            else:
                w = font.WIDTH + space
            self.fill_rect(x+cx, y, w, font.HEIGHT, bg)
            cx += w

    def draw_text(self, font, txt, x, y, fg=Color.white, bg=Color.black, align=Align.left):
        text_width = 0
        if align == Align.right:
            #x = Display.width - x
            for ch in txt:
                _, _, width = font.get_ch(ch)
                x -= width
        elif align == Align.center:
            w = 0
            for ch in txt:
                _, _, width = font.get_ch(ch)
                w += width
            x = int((Display.width - w) / 2)

        for ch in txt:
            data, height, width = font.get_ch(ch)
            n = width * height
            buffer = bytearray(n*2)
            self._tft.map_bitarray_to_rgb565(data, buffer, width, fg, bg)
            self._tft.blit_buffer(buffer, x, y, width, height)
            x += width            

    def draw_text_multi(self, font, txt, x, y, fg=Color.white, bg=Color.black, align=Align.left):
        w = 0
        for ch in txt:
            _, _, width = font.get_ch(ch)
            w += width

        lines = math.ceil(w / Display.width)
        n = int(math.ceil(len(txt) / lines))
        txt = [txt[i:i+n] for i in range(0, len(txt), n)]
        h = 0
        for t in txt:
            self.draw_text(font, t, 0, y + h, fg, bg, align)
            h += font.height()        
