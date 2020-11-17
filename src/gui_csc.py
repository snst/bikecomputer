from data_csc import *
import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class GuiCsc(GuiBase):
    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache(8)
        self.second_view = False

    def get_title(self):
        return "csc"

    def show_id(self, data):
        if self.cache.changed(0, data.id):
            g.display.draw_text(fonts.pf_small, "%d"%data.id, 2, Display.height-fonts.pf_small.height() + 3)

    def show_speed(self, data, y):
        if self.cache.changed(1, data.speed):
            col = Color.white
            if data.goal and data.goal.is_started:
                col = Color.red if data.goal.calc_required_average_km_h > data.speed else Color.green

            self.show_big_speed(data.speed, g.display.width, y, col)

    def show_cadence(self, data, y):
        if self.cache.changed(2, data.cadence):
            g.display.draw_text(fonts.pf_normal, "%2d" % (data.cadence), 0, y, align=Align.left)

    def show_speed_avg(self, data, y):
        if self.cache.changed(3, data.speed_avg):
            col = Color.white
            if data.goal and data.goal.is_started:
                col = Color.red if data.goal.is_behind(data) else Color.green

            self.show_float_speed(data.speed_avg, g.display.width, y, color = col)

    def show_speed_goal(self, goal, data, y):
        #col = Color.green if goal.calc_required_average_km_h < data.speed_avg else Color.red
        col = Color.white
        self.show_float_speed(goal.calc_required_average_km_h, 0, y, color=col, align = Align.left, font = fonts.pf_narrow)

    def show_speed_final(self, goal, y):
        self.show_float_speed(goal.calc_required_average_km_h, 0, y, color=Color.blue, align = Align.left)

    def show_distance_goal(self, data, y):
        self.show_float_speed(data.remaining_distance_km, 0, y, align = Align.left, font = fonts.pf_narrow)

    def show_progress_goal(self, goal, y):
        self.show_progress(y - 12, 8, goal.target_dist_km.value, goal.target_dist_km.value-goal.remaining_distance_km, goal.optimal_distance_km)

    def show_time_goal(self, goal, y):
        self.show_float_time(goal.remaining_time_min, 0, y, align = Align.left, font = fonts.pf_narrow)

    def show_trip_distance(self, data, y):
        if self.cache.changed(4, data.trip_distance):
            self.show_float_speed(data.trip_distance, g.display.width, y)

    def show_trip_duration(self, data, y):
        if self.cache.changed(5, data.trip_duration_min):
            self.show_float_time(data.trip_duration_min, g.display.width, y)

    def show_speed_max(self, data, y):
        if self.cache.changed(6, data.speed_max):
            self.show_float_speed(data.speed_max, g.display.width, y)

    def show_cadence_avg(self, data, y):
        if self.cache.changed(7, data.cadence_avg):
            g.display.draw_text(fonts.pf_normal, "%2d" % (data.cadence_avg), g.display.width, y, align=Align.right)

    def show_title(self, txt, y):
        g.display.draw_text(fonts.pf_small, txt, 3, y + fonts.pf_normal.height() - fonts.pf_small.height() - 10, align=Align.left)

    def show(self, redraw_all):
        #print("show gui_csc")
        if redraw_all:
            self.main.clear()
            self.cache.reset()

        data = self.main.get_csc_data()
        goal = data.goal if data.goal and data.goal.is_started else None
        if goal:
            goal.calculate_progress(data)

        y = 0
        y_1 = 65
        y_2 = y_1 + 60
        y_3 = y_2 + 50
        y_goal = 5

        #self.show_id(data)
        self.show_speed(data, y)
        self.show_cadence(data, y_1)

        self.show_speed_avg(data, y_1)

        if self.second_view:
            #self.show_title("avg", y_1)
            self.show_title("max", y_2)
            self.show_speed_max(data, y_2)
            self.show_title("cad avg", y_3)
            self.show_cadence_avg(data, y_3)

        else:
            self.show_trip_distance(data, y_2)
            self.show_trip_duration(data, y_3)

            if goal:
                if not goal.has_distance_reached:
                    self.show_speed_goal(goal, data, y_goal)
                    pass
                else:
                    self.show_speed_final(goal, y_goal)
                self.show_distance_goal(goal, y_2)
                self.show_progress_goal(goal, y_2)
                self.show_time_goal(goal, y_3)
            else:
                #self.show_title("avg", y_1)
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
                self.main.show_komoot()
            elif id == const.Button.right:
                self.main.next_csc()