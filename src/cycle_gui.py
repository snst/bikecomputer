from cycle_data import *
import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class CycleGui(GuiBase):
    y_speed = 0
    y_avg = 60
    y_distance = y_avg + 60
    y_time = y_distance + 46
    y_goal = 5


    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache(8)

    def get_title(self):
        return "csc"

    def show(self, redraw_all):
        #print("show cycle_gui")
        if redraw_all:
            self.cache.reset()

        data = self.main.get_csc_data()
        goal = data.goal if data.goal and data.goal.is_started else None
        if goal:
            goal.calculate_progress(data)


        self.show_id(data)
        self.show_speed(data, self.y_speed)
        self.show_cadence(data, self.y_avg)

        self.show_speed_avg(data, self.y_avg)

        self.show_trip_distance(data, self.y_distance)
        self.show_trip_duration(data, self.y_time)

        if goal:
            if not goal.has_distance_reached:
                self.show_speed_goal(goal, data, self.y_goal)
                pass
            else:
                self.show_speed_final(goal, self.y_goal)
            self.show_distance_goal(goal, self.y_distance)
            self.show_progress_goal(goal, self.y_distance)
            self.show_time_goal(goal, self.y_time)
        else:
            #self.show_desc("avg", self.y_avg)
            self.show_desc("km", self.y_distance)
            self.show_desc("h:m", self.y_time)

    
    def handle(self, event = 0):
        GuiBase.handle(self, event)
