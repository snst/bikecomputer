from trip_data import *
import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *
from cycle_gui import *


class GoalGui(CycleGui):
    goal_x = 0
    def __init__(self, main):
        CycleGui.__init__(self, main)

    def get_title(self):
        return b'goal'

    def show(self, redraw):
        self.cache.reset(redraw)
        data = g.bc._goal_data
        cycling = self.main.cycling

        y_speed = 0
        y_avg = 60
        y_distance = y_avg + 70
        y_time = y_distance + 55
        y_goal = y_avg

        data.calculate_progress()

        col = Color.white
        if data.is_started:
            col = Color.red if data.calc_required_average_km_h > cycling.speed else Color.green
        self.show_speed_big(cycling.speed, y_speed, col)

        col = Color.white
        if data.is_started:
            col = Color.red if data.is_behind else Color.green
        self.show_speed_avg(data, y_avg, col)
        self.show_trip_distance(data, y_distance, narrow = True)
        self.show_trip_duration(data, g.display.width, y_time, font = fonts.f_narrow_text)

        if not data.is_finished:
            self.show_speed_goal(data, y_goal)

        if self.cache.changed(DataCache.GOAL_FINISHED, data.is_finished):
            if data.is_finished:
                g.display.fill_rect(0, y_goal, (int)(g.display.width/2), fonts.f_narrow_normal.height(), Color.black)


        self.show_distance_goal(data, y_distance)
        self.show_progress_goal(data, y_distance-3)
        self.show_time_goal(data, y_time)


    def handle(self, event = 0):
        if event == (Button.right | Button.long):
            self.main.show_goal_menu()
        else:
            GuiBase.handle(self, event)

    def show_speed_goal(self, data, y):
        speed = round(data.calc_required_average_km_h, 1)
        if self.cache.changed(DataCache.GOAL_REQUIRED_AVG_SPEED, speed):
            self.show_float_speed(speed, self.goal_x, y, color=Color.white, align = Align.left, narrow = True)


    def show_distance_goal(self, data, y):
        distance = round(data.remaining_distance_km, 1)
        if self.cache.changed(DataCache.GOAL_REMAINING_DISTANCE, distance):
            self.show_float_speed(distance, self.goal_x, y, align = Align.left, narrow = True)

    def show_time_goal(self, data, y):
        val = data.remaining_time_sec if data.remaining_time_sec < 60 else data.remaining_time_sec / 60
        if self.cache.changed(DataCache.GOAL_REMAINING_TIME, val):
            self.show_float_time(val, 0, y, align = Align.left, font = fonts.f_narrow_text)

    def show_progress_goal(self, data, y):
        max_val = round(data.target_dist_km.value, 1)
        val = round(data.target_dist_km.value-data.remaining_distance_km, 1)
        marker = round(data.optimal_distance_km, 1)
        updt = self.cache.changed(DataCache.GOAL_PROGRESS_MAX, max_val)
        updt = self.cache.changed(DataCache.GOAL_PROGRESS_VAL, val) or updt
        updt = self.cache.changed(DataCache.GOAL_PROGRESS_MARKER, marker) or updt
        if updt:
            self.show_progress(y - 12, 8, max_val, val, marker)
