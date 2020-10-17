from data_csc import *
import fonts
import const
from gui_base import *
from a import *


class GuiCsc(GuiBase):
    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.shown_data = DataCsc(0)
        self.shown_data.invalidate_shown_data()

    def get_title(self):
        return "csc"


    def show(self, redraw_all):
        #print("show gui_csc")
        if redraw_all:
            self.main.clear()
            self.shown_data.invalidate_shown_data()

        data = self.main.get_csc_data()
        goal = data.goal if data.goal and data.goal.is_active else None

        y = 0

        if self.shown_data.id != data.id:
            self.main.text(fonts.middle, "%d"%data.id, 0, y)
            self.shown_data.id = data.id

        # current speed
        if self.shown_data.speed != data.speed:
            self.show_big_speed(data.speed, 64, y)
            self.shown_data.speed = data.speed

        # current cadence
        if self.shown_data.cadence != data.cadence:
            self.main.text(fonts.bign, "%2d" % (data.cadence), 0, y + fonts.giant.HEIGHT - fonts.bign.HEIGHT)
            self.shown_data.cadence = data.cadence

        y = 60

        # average speed
        if self.shown_data.speed_avg != data.speed_avg:
            self.show_float_speed(data.speed_avg, 75, y)
            self.shown_data.speed_avg = data.speed_avg

        if goal:
            self.show_float_speed(goal.calc_required_average_km_h, 0, y)

        y = 105

 #       data.trip_duration_min = 60*8+44
        #data.trip_distance = 44.4

        if goal:
            self.show_float_speed(goal.remaining_distance_km, 0, y)
            self.show_progress(y + 40, 8, goal.target_dist_km.value, goal.target_dist_km.value-goal.remaining_distance_km, goal.optimal_distance_km)

        # trip distance
        if self.shown_data.trip_distance != data.trip_distance:
            self.show_float_speed(data.trip_distance, 57+16, y)
            self.shown_data.trip_distance = data.trip_distance
            
        y += 52

        # goal remaining time
        if goal != None:
            self.show_float_time(goal.remaining_time_min, 0, y)

        # trip duration
        if self.shown_data.trip_duration_min != data.trip_duration_min:
            self.show_float_time(data.trip_duration_min, 57+16, y)
            self.shown_data.trip_duration_min = data.trip_duration_min

        y = Display.height- fonts.bign.HEIGHT

        # max speed
        if self.shown_data.speed_max != data.speed_max:
            self.show_float_speed(data.speed_max, 75, y, fonts.bign)
            self.shown_data.speed_max != data.speed_max

        #average cadence
        if self.shown_data.cadence_avg != data.cadence_avg:
            self.main.text(fonts.bign, "%2d" % (data.cadence_avg), 0, y)
            self.shown_data.cadence = data.cadence
            self.shown_data.cadence_avg = data.cadence_avg

        #self.main.tft.blit_buffer(PIC, 0, 0, 48, 48)

    
    def handle(self, id, long_click):
        #print("handler_csc")
        if long_click:
            self.main.go_menu_main()
        else:
            if id == const.Button.left:
                self.main.prev_csc()
            elif id == const.Button.right:
                self.main.next_csc()