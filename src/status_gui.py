import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class StatusGui(GuiBase):

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache()
        g.bc.request_sensor_bat()
        g.bc.request_computer_bat()
        g.hal.gc_collect()


    def get_title(self):
        return b'status'

#    def show_val(self, redraw, y, str, val, i):
#        if redraw:
#            g.display.draw_text(fonts.f_narrow_small, str , 0, y, align=Align.left)
#        if self.cache.changed(i, val):
#            g.display.draw_text(fonts.f_narrow_small, val, g.display.width, y, align=Align.right)

    def show(self, redraw):
        y = 0
        ys = fonts.f_wide_smaller.height() + 8
        altimter = g.bc._altimeter
        if redraw:
            self.cache.reset()
        i = 0
        self.show_val(redraw, y + i*ys, "Lipo V", "%.2f" % (g.bc.env_data.computer_bat_volt), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Bat %", "%d" % (g.bc.env_data.sensor_bat_percent), i)
        i += 1
        self.show_val(redraw, y + i*ys, "C", "%.1f" % (altimter.temperature), i)
        i += 1
        self.show_val(redraw, y + i*ys, "hPa", "%.1f" % (altimter.pressure), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt", "%.1f" % (altimter.altitude), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Mem", "%u" % (g.hal.gc_mem_free()), i)


    def handle(self, event):
        GuiBase.handle(self, event)
