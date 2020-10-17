from data_csc import *
import fonts
from const import *

class GuiBase:
    x_desc = 6
    x_val = 35
    rh = 30
    def __init__(self, main):
        self.main = main


    def show_desc(self, txt, y):
        if txt:
            self.main.tft.text(fonts.middle, txt, self.x_desc, y+13, Color.white, Color.black)

    def show_progress(self, y, h, max, val, marker=-1):
        if val > max:
            val = max
        p = 0
        m = 0
        if max > 0:
            p = (int)(135 / max * val)
            m = (int)(135 / max * marker)
        self.main.tft.fill_rect(0, y, 135, h, Color.grey)
        if p > m:
            self.main.tft.fill_rect(0, y, p, h, Color.green)
            self.main.tft.fill_rect(0, y, m, h, Color.yellow)
        else:
            self.main.tft.fill_rect(0, y, m, h, Color.red)
            self.main.tft.fill_rect(0, y, p, h, Color.green)
        #if marker > 0:
            #self.main.tft.fill_rect(0, y, m, 5, Color.red)



    def show_float_speed(self, val, x, y, font = fonts.huge):
        if val > 999:
            val = 999
        if val < 0:
            val = 0
        ival = (int) (val)
        dval = (int)((val - ival)*10)
        self.main.tft.fill_rect(x, y, 3*font.WIDTH+10, font.HEIGHT, Color.black)
        if val < 100:
            self.main.text(font, "%2d" % (ival), x, y)
            x += 2 * font.WIDTH
            self.main.text(font, "%d" % (dval), x + 10, y)
            self.main.tft.fill_rect(x + 3, y + font.HEIGHT - 5, 4, 5, Color.white)
        else:
            self.main.text(font, "%3d" % (ival), x + 10, y)

    def show_float_time(self, val, x, y):
        h = (int)(val / 60)
        m = val % 60
        font = fonts.huge
        self.main.text(font, "%1d" % (h), x, y)
        x += 1 * font.WIDTH
        self.main.text(font, "%.2d" % (m), x + 10, y)
        self.main.tft.fill_rect(x + 3, y + font.HEIGHT - 20, 4, 5, Color.white)
        self.main.tft.fill_rect(x + 3, y + font.HEIGHT - 7, 4, 5, Color.white)


    def show_big_speed(self, val, x, y):
        ival = (int) (val)
        dval = (int)((val - ival)*10)
        self.main.text(fonts.giant, "%2d" % (ival), x, y)
        self.main.text(fonts.huge, "%d" % (dval), x+2*fonts.giant.WIDTH+5, y)

    def show_float_3(self, val, x, y, font = fonts.font16):
        ival = (int)(val)
        dval = (int)((val-ival)*10)
        #self.main.tft.text(font, ".", x+40, y)
        self.main.tft.text(font, "%2d" % (ival), x, y)
        self.main.tft.text(font, "%d" % (dval), x+37, y)
        self.main.tft.pixel(x+35, y+24, 1)
        self.main.tft.pixel(x+36, y+24, 1)
        self.main.tft.pixel(x+35, y+25, 1)
        self.main.tft.pixel(x+36, y+25, 1)
        


    def show_float_1(self, txt, val, x, y, font = fonts.big):
        self.show_desc(txt, y)
        self.main.tft.text(font, "%4.1f" % (val), x, y)

    def show_float_2(self, txt, val, x, y):
        self.show_desc(txt, y)
        self.main.tft.text(fonts.big, "%6.2f" % (val), x, y)

    def show_duration(self, txt, minutes, x, y):
        self.show_desc(txt, y)
        h = minutes / 60
        m = minutes % 60
        self.main.tft.text(fonts.big, "%3d:%.2d" % (h, m), x, y)
