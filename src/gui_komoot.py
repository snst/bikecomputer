from data_komoot import *
import fonts
import const
from gui_base import *
import data_global as g
from data_cache import *

class GuiKomoot(GuiBase):
    y_direction = 0
    y_distance = 20
    y_street = 100

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache(4)

    def get_title(self):
        return "komoot"

    def get_color_from_dist(self, data):
        return Color.red if data.distance < 1000 else Color.white

    def show_distance(self, data, y):
        #print("d %u" % (data.distance))
        if data.distance < 1000:
            str = "%3d" % data.distance
            g.display.draw_text(fonts.pf_normal, str, g.display.width, y, align=Align.right)
        else:
            str = "%.1f" % (data.distance / 1000)
            g.display.draw_text(fonts.pf_normal, str, g.display.width, y, align=Align.right)

    def show_direction(self, data, y):
        g.display.text(fonts.font_komoot, "%c" % (chr(46+data.direction)), 0, 0, fg=self.get_color_from_dist(data))

    def show_street(self, data, y):
        g.display.fill_rect(0, y, g.display.width, fonts.pf_text.height() * 2, Color.black)
        g.display.draw_text_multi(fonts.pf_text, "%s" % (data.street), 0, y, align=Align.center)

    def show(self, redraw_all):
        if redraw_all:
            self.main.clear()
            self.cache.reset()

        data = self.main.get_komoot_data()
        csc = self.main.get_csc_data()
        data.distance = csc.sim * 100
        #data.street = "abcdef0ghi0jklmno0p0qrx0yz"

        if self.cache.changed(0, data.direction) or self.cache.changed(1, self.get_color_from_dist(data)):
            self.show_direction(data, self.y_direction)
            self.show_distance(data, self.y_distance)

        if self.cache.changed(2, data.distance):
            self.show_distance(data, self.y_distance)

        if self.cache.changed(3, data.street):
            self.show_street(data, self.y_street)

    
    def handle(self, id, long_click):
        if long_click:
            if id == Button.right:
                self.main.go_menu_main()
            elif id == Button.left:
                self.main.action_go_csc()
        else:
            if id == const.Button.left:
                self.main.action_go_csc()
            elif id == const.Button.right:
                self.main.action_go_csc()