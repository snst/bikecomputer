import bike_data
import fonts

class GuiCsc:
    rh = 40
    def __init__(self, main):
        self.main = main
        self.shown_data = bike_data.BikeData()
        pass

    def get_title(self):
        return "csc"

    def show(self, redraw_all):
        #print("show gui_csc")

        if redraw_all or self.shown_data.speed != self.main.data.speed:
            self.main.tft.text(fonts.big, "%4.1f" % (self.main.data.speed), 48, 0*self.rh)
            self.shown_data.speed = self.main.data.speed


        if redraw_all or self.shown_data.speed_avg != self.main.data.speed_avg:
            self.main.tft.text(fonts.middle, "avg", 10, 1*self.rh+13)
            self.main.tft.text(fonts.big, "%4.1f" % (self.main.data.speed_avg), 48, 1*self.rh)
            self.shown_data.speed_avg = self.main.data.speed_avg

        if redraw_all or self.shown_data.speed_max != self.main.data.speed_max:
            self.main.tft.text(fonts.middle, "max", 10, 2*self.rh+13)
            self.main.tft.text(fonts.big, "%4.1f" % (self.main.data.speed_max), 48, 2*self.rh)
            self.shown_data.speed_max != self.main.data.speed_max

        if redraw_all or self.shown_data.cadence != self.main.data.cadence or self.shown_data.cadence_avg != self.main.data.cadence_avg:
            self.main.tft.text(fonts.big, "%3d %3d" % (self.main.data.cadence, self.main.data.cadence_avg), 5, 3*self.rh)
            self.shown_data.cadence = self.main.data.cadence
            self.shown_data.cadence_avg = self.main.data.cadence_avg

        #if self.shown_data.cadence_avg != self.main.data.cadence_avg:
        #    self.main.tft.text(fonts.big, "%d" % (self.main.data.cadence_avg), 5, 3*self.rh)
        #    self.shown_data.cadence_avg = self.main.data.cadence_avg

        if redraw_all or self.shown_data.trip_distance != self.main.data.trip_distance:
            self.main.tft.text(fonts.big, "%6.2f" % (self.main.data.trip_distance), 16, 4*self.rh)
            self.shown_data.trip_distance = self.main.data.trip_distance
            

        if redraw_all or self.shown_data.trip_duration != self.main.data.trip_duration:
            h = self.main.data.trip_duration / 60
            m = self.main.data.trip_duration % 60
            self.main.tft.text(fonts.big, "%2d:%.2d" % (h, m), 32, 5*self.rh)
            self.shown_data.trip_duration = self.main.data.trip_duration
    
    def handle(self, id, long_click):
        #print("handler_csc")
        if long_click:
            self.main.go_menu_main()