from cycle_data import *
import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class CycleGui(GuiBase):

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache()
        self._font = fonts.pf_normal

    def get_title(self):
        return b'csc'

    def show(self, redraw):
        if redraw:
            self.cache.reset()

        data = self.main.get_csc_data()
        alt_data = self.main.get_current_meter().alt_data

        yd = 46
        y_speed = 0
        y_avg = 58
        y_distance = y_avg + yd
        y_time = y_distance + yd
        y_alt = y_time + yd

        self.show_id(data)
        self.show_speed_big(data, y_speed)
        #self.show_cadence(data, self.y_avg)

        self.show_speed_avg(data, y_avg)

        self.show_trip_distance(data, y_distance)
        self.show_trip_duration(data, y_time)
        self.show_trip_alt(alt_data, y_alt)

        self.show_desc(b'avg', y_avg)
        self.show_desc(b'km', y_distance)
        self.show_desc(b'h:m', y_time)
        self.show_desc(b'hm', y_alt)

    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_cycle_menu()
        else:
            GuiBase.handle(self, event)

    def show_speed_big(self, data, y):
        speed = round(data.speed, 1)
        col = Color.white
        if data.goal and data.goal.is_started:
            col = Color.red if data.goal.calc_required_average_km_h > speed else Color.green
        if self.cache.changed(1, speed) or self.cache.changed(2, col):
            self.show_big_speed(speed, g.display.width, y, col)

    def show_speed(self, data, y):
        speed = round(data.speed, 1)
        col = Color.white
        if data.goal and data.goal.is_started:
            col = Color.red if data.goal.calc_required_average_km_h > speed else Color.green
        if self.cache.changed(1, speed) or self.cache.changed(2, col):
            self.show_float_speed(speed, g.display.width, y, color = col, font = self._font)

    def show_cadence(self, data, y):
        if self.cache.changed(3, data.cadence):
            g.display.draw_text(fonts.pf_normal, "%2d" % (data.cadence), 0, y, align=Align.left)

    def show_id(self, data):
        if self.cache.changed(0, data.id):
            g.display.draw_text(fonts.pf_small, "%d"%data.id, 5, 0)

    def show_speed_avg(self, data, y):
        speed = round(data.speed_avg, 1)
        col = Color.white
        if data.goal and data.goal.is_started:
            col = Color.red if data.goal.is_behind() else Color.green
        if self.cache.changed(4, speed) or self.cache.changed(5, col):
            self.show_float_speed(speed, g.display.width, y, color = col, font = self._font)

    def show_trip_distance(self, data, y):
        distance = round(data.trip_distance, 1)
        if self.cache.changed(6, distance):
            self.show_float_speed(distance, g.display.width, y, font = self._font)

    def show_trip_duration(self, data, y):
        if self.cache.changed(7, data.trip_duration_min):
            self.show_float_time(data.trip_duration_min, g.display.width, y, font = self._font)

    def show_trip_alt(self, data, y):
        if self.cache.changed(15, data.sum):
            g.display.draw_text(fonts.pf_normal, "%d" % (data.sum), g.display.width, y, align = Align.right)
