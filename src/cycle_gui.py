from trip_data import *
import fonts
import const
from gui_base import *
from display import *
import data_global as g
import s_avg
import s_hm
import s_time
import s_km

class CycleGui(GuiBase):
    def __init__(self, main):
        GuiBase.__init__(self, main)

    def get_title(self):
        return b'csc'

    def show(self, redraw):
        self.cache.reset(redraw)
        trip = self.trip
        cycling = self.cycling

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
        if self.cache.changed(DataCache.SPEED, speed) or self.cache.changed(DataCache.SPEED_COLOR, col):
            self.show_big_speed(speed, g.display.width, y, col)

    def show_cadence(self, trip, y):
        if self.cache.changed(DataCache.CADENCE, trip.cadence):
            g.display.draw_text(fonts.f_wide_normal, "%2d" % (trip.cadence), 0, y, align=Align.left)

    def show_id(self, trip):
        if trip.id != 1:
            if self.cache.changed(DataCache.TRIP_ID, trip.id):
                g.display.draw_text(fonts.f_narrow_small, "%d"%trip.id, 5, 0)

    def show_speed_avg(self, trip, y, col = Color.white):
        speed = round(trip.speed_avg, 1)
        if self.cache.changed(DataCache.SPEED_AVG, speed) or self.cache.changed(DataCache.SPEED_AVG_COLOR, col):
            self.show_float_speed(speed, g.display.width, y, color = col)

    def show_trip_distance(self, trip, y, narrow = False):
        distance = math.floor(trip.trip_distance*100) / 100
        #distance = math.floor(trip.trip_distance*10) / 10
        if self.cache.changed(DataCache.TRIP_DISTANCE, distance):
            self.show_float_speed(distance, g.display.width, y, narrow = narrow)

    def show_trip_duration(self, trip, x, y, font = fonts.f_wide_normal):
        val = trip.trip_duration_sec if trip.trip_duration_sec < 60 else trip.trip_duration_sec / 60
        if self.cache.changed(DataCache.TRIP_DURATION, trip.trip_duration_sec):
            self.show_float_time(val, x, y, font = font)

    def show_trip_alt(self, trip, y):
        if self.cache.changed(DataCache.TRIP_ALTITUDE, trip.altitude.sum):
            g.display.draw_text(fonts.f_wide_normal, "%d" % (trip.altitude.sum), g.display.width, y, align = Align.right)
