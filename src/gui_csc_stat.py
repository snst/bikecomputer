from cycle_data import *
import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class GuiCscStat(GuiBase):
    y_speed = 0
    y_avg = 60
    y_distance = y_avg + 60
    y_time = y_distance + 46

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache(8)

    def get_title(self):
        return "stat"

    def show(self, redraw_all):
        #print("show cycle_gui")
        if redraw_all:
            self.cache.reset()

        data = self.main.get_csc_data()

        self.show_id(data)
        self.show_speed(data, self.y_speed)
        self.show_cadence(data, self.y_avg)

        self.show_speed_avg(data, self.y_avg)

        self.show_desc("max", self.y_distance)
        self.show_speed_max(data, self.y_distance)
        self.show_desc("cad avg", self.y_time)
        self.show_cadence_avg(data, self.y_time)

    
    def handle(self, event = 0):
        GuiBase.handle(self, event)
