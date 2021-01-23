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

    def get_title(self):
        return b'alt'

    def show(self, redraw):
        self.cache.reset(redraw)
        y = 0
        ys = fonts.f_wide_smaller.height() + 8
        trip = self.main.get_trip()
        i = 0
        self.show_val(redraw, y + i*ys, "Id", "%d" % (trip.id), i)
        i += 1
        self.show_val(redraw, y + i*ys, "km/h", "%.1f" % (round(trip.speed_max, 1)), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Cadence", "%d" % (self.main.cycling.cadence), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Avg cad", "%d" % (trip.cadence_avg), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt", "%.1f" % (trip.alt_data.sum), i)
        i += 1
        ya = y + i * ys
        if self.cache.changed(i, (int)(trip.alt_data.min)):
            g.display.draw_text(fonts.f_wide_smaller, "%d" % (trip.alt_data.min), (int)(g.display.width/2), ya, align=Align.right)
        i += 1
        if self.cache.changed(i, (int)(trip.alt_data.max)):
            g.display.draw_text(fonts.f_wide_smaller, "%d" % (trip.alt_data.max), (int)(g.display.width), ya, align=Align.right)
        
    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_cycle_menu()
        else:
            GuiBase.handle(self, event)
