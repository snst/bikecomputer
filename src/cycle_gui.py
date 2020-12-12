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


    def __init__(self, main, style):
        GuiBase.__init__(self, main)
        self.cache = DataCache()
        self._style = style

    def get_title(self):
        return "csc"

    def show(self, redraw_all):
        #print("show cycle_gui")
        if redraw_all:
            self.cache.reset()

        if self._style == 0:
            self.show0()
        else:
            self.show1()

    def show0(self):
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


    def show1(self):
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


    def show_speed(self, data, y):
        speed = round(data.speed, 1)
        col = Color.white
        if data.goal and data.goal.is_started:
            col = Color.red if data.goal.calc_required_average_km_h > speed else Color.green
        if self.cache.changed(1, speed) or self.cache.changed(2, col):
            self.show_big_speed(speed, g.display.width, y, col)

    def show_cadence(self, data, y):
        if self.cache.changed(3, data.cadence):
            g.display.draw_text(fonts.pf_normal, "%2d" % (data.cadence), 0, y, align=Align.left)

    def show_id(self, data):
        if self.cache.changed(0, data.id):
            g.display.draw_text(fonts.pf_small, "%d"%data.id, g.display.width - 25, g.display.height-fonts.pf_small.height())

    def show_speed_avg(self, data, y):
        speed = round(data.speed_avg, 1)
        col = Color.white
        if data.goal and data.goal.is_started:
            col = Color.red if data.goal.is_behind(data) else Color.green
        if self.cache.changed(4, speed) or self.cache.changed(5, col):
            self.show_float_speed(speed, g.display.width, y, color = col)

    def show_trip_distance(self, data, y):
        distance = round(data.trip_distance, 1)
        if self.cache.changed(6, distance):
            self.show_float_speed(distance, g.display.width, y)

    def show_trip_duration(self, data, y):
        if self.cache.changed(7, data.trip_duration_min):
            self.show_float_time(data.trip_duration_min, g.display.width, y)

    def show_speed_goal(self, goal, data, y):
        speed = round(data.calc_required_average_km_h, 1)
        if self.cache.changed(8, speed):
            self.show_float_speed(speed, 0, y, color=Color.white, align = Align.left)

    def show_speed_final(self, goal, y):
        if self.cache.changed(9, goal.calc_required_average_km_h):
            self.show_float_speed(goal.calc_required_average_km_h, 0, y, color=Color.blue, align = Align.left)

    def show_distance_goal(self, data, y):
        distance = round(data.remaining_distance_km, 1)
        if self.cache.changed(10, distance):
            self.show_float_speed(distance, 0, y, align = Align.left)

    def show_time_goal(self, goal, y):
        if self.cache.changed(11, goal.remaining_time_min):
            self.show_float_time(goal.remaining_time_min, 0, y, align = Align.left)

    def show_progress_goal(self, goal, y):
        max_val = round(goal.target_dist_km.value, 1)
        val = round(goal.target_dist_km.value-goal.remaining_distance_km, 1)
        marker = round(goal.optimal_distance_km, 1)
        updt = self.cache.changed(12, max_val)
        updt = self.cache.changed(13, val) or updt
        updt = self.cache.changed(14, marker) or updt
        if updt:
            self.show_progress(y - 12, 8, max_val, val, marker)
