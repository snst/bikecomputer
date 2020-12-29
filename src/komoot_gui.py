from komoot_data import *
import fonts
import const
from cycle_gui import *
import data_global as g
from data_cache import *
from signs import *

class KomootGui(CycleGui):
    y_distance = 0
    y_direction = 55
    y_street_speed = 140
    y_time_direction = 190

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache()

    def get_title(self):
        return b'komoot'

    def get_color_from_dist(self, data):
        return Color.red if data.distance <= self.main._settings.komoot_red_color.value else Color.white

    def show_distance(self, data, y):
        #print("d %u" % (data.distance))
        if data.distance < 1000:
            str = " %3d " % data.distance
            g.display.draw_text(fonts.f_wide_big, str, g.display.width, y, align=Align.center)
        else:
            str = " %.1f " % (data.distance / 1000)
            g.display.draw_text(fonts.f_wide_big, str, g.display.width, y, align=Align.center)

    def show_direction(self, data, y):
        W = g.display.width
        H = 80
        d = data.direction
        sign = get_sign(d)
        g.display.fill_rect((int)((g.display.width-72)/2), y, 72, H, Color.black)
        if sign:
            x = (int)((W - sign.WIDTH)/2)
            y += (int)((H - sign.HEIGHT)/2)
            g.display.bitmap_blit(x, y, sign, fg=self.get_color_from_dist(data))

    def show_street(self, data, y):
        if self.cache.changed(9, data.street):
            #g.display.fill_rect(0, y, g.display.width, fonts.f_narrow_text.height() * 2, Color.black)
            self.clear_street()
            g.display.draw_text_multi(fonts.f_narrow_text, "%s" % (data.street), 0, y, align=Align.center)

    def clear_street(self):
        g.display.fill_rect(0, self.y_street_speed, g.display.width, g.display.height-self.y_street_speed, Color.black)

    def show(self, redraw):
        if redraw:
            self.cache.reset()

        data = self.main.komoot_data
        csc = self.main.get_csc_data()
        settings = self.main._settings

        #data.street = "Schulstraße 77"

        dist_notify = False
        dir_changed = self.cache.changed(8, data.direction)

        if dir_changed or self.cache.changed(11, self.get_color_from_dist(data)):
            self.show_direction(data, self.y_direction)

        if self.cache.changed(13, data.distance):
            self.show_distance(data, self.y_distance)
            dist_notify = data.distance <= settings.komoot_all_on.value or (self.cache.changed(12, (int)(data.distance/100)) and data.distance <= settings.komoot_flash_on.value)

        show_street = settings.komoot_street_dist.value == 0 or data.distance < settings.komoot_street_dist.value
        show_street_changed = self.cache.changed(10, show_street)

        if show_street_changed:
            self.clear_street()

            if show_street:
                self.cache.reset_val(9)
            else:
                self.cache.reset_val(1)
                self.cache.reset_val(6)
                self.cache.reset_val(7)

        if show_street:
            self.show_street(data, self.y_street_speed)
        else:
            self.show_speed(csc, self.y_street_speed)
            self.show_trip_distance(csc, self.y_time_direction)
            self.show_trip_duration(csc, 58, self.y_time_direction, font=fonts.f_narrow_text)

        if settings.komoot_auto_on.value == 1 and (dir_changed or dist_notify):
            g.bc._display_ctrl.set_display_on()

    def show_speed(self, data, y):
        speed = round(data.speed, 1)
        if self.cache.changed(1, speed):
            self.show_float_speed(speed, g.display.width, y)


    def handle(self, event):
        if event == (Button.right | Button.long):
            self.main.gui_show_komoot_menu()
        else:
            GuiBase.handle(self, event)
