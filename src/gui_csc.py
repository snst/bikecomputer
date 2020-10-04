from data_csc import *
import fonts
import const

class GuiCsc:
    rh = 40
    def __init__(self, main):
        self.main = main
        self.shown_data = DataCsc(0)
        pass

    def get_title(self):
        return "csc"

    def show(self, redraw_all):
        #print("show gui_csc")

        csc_data = self.main.get_csc_data()

        self.main.tft.text(fonts.small, "%d" % (csc_data.id), 1, 1)

        if redraw_all or self.shown_data.speed != csc_data.speed:
            self.main.tft.text(fonts.big, "%4.1f" % (csc_data.speed), 48, 0*self.rh)
            self.shown_data.speed = csc_data.speed


        if redraw_all or self.shown_data.speed_avg != csc_data.speed_avg:
            self.main.tft.text(fonts.middle, "avg", 10, 1*self.rh+13)
            self.main.tft.text(fonts.big, "%4.1f" % (csc_data.speed_avg), 48, 1*self.rh)
            self.shown_data.speed_avg = csc_data.speed_avg

        if redraw_all or self.shown_data.speed_max != csc_data.speed_max:
            self.main.tft.text(fonts.middle, "max", 10, 2*self.rh+13)
            self.main.tft.text(fonts.big, "%4.1f" % (csc_data.speed_max), 48, 2*self.rh)
            self.shown_data.speed_max != csc_data.speed_max

        if redraw_all or self.shown_data.cadence != csc_data.cadence or self.shown_data.cadence_avg != csc_data.cadence_avg:
            self.main.tft.text(fonts.big, "%3d %3d" % (csc_data.cadence, csc_data.cadence_avg), 5, 3*self.rh)
            self.shown_data.cadence = csc_data.cadence
            self.shown_data.cadence_avg = csc_data.cadence_avg

        #if self.shown_data.cadence_avg != csc_data.cadence_avg:
        #    self.main.tft.text(fonts.big, "%d" % (csc_data.cadence_avg), 5, 3*self.rh)
        #    self.shown_data.cadence_avg = csc_data.cadence_avg

        if redraw_all or self.shown_data.trip_distance != csc_data.trip_distance:
            self.main.tft.text(fonts.big, "%6.2f" % (csc_data.trip_distance), 16, 4*self.rh)
            self.shown_data.trip_distance = csc_data.trip_distance
            

        if redraw_all or self.shown_data.trip_duration != csc_data.trip_duration:
            h = csc_data.trip_duration / 60
            m = csc_data.trip_duration % 60
            self.main.tft.text(fonts.big, "%2d:%.2d" % (h, m), 32, 5*self.rh)
            self.shown_data.trip_duration = csc_data.trip_duration
    
    def handle(self, id, long_click):
        #print("handler_csc")
        if long_click:
            self.main.go_menu_main()
        else:
            if id == const.Button.left:
                self.main.prev_csc()
            elif id == const.Button.right:
                self.main.next_csc()