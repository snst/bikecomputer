from cycle_data import *
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

        data = self.main.get_csc_data()
        alt_data = self.main.get_current_meter().alt_data

        yd = 46
        y_speed = 0
        y_avg = 58
        y_distance = y_avg + yd
        y_time = y_distance + yd
        y_alt = y_time + yd

        self.show_id(data)
        self.show_speed_big(data, y_speed, col=Color.white if data.is_riding else Color.red)
        #self.show_cadence(data, self.y_avg)

        self.show_speed_avg(data, y_avg)

        self.show_trip_distance(data, y_distance)
        self.show_trip_duration(data, g.display.width, y_time)
        self.show_trip_alt(alt_data, y_alt)

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

    def show_speed_big(self, data, y, col=Color.white):
        speed = round(data.speed, 1)
        if self.cache.changed(1, speed) or self.cache.changed(2, col):
            self.show_big_speed(speed, g.display.width, y, col)

    def show_cadence(self, data, y):
        if self.cache.changed(3, data.cadence):
            g.display.draw_text(fonts.f_wide_normal, "%2d" % (data.cadence), 0, y, align=Align.left)

    def show_id(self, data):
        if data.id != 1:
            if self.cache.changed(0, data.id):
                g.display.draw_text(fonts.f_narrow_small, "%d"%data.id, 5, 0)

    def show_speed_avg(self, data, y, col = Color.white):
        speed = round(data.speed_avg, 1)
        if self.cache.changed(4, speed) or self.cache.changed(5, col):
            self.show_float_speed(speed, g.display.width, y, color = col)

    def show_trip_distance(self, data, y, narrow = False):
        distance = round(data.trip_distance, 1)
        if self.cache.changed(6, distance):
            self.show_float_speed(distance, g.display.width, y, narrow = narrow)

    def show_trip_duration(self, data, x, y, font = fonts.f_wide_normal):
        if self.cache.changed(7, data.trip_duration_min):
            self.show_float_time(data.trip_duration_min, x, y, font = font)

    def show_trip_alt(self, data, y):
        if self.cache.changed(15, data.sum):
            g.display.draw_text(fonts.f_wide_normal, "%d" % (data.sum), g.display.width, y, align = Align.right)
