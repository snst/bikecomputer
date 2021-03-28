import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class Trip2Gui(GuiBase):
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
        #self.show_val(redraw, y + i*ys, "#", "%d" % (trip.id), i)
        #i += 1
        self.show_val(redraw, y + i*ys, "%d-Max" % (trip.id), "%.1f" % (round(trip.speed_max, 1)), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Cadence", "%d" % (self.main.cycling.cadence), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Cad-0", "%d" % (trip.cadence_avg), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt-L", "%.1f" % (trip.altitude.min), i)
        i += 1
        self.show_val(redraw, y + i*ys, "Alt-H", "%.1f" % (trip.altitude.max), i)
        
    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_cycle_menu()
        else:
            GuiBase.handle(self, event)
