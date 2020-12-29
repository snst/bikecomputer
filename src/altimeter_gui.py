import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class AltimeterGui(GuiBase):
    y_speed = 0
    y_avg = 60
    y_distance = y_avg + 60
    y_time = y_distance + 46

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache()
        #self._cnt = 0

    def get_title(self):
        return b'alt'

    def show(self, redraw):
        y = 0
        ys = fonts.f_wide_smaller.height() + 8
        data = self.main.get_csc_data()
        altimter = g.bc._altimeter
        alt = self.main.get_current_meter().alt_data
        if redraw:
            self.cache.reset()
        i = 0
        self.show_val(redraw, y + i*ys, "Id", "%d" % (data.id), i)
        i += 1
        self.show_val(redraw, y + i*ys, "km/h", "%.1f" % (round(data.speed_max, 1)), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Cadence", "%d" % (data.cadence), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Avg cad", "%d" % (data.cadence_avg), i)
        i += 1
#        self.show_val(redraw, y + i*ys, "Alt", "%.1f m" % (altimter.altitude), i)
#        i += 1
#        self.show_val(redraw, y + i*ys, "Alt min", "%.1f m" % (alt.min), i)
#        i += 1
#        self.show_val(redraw, y + i*ys, "Alt max", "%.1f m" % (alt.max), i)
#        i += 1
        self.show_val(redraw, y + i*ys, "Alt", "%.1f" % (alt.sum), i)
        i += 1
        ya = y + i * ys
        if self.cache.changed(i, (int)(alt.min)):
            g.display.draw_text(fonts.f_wide_smaller, "%d" % (alt.min), (int)(g.display.width/2), ya, align=Align.right)
        #i += 1
        #if self.cache.changed(i, (int)(altimter.altitude)):
        #    g.display.draw_text(fonts.f_narrow_small, "%d" % (altimter.altitude), (int)(g.display.width/3*2), ya, align=Align.right)
        i += 1
        if self.cache.changed(i, (int)(alt.max)):
            g.display.draw_text(fonts.f_wide_smaller, "%d" % (alt.max), (int)(g.display.width), ya, align=Align.right)
        
    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_cycle_menu()
        else:
            GuiBase.handle(self, event)
