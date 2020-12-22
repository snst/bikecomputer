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

    def show_val(self, redraw, y, str, val, i):
        if redraw:
            g.display.draw_text(fonts.pf_small, str , 0, y, align=Align.left)
        if self.cache.changed(i, val):
            g.display.draw_text(fonts.pf_small, val, g.display.width, y, align=Align.right)

    def show(self, redraw):
        y = 0
        ys = fonts.pf_small.height()
        data = self.main.get_csc_data()
        altimter = g.bc._altimeter
        alt = self.main.get_current_meter().alt_data
        if redraw:
            self.cache.reset()
        i = 0
        self.show_val(redraw, y + i*ys, "Id", "%d" % (data.id), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Max km/h", "%.1f" % (round(data.speed_max, 1)), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Cadence", "%d" % (data.cadence), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Avg cadence", "%d" % (data.cadence_avg), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt", "%.1f m" % (altimter.altitude), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt min", "%.1f m" % (alt.min), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt max", "%.1f m" % (alt.max), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt sum", "%.1f m" % (alt.sum), i)
        
    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_cycle_menu()
        else:
            GuiBase.handle(self, event)
