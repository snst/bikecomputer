from tkinter import *


import struct


BLACK = (0x0000)
BLUE = (0x001F)
RED = (0xF800)
GREEN = (0x07E0)
CYAN = (0x07FF)
MAGENTA = (0xF81F)
YELLOW = (0xFFE0)
WHITE = (0xFFFF)


_BUFFER_SIZE = (256)

_BIT7 = (0x80)
_BIT6 = (0x40)
_BIT5 = (0x20)
_BIT4 = (0x10)
_BIT3 = (0x08)
_BIT2 = (0x04)
_BIT1 = (0x02)
_BIT0 = (0x01)

def convert_color(val):
    if val==BLACK:
        return "black"
    elif val==BLUE:
        return "blue"
    elif val==RED:
        return "red"
    elif val==GREEN:
        return "green"
    elif val==CYAN:
        return "cyan"
    elif val==MAGENTA:
        return "magenta"
    elif val==YELLOW:
        return "yellow"
    else:
        return "white"


def color565(red, green=0, blue=0):
    """
    Convert red, green and blue values (0-255) into a 16-bit 565 encoding.
    """
    try:
        red, green, blue = red  # see if the first var is a tuple/list
    except TypeError:
        pass
    return (red & 0xf8) << 8 | (green & 0xfc) << 3 | blue >> 3


class ST7789:

    def __init__(self, spi, width, height, reset=None, cs=None, dc=None, backlight=None, rotation=None):
        self.width = width
        self.height = height
        self.tk = Tk()
        self.w = Canvas(self.tk, 
                width=width,
                height=height)
        self.w.pack()
        self.w.bind("<Button-1>", self.btn_down)
        self.w.bind("<ButtonRelease-1>", self.btn_up)
        self.btn_up_cb = None
        self.btn_down_cb = None
        pass


    def init(self):
        pass

    def get_btn_id(self, x, y):
        if x<self.width/2:
            return 0
        else:
            return 1

    def btn_down(self, event):
        #print("btn_down at %d %d" % (event.x, event.y))
        if self.btn_down_cb:
            self.btn_down_cb(self.get_btn_id(event.x, event.y))

    def btn_up(self, event):
        #print("btn_up at %d %d" % (event.x, event.y))
        if self.btn_up_cb:
            self.btn_up_cb(self.get_btn_id(event.x, event.y))

    def set_btn_callback(self, down, up):
        self.btn_down_cb = down
        self.btn_up_cb = up

    def fill(self, color):
        self.w.create_rectangle(0, 0, self.width, self.height, fill=convert_color(color))
        pass

    def pixel(self, x, y, color):
        self.w.create_line(x, y, x+1, y, fill=convert_color(color))
        pass

    def line(self, x0, y0, x1, y1, color):
        self.w.create_line(x0, y0, x1, y1, fill=convert_color(color))
        pass

    def hline(self, x, y, length, color):
        self.w.create_line(x, y, x+length, y, fill=convert_color(color))
        pass

    def vline(self, x, y, length, color):
        self.w.create_line(x, y, x, y+length, fill=convert_color(color))
        pass

    def rect(self, x, y, width, height, color):
        self.w.create_rectangle(x, y, x+width, y+height, outline=convert_color(color))
        pass

    def fill_rect(self, x, y, width, height, color):
        self.w.create_rectangle(x, y, x+width, y+height, fill=convert_color(color))
        pass

    #def text(self, font, s, x, y, fg=WHITE, bg=BLACK):
    #    self.w.create_text(x, y, anchor=W, font="Purisa", text=s)
    #    pass

    def width(self):
        return self.width

    def height(self):
        return self.height
        
    def mainloop(self):
        mainloop()

    def blit_buffer(self, buffer, x, y, width, height):
        """
        Copy buffer to display at the given location.
        Args:
            buffer (bytes): Data to copy to display
            x (int): Top left corner x coordinate
            Y (int): Top left corner y coordinate
            width (int): Width
            height (int): Height
        """
        i = 0
        n = len(buffer)
        xx=0
        yy=0
        while i<n:
            val = (buffer[i+1]) + (buffer[i]<<8)
            i+=2
            self.pixel(x+xx,y+yy,val)
            xx += 1
            if xx==width:
                xx = 0
                yy += 1


        #self.set_window(x, y, x + width - 1, y + height - 1)
        #self.write(None, buffer)

#from: https://github.com/russhughes/st7789py_mpy/blob/master/lib/st7789py.py
    def _text8(self, font, text, x0, y0, color=WHITE, background=BLACK):
        """
        Internal method to write characters with width of 8 and
        heights of 8 or 16.
        Args:
            font (module): font module to use
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        for char in text:
            ch = ord(char)
            if (font.FIRST <= ch < font.LAST
                    and x0+font.WIDTH <= self.width
                    and y0+font.HEIGHT <= self.height):

                if font.HEIGHT == 8:
                    passes = 1
                    size = 8
                    each = 0
                else:
                    passes = 2
                    size = 16
                    each = 8

                for line in range(passes):
                    idx = (ch-font.FIRST)*size+(each*line)
                    buffer = struct.pack('>64H',
                        color if font.FONT[idx] & _BIT7 else background,
                        color if font.FONT[idx] & _BIT6 else background,
                        color if font.FONT[idx] & _BIT5 else background,
                        color if font.FONT[idx] & _BIT4 else background,
                        color if font.FONT[idx] & _BIT3 else background,
                        color if font.FONT[idx] & _BIT2 else background,
                        color if font.FONT[idx] & _BIT1 else background,
                        color if font.FONT[idx] & _BIT0 else background,
                        color if font.FONT[idx+1] & _BIT7 else background,
                        color if font.FONT[idx+1] & _BIT6 else background,
                        color if font.FONT[idx+1] & _BIT5 else background,
                        color if font.FONT[idx+1] & _BIT4 else background,
                        color if font.FONT[idx+1] & _BIT3 else background,
                        color if font.FONT[idx+1] & _BIT2 else background,
                        color if font.FONT[idx+1] & _BIT1 else background,
                        color if font.FONT[idx+1] & _BIT0 else background,
                        color if font.FONT[idx+2] & _BIT7 else background,
                        color if font.FONT[idx+2] & _BIT6 else background,
                        color if font.FONT[idx+2] & _BIT5 else background,
                        color if font.FONT[idx+2] & _BIT4 else background,
                        color if font.FONT[idx+2] & _BIT3 else background,
                        color if font.FONT[idx+2] & _BIT2 else background,
                        color if font.FONT[idx+2] & _BIT1 else background,
                        color if font.FONT[idx+2] & _BIT0 else background,
                        color if font.FONT[idx+3] & _BIT7 else background,
                        color if font.FONT[idx+3] & _BIT6 else background,
                        color if font.FONT[idx+3] & _BIT5 else background,
                        color if font.FONT[idx+3] & _BIT4 else background,
                        color if font.FONT[idx+3] & _BIT3 else background,
                        color if font.FONT[idx+3] & _BIT2 else background,
                        color if font.FONT[idx+3] & _BIT1 else background,
                        color if font.FONT[idx+3] & _BIT0 else background,
                        color if font.FONT[idx+4] & _BIT7 else background,
                        color if font.FONT[idx+4] & _BIT6 else background,
                        color if font.FONT[idx+4] & _BIT5 else background,
                        color if font.FONT[idx+4] & _BIT4 else background,
                        color if font.FONT[idx+4] & _BIT3 else background,
                        color if font.FONT[idx+4] & _BIT2 else background,
                        color if font.FONT[idx+4] & _BIT1 else background,
                        color if font.FONT[idx+4] & _BIT0 else background,
                        color if font.FONT[idx+5] & _BIT7 else background,
                        color if font.FONT[idx+5] & _BIT6 else background,
                        color if font.FONT[idx+5] & _BIT5 else background,
                        color if font.FONT[idx+5] & _BIT4 else background,
                        color if font.FONT[idx+5] & _BIT3 else background,
                        color if font.FONT[idx+5] & _BIT2 else background,
                        color if font.FONT[idx+5] & _BIT1 else background,
                        color if font.FONT[idx+5] & _BIT0 else background,
                        color if font.FONT[idx+6] & _BIT7 else background,
                        color if font.FONT[idx+6] & _BIT6 else background,
                        color if font.FONT[idx+6] & _BIT5 else background,
                        color if font.FONT[idx+6] & _BIT4 else background,
                        color if font.FONT[idx+6] & _BIT3 else background,
                        color if font.FONT[idx+6] & _BIT2 else background,
                        color if font.FONT[idx+6] & _BIT1 else background,
                        color if font.FONT[idx+6] & _BIT0 else background,
                        color if font.FONT[idx+7] & _BIT7 else background,
                        color if font.FONT[idx+7] & _BIT6 else background,
                        color if font.FONT[idx+7] & _BIT5 else background,
                        color if font.FONT[idx+7] & _BIT4 else background,
                        color if font.FONT[idx+7] & _BIT3 else background,
                        color if font.FONT[idx+7] & _BIT2 else background,
                        color if font.FONT[idx+7] & _BIT1 else background,
                        color if font.FONT[idx+7] & _BIT0 else background
                    )
                    self.blit_buffer(buffer, x0, y0+8*line, 8, 8)

                x0 += 8



    def _text16(self, font, text, x0, y0, color=WHITE, background=BLACK):
        """
        Internal method to draw characters with width of 16 and heights of 16
        or 32.
        Args:
            font (module): font module to use
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        for char in text:
            ch = ord(char)
            if (font.FIRST <= ch < font.LAST
                    and x0+font.WIDTH <= self.width
                    and y0+font.HEIGHT <= self.height):

                if font.HEIGHT == 16:
                    passes = 2
                    size = 32
                    each = 16
                else:
                    passes = 4
                    size = 64
                    each = 16

                for line in range(passes):
                    idx = (ch-font.FIRST)*size+(each*line)
                    buffer = struct.pack('>128H',
                        color if font.FONT[idx] & _BIT7 else background,
                        color if font.FONT[idx] & _BIT6 else background,
                        color if font.FONT[idx] & _BIT5 else background,
                        color if font.FONT[idx] & _BIT4 else background,
                        color if font.FONT[idx] & _BIT3 else background,
                        color if font.FONT[idx] & _BIT2 else background,
                        color if font.FONT[idx] & _BIT1 else background,
                        color if font.FONT[idx] & _BIT0 else background,
                        color if font.FONT[idx+1] & _BIT7 else background,
                        color if font.FONT[idx+1] & _BIT6 else background,
                        color if font.FONT[idx+1] & _BIT5 else background,
                        color if font.FONT[idx+1] & _BIT4 else background,
                        color if font.FONT[idx+1] & _BIT3 else background,
                        color if font.FONT[idx+1] & _BIT2 else background,
                        color if font.FONT[idx+1] & _BIT1 else background,
                        color if font.FONT[idx+1] & _BIT0 else background,
                        color if font.FONT[idx+2] & _BIT7 else background,
                        color if font.FONT[idx+2] & _BIT6 else background,
                        color if font.FONT[idx+2] & _BIT5 else background,
                        color if font.FONT[idx+2] & _BIT4 else background,
                        color if font.FONT[idx+2] & _BIT3 else background,
                        color if font.FONT[idx+2] & _BIT2 else background,
                        color if font.FONT[idx+2] & _BIT1 else background,
                        color if font.FONT[idx+2] & _BIT0 else background,
                        color if font.FONT[idx+3] & _BIT7 else background,
                        color if font.FONT[idx+3] & _BIT6 else background,
                        color if font.FONT[idx+3] & _BIT5 else background,
                        color if font.FONT[idx+3] & _BIT4 else background,
                        color if font.FONT[idx+3] & _BIT3 else background,
                        color if font.FONT[idx+3] & _BIT2 else background,
                        color if font.FONT[idx+3] & _BIT1 else background,
                        color if font.FONT[idx+3] & _BIT0 else background,
                        color if font.FONT[idx+4] & _BIT7 else background,
                        color if font.FONT[idx+4] & _BIT6 else background,
                        color if font.FONT[idx+4] & _BIT5 else background,
                        color if font.FONT[idx+4] & _BIT4 else background,
                        color if font.FONT[idx+4] & _BIT3 else background,
                        color if font.FONT[idx+4] & _BIT2 else background,
                        color if font.FONT[idx+4] & _BIT1 else background,
                        color if font.FONT[idx+4] & _BIT0 else background,
                        color if font.FONT[idx+5] & _BIT7 else background,
                        color if font.FONT[idx+5] & _BIT6 else background,
                        color if font.FONT[idx+5] & _BIT5 else background,
                        color if font.FONT[idx+5] & _BIT4 else background,
                        color if font.FONT[idx+5] & _BIT3 else background,
                        color if font.FONT[idx+5] & _BIT2 else background,
                        color if font.FONT[idx+5] & _BIT1 else background,
                        color if font.FONT[idx+5] & _BIT0 else background,
                        color if font.FONT[idx+6] & _BIT7 else background,
                        color if font.FONT[idx+6] & _BIT6 else background,
                        color if font.FONT[idx+6] & _BIT5 else background,
                        color if font.FONT[idx+6] & _BIT4 else background,
                        color if font.FONT[idx+6] & _BIT3 else background,
                        color if font.FONT[idx+6] & _BIT2 else background,
                        color if font.FONT[idx+6] & _BIT1 else background,
                        color if font.FONT[idx+6] & _BIT0 else background,
                        color if font.FONT[idx+7] & _BIT7 else background,
                        color if font.FONT[idx+7] & _BIT6 else background,
                        color if font.FONT[idx+7] & _BIT5 else background,
                        color if font.FONT[idx+7] & _BIT4 else background,
                        color if font.FONT[idx+7] & _BIT3 else background,
                        color if font.FONT[idx+7] & _BIT2 else background,
                        color if font.FONT[idx+7] & _BIT1 else background,
                        color if font.FONT[idx+7] & _BIT0 else background,
                        color if font.FONT[idx+8] & _BIT7 else background,
                        color if font.FONT[idx+8] & _BIT6 else background,
                        color if font.FONT[idx+8] & _BIT5 else background,
                        color if font.FONT[idx+8] & _BIT4 else background,
                        color if font.FONT[idx+8] & _BIT3 else background,
                        color if font.FONT[idx+8] & _BIT2 else background,
                        color if font.FONT[idx+8] & _BIT1 else background,
                        color if font.FONT[idx+8] & _BIT0 else background,
                        color if font.FONT[idx+9] & _BIT7 else background,
                        color if font.FONT[idx+9] & _BIT6 else background,
                        color if font.FONT[idx+9] & _BIT5 else background,
                        color if font.FONT[idx+9] & _BIT4 else background,
                        color if font.FONT[idx+9] & _BIT3 else background,
                        color if font.FONT[idx+9] & _BIT2 else background,
                        color if font.FONT[idx+9] & _BIT1 else background,
                        color if font.FONT[idx+9] & _BIT0 else background,
                        color if font.FONT[idx+10] & _BIT7 else background,
                        color if font.FONT[idx+10] & _BIT6 else background,
                        color if font.FONT[idx+10] & _BIT5 else background,
                        color if font.FONT[idx+10] & _BIT4 else background,
                        color if font.FONT[idx+10] & _BIT3 else background,
                        color if font.FONT[idx+10] & _BIT2 else background,
                        color if font.FONT[idx+10] & _BIT1 else background,
                        color if font.FONT[idx+10] & _BIT0 else background,
                        color if font.FONT[idx+11] & _BIT7 else background,
                        color if font.FONT[idx+11] & _BIT6 else background,
                        color if font.FONT[idx+11] & _BIT5 else background,
                        color if font.FONT[idx+11] & _BIT4 else background,
                        color if font.FONT[idx+11] & _BIT3 else background,
                        color if font.FONT[idx+11] & _BIT2 else background,
                        color if font.FONT[idx+11] & _BIT1 else background,
                        color if font.FONT[idx+11] & _BIT0 else background,
                        color if font.FONT[idx+12] & _BIT7 else background,
                        color if font.FONT[idx+12] & _BIT6 else background,
                        color if font.FONT[idx+12] & _BIT5 else background,
                        color if font.FONT[idx+12] & _BIT4 else background,
                        color if font.FONT[idx+12] & _BIT3 else background,
                        color if font.FONT[idx+12] & _BIT2 else background,
                        color if font.FONT[idx+12] & _BIT1 else background,
                        color if font.FONT[idx+12] & _BIT0 else background,
                        color if font.FONT[idx+13] & _BIT7 else background,
                        color if font.FONT[idx+13] & _BIT6 else background,
                        color if font.FONT[idx+13] & _BIT5 else background,
                        color if font.FONT[idx+13] & _BIT4 else background,
                        color if font.FONT[idx+13] & _BIT3 else background,
                        color if font.FONT[idx+13] & _BIT2 else background,
                        color if font.FONT[idx+13] & _BIT1 else background,
                        color if font.FONT[idx+13] & _BIT0 else background,
                        color if font.FONT[idx+14] & _BIT7 else background,
                        color if font.FONT[idx+14] & _BIT6 else background,
                        color if font.FONT[idx+14] & _BIT5 else background,
                        color if font.FONT[idx+14] & _BIT4 else background,
                        color if font.FONT[idx+14] & _BIT3 else background,
                        color if font.FONT[idx+14] & _BIT2 else background,
                        color if font.FONT[idx+14] & _BIT1 else background,
                        color if font.FONT[idx+14] & _BIT0 else background,
                        color if font.FONT[idx+15] & _BIT7 else background,
                        color if font.FONT[idx+15] & _BIT6 else background,
                        color if font.FONT[idx+15] & _BIT5 else background,
                        color if font.FONT[idx+15] & _BIT4 else background,
                        color if font.FONT[idx+15] & _BIT3 else background,
                        color if font.FONT[idx+15] & _BIT2 else background,
                        color if font.FONT[idx+15] & _BIT1 else background,
                        color if font.FONT[idx+15] & _BIT0 else background
                    )
                    self.blit_buffer(buffer, x0, y0+8*line, 16, 8)
            x0 += font.WIDTH

    def text(self, font, text, x0, y0, color=WHITE, background=BLACK):
        """
        Draw text on display in specified font and colors. 8 and 16 bit wide
        fonts are supported.
        Args:
            font (module): font module to use.
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        if font.WIDTH == 8:
            self._text8(font, text, x0, y0, color, background)
        else:
            self._text16(font, text, x0, y0, color, background)        