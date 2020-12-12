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

    def get_title(self):
        return "status"

    def show_val(self, redraw, y, str, val, i):
        if redraw:
            g.display.draw_text(fonts.pf_small, str , 0, y, align=Align.left)
        if self.cache.changed(i, val):
            g.display.draw_text(fonts.pf_small, val, g.display.width, y, align=Align.right)

    def show(self, redraw):
        y = 0
        ys = fonts.pf_small.height()
        data = self.main.get_csc_data()
        alt = g.bc._altimeter
        if redraw:
            self.cache.reset()
        i = 0
        self.show_val(redraw, y + i*ys, "Comp bat", "%.2f V" % (g.bc.computer_bat), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Bike bat", "%d %%" % (g.bc.sensor_bat), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Max km/h", "%.1f" % (round(data.speed_max, 1)), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Avg cadence", "%d" % (data.cadence_avg), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Temp", "%.1f C" % (alt.temperature), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Pressure", "%.1f hPa" % (alt.pressure), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt", "%.1f m" % (alt.altitude), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt min", "%.1f m" % (alt.altitude_min), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt max", "%.1f m" % (alt.altitude_max), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt sum", "%.1f m" % (alt.altitude_sum), i)

        """if redraw_all:
            self.cache.reset()
            g.display.draw_text(fonts.pf_small, "Computer bat" , 0, y, align=Align.left)
            y += ys
            g.display.draw_text(fonts.pf_small, "Bike bat" , 0, y, align=Align.left)
            y += ys
            g.display.draw_text(fonts.pf_small, "Max km/h" , 0, y, align=Align.left)
            y += ys
            g.display.draw_text(fonts.pf_small, "Avg cadence" , 0, y, align=Align.left)

        data = self.main.get_csc_data()

        y = 0
        if self.cache.changed(0, g.bc.computer_bat):
            g.display.draw_text(fonts.pf_small, "%.2fV" % (g.bc.computer_bat), g.display.width, y, align=Align.right)
        
        y += ys
        if self.cache.changed(1, g.bc.sensor_bat):
            g.display.draw_text(fonts.pf_small, "%d%%" % (g.bc.sensor_bat), g.display.width, y, align=Align.right)
        
        y += ys
        val = round(data.speed_max, 1)
        if self.cache.changed(2, val):
            g.display.draw_text(fonts.pf_small, "%.1f" % (val), g.display.width, y, align=Align.right)

        y += ys
        val = data.cadence_avg
        if self.cache.changed(3, data.cadence_avg):
            g.display.draw_text(fonts.pf_small, "%d" % (val), g.display.width, y, align=Align.right)"""


    def handle(self, event):
        GuiBase.handle(self, event)
