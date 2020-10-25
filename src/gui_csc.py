from data_csc import *
import fonts
import const
from gui_base import *
#from a import *


class GuiCsc(GuiBase):
    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.shown_data = DataCsc(0)
        self.shown_data.invalidate_shown_data()
        self.second_view = False

    def get_title(self):
        return "csc"

    def show_id(self, data, y):
        if self.shown_data.id != data.id:
            self.main.text(fonts.middle, "%d"%data.id, 0, y)
            self.shown_data.id = data.id

    def show_speed(self, data, y):
        if self.shown_data.speed != data.speed:
            self.show_big_speed(data.speed, 64, y)
            self.shown_data.speed = data.speed

    def show_cadence(self, data, y):
        if self.shown_data.cadence != data.cadence:
            self.main.text(fonts.bign, "%2d" % (data.cadence), 0, y + fonts.giant.HEIGHT - fonts.bign.HEIGHT)
            self.shown_data.cadence = data.cadence

    def show_speed_avg(self, data, y):
        if self.shown_data.speed_avg != data.speed_avg:
            self.show_float_speed(data.speed_avg, 75, y)
            self.shown_data.speed_avg = data.speed_avg

    def show_speed_goal(self, goal, data, y):
        col = Color.green if goal.calc_required_average_km_h < data.speed_avg else Color.red
        self.show_float_speed(goal.calc_required_average_km_h, 0, y, color=col)

    def show_distance_goal(self, goal, y):
        self.show_float_speed(goal.remaining_distance_km, 0, y)

    def show_progress_goal(self, goal, y):
        self.show_progress(y + 40, 8, goal.target_dist_km.value, goal.target_dist_km.value-goal.remaining_distance_km, goal.optimal_distance_km)

    def show_time_goal(self, goal, y):
        self.show_float_time(goal.remaining_time_min, 0, y)

    def show_trip_distance(self, data, y):
        if self.shown_data.trip_distance != data.trip_distance:
            self.show_float_speed(data.trip_distance, 75, y)
            self.shown_data.trip_distance = data.trip_distance

    def show_trip_duration(self, data, y):
        if self.shown_data.trip_duration_min != data.trip_duration_min:
            self.show_float_time(data.trip_duration_min, 57+16, y)
            self.shown_data.trip_duration_min = data.trip_duration_min

    def show_speed_max(self, data, y):
        if self.shown_data.speed_max != data.speed_max:
            self.show_float_speed(data.speed_max, 75, y, fonts.huge)
            self.shown_data.speed_max != data.speed_max

    def show_cadence_avg(self, data, y):
        if self.shown_data.cadence_avg != data.cadence_avg:
            self.main.text(fonts.huge, "%2d" % (data.cadence_avg), 75, y)
            self.shown_data.cadence = data.cadence
            self.shown_data.cadence_avg = data.cadence_avg

    def show_title(self, txt, y):
        self.main.text_aligned(fonts.middle, txt, 3, y + fonts.huge.HEIGHT - fonts.middle.HEIGHT - 2, Align.left)

    def show(self, redraw_all):
        #print("show gui_csc")
        if redraw_all:
            self.main.clear()
            self.shown_data.invalidate_shown_data()

        data = self.main.get_csc_data()
        goal = data.goal if data.goal and data.goal.is_active else None
        if goal:
            goal.calculate_progress(data)

        y = 0
        y_1 = 65
        y_2 = y_1 + 50
        y_3 = y_2 + 55

        self.show_id(data, y)
        self.show_speed(data, y)
        self.show_cadence(data, y)

        self.show_speed_avg(data, y_1)

        if self.second_view:
            self.show_title("avg", y_1)
            self.show_title("kmh max", y_2)
            self.show_speed_max(data, y_2)
            self.show_title("cad avg", y_3)
            self.show_cadence_avg(data, y_3)

        else:
            self.show_trip_distance(data, y_2)
            self.show_trip_duration(data, y_3)

            if goal:
                self.show_speed_goal(goal, data,y_1)
                self.show_distance_goal(goal, y_2)
                self.show_progress_goal(goal, y_2)
                self.show_time_goal(goal, y_3)
            else:
                self.show_title("avg", y_1)
                self.show_title("km", y_2)
                self.show_title("h:m", y_3)

    
    def handle(self, id, long_click):
        #print("handler_csc")
        if long_click:
            if id == Button.right:
                self.main.go_menu_main()
            elif id == Button.left:
                self.second_view = not self.second_view
                self.main.show()
        else:
            if id == const.Button.left:
                self.main.prev_csc()
            elif id == const.Button.right:
                self.main.next_csc()