import pygame
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))


import struct


BLACK = 0
WHITE = 1
GREY = 2
RED = 3

_BUFFER_SIZE = (256)

_BIT7 = (0x80)
_BIT6 = (0x40)
_BIT5 = (0x20)
_BIT4 = (0x10)
_BIT3 = (0x08)
_BIT2 = (0x04)
_BIT1 = (0x02)
_BIT0 = (0x01)


def color565(red, green=0, blue=0):
    """
    Convert red, green and blue values (0-255) into a 16-bit 565 encoding.
    """
    try:
        red, green, blue = red  # see if the first var is a tuple/list
    except TypeError:
        pass
    return (red & 0xf8) << 8 | (green & 0xfc) << 3 | blue >> 3

def colorRGB(val):
    r = ((((val >> 11) & 0x1F) * 527) + 23) >> 6
    g = ((((val >> 5) & 0x3F) * 259) + 33) >> 6
    b = (((val & 0x1F) * 527) + 23) >> 6
    return (r,g,b)

class ST7789:

    def __init__(self, spi, width, height, reset=None, cs=None, dc=None, backlight=None, rotation=None):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.btn_up_cb = None
        self.btn_down_cb = None
        self.display_brightness = 10
        self.gui = None
        pass


    def init(self):
        pass

    def convert_color(self, color):
        return color
        if color == BLACK:
            return (0, 0, 0)
        elif color == WHITE:
            v = 55 + 20 * self.display_brightness
            return (v, v, v) 
        elif color == RED:
            v = 55 + 20 * self.display_brightness
            return (v, 0, 0) 
        elif color == GREY:
            return (100, 100, 100)
        else:
            return (255,255,0)

    def convert_color_565(self, color):
        col = self.convert_color(color)
        return color565(col[0], col[1], col[2])


    def set_brightness(self, val):
        repaint = self.display_brightness != val
        self.display_brightness = val
        if repaint:
            print("LED %d" % (val))
        #if repaint and self.gui != None:
        #    self.gui.show()

    def set_gui(self, gui):
        self.gui = gui

    def get_btn_id(self, key):
        if key == pygame.K_a:
            return 0
        elif key == pygame.K_s:
            return 1
        else:
            return 2

    def btn_down(self, event):
        #print("btn_down at %d %d" % (event.x, event.y))
        if self.btn_down_cb:
            self.btn_down_cb(self.get_btn_id(event))

    def btn_up(self, event):
        #print("btn_up at %d %d" % (event.x, event.y))
        if self.btn_up_cb:
            self.btn_up_cb(self.get_btn_id(event))

    def set_btn_callback(self, down, up):
        self.btn_down_cb = down
        self.btn_up_cb = up

    def fill(self, color):
        #self.w.create_rectangle(0, 0, self.width, self.height, fill=convert_color(color))
        #self.screen.fill(BLACK)
        c = 20 - (20 / 10 * self.display_brightness)
        self.screen.fill((c,c,c))
        pass

    def pixel(self, x, y, color):
        #self.w.create_line(x, y, x+1, y, fill=convert_color(color))
        pygame.draw.line(self.screen, self.convert_color(color), (x,y), (x,y))
        pass

    def pixel2(self, x, y, color):
        #self.w.create_line(x, y, x+1, y, fill=convert_color(color))
        pygame.draw.line(self.screen, colorRGB(color), (x,y), (x,y))
        pass

    def line(self, x0, y0, x1, y1, color):
        #self.w.create_line(x0, y0, x1, y1, fill=convert_color(color))
        pass

    def hline(self, x, y, length, color):
        #self.w.create_line(x, y, x+length, y, fill=convert_color(color))
        pass

    def vline(self, x, y, length, color):
        #self.w.create_line(x, y, x, y+length, fill=convert_color(color))
        pass

    def rect(self, x, y, width, height, color):
        #self.w.create_rectangle(x, y, x+width, y+height, outline=convert_color(color))
        pass

    def fill_rect(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, colorRGB(color), (x, y, width, height))
        #self.w.create_rectangle(x, y, x+width, y+height, fill=convert_color(color))
        pass

    #def text(self, font, s, x, y, fg=WHITE, bg=BLACK):
    #    self.w.create_text(x, y, anchor=W, font="Purisa", text=s)
    #    pass

    def width(self):
        return self.width

    def height(self):
        return self.height
        

    def update(self):
        pygame.display.update()



    def blit_buffer(self, buffer, x, y, width, height):
        
        i = 0
        n = width*height*2 #len(buffer)
        xx=0
        yy=0
        while i<n:
            val = (buffer[i+1]) + (buffer[i+0]<<8)
            i+=2
            self.pixel2(x+xx,y+yy,val)
            xx += 1
            if xx==width:
                xx = 0
                yy += 1


    def blit_buffer_font(self, buffer, x, y, width, height):
        
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
                    self.blit_buffer_font(buffer, x0, y0+8*line, 8, 8)

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
                    self.blit_buffer_font(buffer, x0, y0+8*line, 16, 8)
            x0 += font.WIDTH

    def _text24(self, font, text, x0, y0, color=WHITE, background=BLACK):
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

                if font.HEIGHT == 48:
                    passes = 6
                    size = 32
                    each = 24
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
                    self.blit_buffer_font(buffer, x0, y0+8*line, 16, 8)
            x0 += font.WIDTH

    def text_o(self, font, text, x0, y0, color=WHITE, background=BLACK):
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
        if font.WIDTH == 16:
            self._text16(font, text, x0, y0, color, background)        
        else:
            self._text24(font, text, x0, y0, color, background)                    

    def text(self, font, text, x0, y0, fg, bg):
        n = font.WIDTH * font.HEIGHT
        buffer = bytearray(n*2)
        cx = 0
        #fg = self.convert_color_565(color)
        #bg = self.convert_color_565(background)

        for char in text:
            i = 0
            ch = ord(char)
            idx = (int)((ch-font.FIRST)*(n/8))
            if font.FIRST <= ch < font.LAST:
                bit = (0x80)
                wp = 0
                while i < n: # loop pixel
                    f = font.FONT[idx]
                    col = fg if ((f & bit) > 0) else bg
                    if bit == 1:
                        bit = (0x80) 
                        idx += 1
                    else:
                        bit = bit >> 1
                    buffer[i*2] = (col >> 8) & 0xFF
                    buffer[i*2+1] = (col) & 0xFF
                    i += 1
#                    wp += 1
#                    if wp == font.WIDTH
                self.blit_buffer(buffer, x0+cx, y0, font.WIDTH, font.HEIGHT)
                cx += font.WIDTH
            else:
                self.rect(x0+cx, y0, font.WIDTH, font.HEIGHT, bg)
                self.blit_buffer(buffer, x0+cx, y0, font.WIDTH, font.HEIGHT)
                cx += font.WIDTH



    def bitblt(self, font, w, h, ch, x0, y0, fg, bg):
        n = w * h
        buffer = bytearray(n*2)
        i = 0
        idx = 0
        bit = (0x80)
        wp = 0
        x = 0
        y = 0
        while i < n: # loop pixel
            f = font[idx]
            col = fg if ((f & bit) > 0) else bg
            if bit == 1:
                bit = (0x80) 
                idx += 1
            else:
                bit = bit >> 1
            k = (y*w+x)*2
            buffer[k] = (col >> 8) & 0xFF
            buffer[k+1] = (col) & 0xFF
            i += 1
            y += 1
            if y == h:
                y = 0
                x += 1

        self.blit_buffer(buffer, x0, y0, w, h)


    def font_blt(self, font, ch, x, y, fg, bg):
        data, height, width = font.get_ch(ch)
        n = width * height
        k = 0
        buffer = bytearray(n*2)
        for row in range(height):
            bytes_per_col = (height - 1)//8 + 1
            for col in range(width):
                byte = data[col * bytes_per_col + row//8]
                bit = (byte & (1 << (row % 8))) > 0
                col = fg if bit else bg
                buffer[k] = (col >> 8) & 0xFF
                buffer[k+1] = (col) & 0xFF
                k += 2

        self.blit_buffer(buffer, x, y, width, height)

    def map_bitarray_to_rgb565(self, bitarray, buffer, width, fg, bg):
        #height2 = int(len(buffer) / width / 2)
        n = len(bitarray) * 8
        w = int(width / 8) * 8
        if (width % 8) != 0:
            w += 8
        height = int(n / w)
        k = 0
        for row in range(height):
            bytes_per_row = (width - 1)//8 + 1
            for col in range(width):
                byte = bitarray[row * bytes_per_row + col // 8]
                bit = (byte & (1 << (7 - (col % 8)))) > 0
                col = fg if bit else bg
                buffer[k] = (col >> 8) & 0xFF
                buffer[k+1] = (col) & 0xFF
                k += 2
