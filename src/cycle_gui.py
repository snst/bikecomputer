from trip_data import *
import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *
import s_avg
import s_hm
import s_time
import s_km

class CycleGui(GuiBase):

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache()

    def get_title(self):
        return b'csc'

    def show(self, redraw):
        if redraw:
            self.cache.reset()

        trip = self.main.get_trip()
        cycling = self.main.cycling

        yd = 46
        y_speed = 0
        y_avg = 58
        y_distance = y_avg + yd
        y_time = y_distance + yd
        y_alt = y_time + yd

        self.show_id(trip)
        self.show_speed_big(cycling.speed, y_speed, col=Color.white if cycling.is_riding else Color.red)
        #self.show_cadence(trip, self.y_avg)

        self.show_speed_avg(trip, y_avg)

        self.show_trip_distance(trip, y_distance)
        self.show_trip_duration(trip, g.display.width, y_time)
        self.show_trip_alt(trip, y_alt)

        #self.show_desc(b'avg', y_avg)
        #self.show_desc(b'km', y_distance)
        #self.show_desc(b'h:m', y_time)
        #self.show_desc(b'hm', y_alt)
        self.show_icon(s_avg, y_avg)
        self.show_icon(s_hm, y_alt)
        self.show_icon(s_time, y_time)
        self.show_icon(s_km, y_distance)

    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_cycle_menu()
        else:
            GuiBase.handle(self, event)

    def show_speed_big(self, speed, y, col=Color.white):
        if self.cache.changed(1, speed) or self.cache.changed(2, col):
            self.show_big_speed(speed, g.display.width, y, col)

    def show_cadence(self, trip, y):
        if self.cache.changed(3, trip.cadence):
            g.display.draw_text(fonts.f_wide_normal, "%2d" % (trip.cadence), 0, y, align=Align.left)

    def show_id(self, trip):
        if trip.id != 1:
            if self.cache.changed(0, trip.id):
                g.display.draw_text(fonts.f_narrow_small, "%d"%trip.id, 5, 0)

    def show_speed_avg(self, trip, y, col = Color.white):
        speed = round(trip.speed_avg, 1)
        if self.cache.changed(4, speed) or self.cache.changed(5, col):
            self.show_float_speed(speed, g.display.width, y, color = col)

    def show_trip_distance(self, trip, y, narrow = False):
        distance = round(trip.trip_distance, 1)
        if self.cache.changed(6, distance):
            self.show_float_speed(distance, g.display.width, y, narrow = narrow)

    def show_trip_duration(self, trip, x, y, font = fonts.f_wide_normal):
        if self.cache.changed(7, trip.trip_duration_min):
            self.show_float_time(trip.trip_duration_min, x, y, font = font)

    def show_trip_alt(self, trip, y):
        if self.cache.changed(15, trip.alt_data.sum):
            g.display.draw_text(fonts.f_wide_normal, "%d" % (trip.alt_data.sum), g.display.width, y, align = Align.right)
