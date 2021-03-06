import math
from const import *
import data_global as g

class Display:
    width = 135
    height = 240
    def __init__(self, tft):
        self._tft = tft
        #self.m = 0
        #self.buffer = bytearray(2900)

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

    # Nav sign
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

    def get_digit_width(self, font, text, digits):
        text_width = 0
        clear_width = 0
        chw0 = font.get_width(b'0')
        w0 = 0
        for ch in text:
            if isinstance(ch, int):
                ch = chr(ch)
            width = font.get_width(ch)
            text_width += width

            if (ch == ':' or ch == '.'):
                w0 += width
        if digits > 0:
            w0 += digits * chw0
            clear_width = w0 - text_width
        return text_width, clear_width


    def draw_text(self, font, txt, x, y, fg=Color.white, bg=Color.black, align=Align.left, digits=0):
        text_width, clear_width = self.get_digit_width(font, txt, digits)
        x0 = None

        if align == Align.right:
            x -= text_width
            x0 = max(0, x - clear_width)
        elif align == Align.center:
            x = int((Display.width - text_width) / 2)
        else:
            x0 = x + text_width
            pass

        if None != x0 and 0 < clear_width:
            self._tft.fill_rect(x0, y, clear_width, font.height(), Color.black)

        for ch in txt:
            if isinstance(ch, int):
                ch = chr(ch)
            data, height, width = font.get_ch(ch)
            self._tft.blit_bitarray(data, width, x, y, fg, bg)
            x += width
        return text_width  

    def draw_text_old(self, font, txt, x, y, fg=Color.white, bg=Color.black, align=Align.left, htrim=True):
        text_width = 0
        chw0 = font.get_width(b'0')
        w0 = 0
        for ch in txt:
            if isinstance(ch, int):
                ch = chr(ch)
            width = font.get_width(ch)
            text_width += width
            if (ch >= '0' and ch <= '9') or ch == ' ':
                w0 += chw0
            else:
                w0 += width
        w0 = w0 - text_width
        x0 = None

        if align == Align.right:
            x -= text_width
            x0 = x - w0
        elif align == Align.center:
            x = int((Display.width - text_width) / 2)
        else:
            x0 = x + text_width
            pass

        if None != x0 and 0 < w0:
            self._tft.fill_rect(x0, y, w0, font.height(), Color.black)

        for ch in txt:
            if isinstance(ch, int):
                ch = chr(ch)
            data, height, width = font.get_ch(ch)
            self._tft.blit_bitarray(data, width, x, y, fg, bg)
            x += width            


    def draw_text_multi(self, font, txt, x, y, fg=Color.white, bg=Color.black, align=Align.left):
        if align == Align.center_sep:
            txt = txt.split(b';')
            align = Align.center
        else:
            w = 0
            for ch in txt:
                w += font.get_width(ch)

            lines = math.ceil(w / Display.width)
            n = int(math.ceil(len(txt) / lines))
            txt = [txt[i:i+n] for i in range(0, len(txt), n)]

        h = 0
        for t in txt:
            self.draw_text(font, t, 0, y + h, fg, bg, align)
            h += font.height()        

    def bitmap_blit(self, x, y, bitmap, fg=Color.white, bg=Color.black):
        self._tft.blit_bitarray(bitmap.BITMAP, bitmap.WIDTH, x, y, fg, bg)
        pass