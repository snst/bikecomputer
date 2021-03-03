# This Python file uses the following encoding: utf-8
from nav_data import *
import fonts
import const
from cycle_gui import *
import data_global as g
from data_cache import *
from signs import *

class NavGui(CycleGui):
    y_distance = 0
    y_direction = 55
    y_street_speed = 140
    y_time_direction = 190

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self._last_ms = g.hal.ticks_ms()
        self.show_distance_field = False

    def get_title(self):
        return b'nav'

    def show_nav_distance(self, nav, y):
        #print("d %u" % (nav.distance))
        if nav.distance < 1000:
            str = " %3d " % nav.distance
            g.display.draw_text(fonts.f_wide_big, str, g.display.width, y, align=Align.center)
        else:
            str = " %.1f " % (nav.distance / 1000)
            g.display.draw_text(fonts.f_wide_big, str, g.display.width, y, align=Align.center)

    def show_direction(self, nav, y):
        W = g.display.width
        H = 80
        d = nav.direction
        sign = get_sign(d)
        g.display.fill_rect((int)((g.display.width-72)/2), y, 72, H, Color.black)
        if sign:
            x = (int)((W - sign.WIDTH)/2)
            y += (int)((H - sign.HEIGHT)/2)
            g.display.bitmap_blit(x, y, sign)

    def replace_street_str(self, txt):
        txt = txt.replace("ß", "ss")
        txt = txt.replace("ä", "a")
        txt = txt.replace("ö", "o")
        txt = txt.replace("ü", "u")
        return txt

    def show_street(self, nav, y):
        if self.cache.changed(DataCache.NAV_STREET, nav.street):
            #g.display.fill_rect(0, y, g.display.width, fonts.f_narrow_text.height() * 2, Color.black)
            self.clear_street()
            g.display.draw_text_multi(fonts.f_narrow_text, "%s" % (self.replace_street_str(nav.street)), 0, y, align=Align.center)

    def clear_street(self):
        g.display.fill_rect(0, self.y_street_speed, g.display.width, g.display.height-self.y_street_speed, Color.black)

    def show(self, redraw):
        self.cache.reset(redraw)

        nav = self.main.nav_data
        trip = self.main.get_trip()
        settings = self.main._settings

        dist_notify = False


        if (g.hal.ticks_ms() - self._last_ms) > (settings.nav_km_time_ms.value * 1000):
            self.show_distance_field = not self.show_distance_field
            self._last_ms = g.hal.ticks_ms()
            self.cache.reset_val(DataCache.TRIP_DISTANCE)
            self.cache.reset_val(DataCache.TRIP_DURATION)
            g.display.fill_rect(0, self.y_time_direction, g.display.width, fonts.f_wide_normal.height(), Color.black)

        dir_changed = self.cache.changed(DataCache.NAV_DIRECTION, nav.direction)

        if dir_changed:
            self.show_direction(nav, self.y_direction)

        if self.cache.changed(DataCache.NAV_DISTANCE, nav.distance):
            self.show_nav_distance(nav, self.y_distance)
            dist_notify = nav.distance <= settings.nav_all_on.value or (self.cache.changed(DataCache.NAV_DIST_100, (int)(nav.distance/100)) and nav.distance <= settings.nav_flash_on.value)

        show_street = settings.nav_street_dist.value == 0 or nav.distance < settings.nav_street_dist.value
        show_street_changed = self.cache.changed(DataCache.NAV_SHOW_STREET, show_street)

        if show_street_changed:
            self.clear_street()

            if show_street:
                self.cache.reset_val(DataCache.NAV_STREET)
            else:
                self.cache.reset_val(DataCache.SPEED)

        if show_street:
            self.show_street(nav, self.y_street_speed)
        else:
            self.show_speed(self.main.cycling.speed, self.y_street_speed)
            #self.show_trip_distance(trip, self.y_time_direction)
            #self.show_trip_duration(trip, 68, self.y_time_direction, font=fonts.f_narrow_text)

            if self.show_distance_field:
                self.show_trip_distance(trip, self.y_time_direction)
                self.show_icon(s_km, self.y_time_direction)
            else:
                self.show_trip_duration(trip, g.display.width, self.y_time_direction)
                self.show_icon(s_time, self.y_time_direction)

        if settings.nav_auto_on.value == 1 and (dir_changed or dist_notify):
            g.bc._display_ctrl.set_display_on()

    def show_speed(self, speed, y):
        if self.cache.changed(DataCache.SPEED, speed):
            self.show_float_speed(speed, g.display.width, y)


    def handle(self, event):
        if event == (Button.right | Button.long):
            self.main.gui_show_navi_menu()
        else:
            GuiBase.handle(self, event)
