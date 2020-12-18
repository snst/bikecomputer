from cycle_data import *
import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *
from cycle_gui import *


class GoalGui(CycleGui):

    def __init__(self, main):
        CycleGui.__init__(self, main)
        self._font = fonts.f_narrow_n
        

    def get_title(self):
        return "goal"

    def show(self, redraw):
        if redraw:
            self.cache.reset()

        alt_data = self.main.get_current_meter().alt_data
        data = g.bc._goal_meter.cycle_data
        goal = data.goal        

        yd = 48
        y_speed = 0
        y_avg = 58
        y_distance = y_avg + 70
        y_time = y_distance + yd
        y_alt = y_time + yd
        y_goal = y_avg

        goal.calculate_progress(data)

        self.show_id(data)
        self.show_speed_big(data, y_speed)
        #self.show_cadence(data, self.y_avg)

        self.show_speed_avg(data, y_avg)

        self.show_trip_distance(data, y_distance)
        self.show_trip_duration(data, y_time)

        if not goal.has_distance_reached:
            self.show_speed_goal(goal, data, y_goal)
            pass
        else:
            self.show_speed_final(goal, y_goal)
        self.show_distance_goal(goal, y_distance)
        self.show_progress_goal(goal, y_distance-3)
        self.show_time_goal(goal, y_time)


    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_goal_menu()
        else:
            GuiBase.handle(self, event)

    def show_speed_goal(self, goal, data, y):
        speed = round(goal.calc_required_average_km_h, 1)
        if self.cache.changed(8, speed):
            self.show_float_speed(speed, 0, y, color=Color.white, align = Align.left, font = self._font)

    def show_speed_final(self, goal, y):
        if self.cache.changed(9, goal.calc_required_average_km_h):
            self.show_float_speed(goal.calc_required_average_km_h, 0, y, color=Color.blue, align = Align.left, font = self._font)

    def show_distance_goal(self, data, y):
        distance = round(data.remaining_distance_km, 1)
        if self.cache.changed(10, distance):
            self.show_float_speed(distance, 0, y, align = Align.left, font = self._font)

    def show_time_goal(self, goal, y):
        if self.cache.changed(11, goal.remaining_time_min):
            self.show_float_time(goal.remaining_time_min, 0, y, align = Align.left, font = self._font)

    def show_progress_goal(self, goal, y):
        max_val = round(goal.target_dist_km.value, 1)
        val = round(goal.target_dist_km.value-goal.remaining_distance_km, 1)
        marker = round(goal.optimal_distance_km, 1)
        updt = self.cache.changed(12, max_val)
        updt = self.cache.changed(13, val) or updt
        updt = self.cache.changed(14, marker) or updt
        if updt:
            self.show_progress(y - 12, 8, max_val, val, marker)
