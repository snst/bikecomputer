import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class GuiAltitude(GuiBase):
    y_speed = 0
    y_avg = 60
    y_distance = y_avg + 60
    y_time = y_distance + 46

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache(8)
        self._cnt = 0

    def get_title(self):
        return "alt"

    def show(self, redraw_all):
        #print("show gui_csc")
        if redraw_all:
            self.cache.reset()

        self.clear()
        alt = g.bc._altimeter

        self._cnt += 1

        g.display.draw_text(fonts.pf_small, "cnt  %2d" % (self._cnt), 0, 10, align=Align.left)
        g.display.draw_text(fonts.pf_small, "temp %.2f" % (alt.temperature), 0, 40, align=Align.left)
        g.display.draw_text(fonts.pf_small, "pres %.2f" % (alt.pressure), 0, 70, align=Align.left)
        g.display.draw_text(fonts.pf_small, "alt  %.2f" % (alt.altitude), 0, 100, align=Align.left)
    
    def handle(self, event):
        GuiBase.handle(self, event)
