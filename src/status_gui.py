import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class StatusGui(GuiBase):
    def __init__(self, main):
        GuiBase.__init__(self, main)
        g.bc.request_sensor_bat()
        g.bc.request_computer_bat()
        g.hal.gc_collect()

    def get_title(self):
        return b'status'

    def show(self, redraw):
        self.cache.reset(redraw)
        y = 0
        ys = fonts.f_wide_smaller.height() + 8
        env_data = g.bc._env_data
        env = self.main.env_data
        i = 0
        self.show_val(redraw, y + i*ys, "Lipo V", "%.2f" % (env.computer_bat_volt), i, 3)
        i += 1
        self.show_val(redraw, y + i*ys, "Bat %", "%d" % (env.sensor_bat_percent), i, 3)
        i += 1
        self.show_val(redraw, y + i*ys, "C", "%.1f" % (env_data.temperature), i, 3)
        i += 1
        #self.show_val(redraw, y + i*ys, "hPa", "%.1f" % (env_data.pressure), i)
        self.show_val(redraw, y + i*ys, "#m", "%d" % (self.cycling.msg_cnt), i, 5)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt", "%.1f" % (env_data.altitude), i, 5)
        i += 1
        self.show_val(redraw, y + i*ys, "Mem", "%u" % ((int)(g.hal.gc_mem_free() / 1024)), i, 4)

    def handle(self, event):
        GuiBase.handle(self, event)
