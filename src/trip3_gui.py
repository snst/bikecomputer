import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class Trip3Gui(GuiBase):
    y_speed = 0
    y_avg = 60
    y_distance = y_avg + 60
    y_time = y_distance + 46

    def __init__(self, main):
        GuiBase.__init__(self, main)

    def get_title(self):
        return b'trip3'

    def show(self, redraw):
        self.cache.reset(redraw)
        y = 0
        ys = fonts.f_wide_smaller.height() + 8
        trip = self.main.get_trip()
        i = 0
        #self.show_val(redraw, y + i*ys, "#", "%d" % (trip.id), i)
        #i += 1
        self.show_val(redraw, y + i*ys, "#%d" % (trip.id), "%.1f" % round(self.cycling.speed, 1), i)
        i += 1
        self.show_val(redraw, y + i*ys, "", "%.2f" % round(trip.trip_distance, 2), i)
        i += 1
        ms = trip.trip_duration_sec
        txt = "%.2d:%.2d:%.2d" % (ms/3600, (ms/60)% 60, ms % 60)
        self.show_val(redraw, y + i*ys, "", txt, i)

        i += 1
        ms = trip.trip_pause_sum_ms/1000
        txt = "%.2d:%.2d:%.2d" % (ms/3600, (ms/60)% 60, ms % 60)
        self.show_val(redraw, y + i*ys, "", txt, i)

        i += 1
        self.show_val(redraw, y + i*ys, "Alt", "%.1f" % (trip.altitude.sum), i)

    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_cycle_menu()
        else:
            GuiBase.handle(self, event)
