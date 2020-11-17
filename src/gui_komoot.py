from data_komoot import *
import fonts
import const
from gui_base import *
import data_global as g
from data_cache import *

class GuiKomoot(GuiBase):
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
        g.display.fill_rect(0, y, g.display.width, fonts.pf_narrow.height() * 2, Color.black)
        g.display.draw_text_multi(fonts.pf_narrow, "%s" % (data.street), 0, y, align=Align.center)

    def show(self, redraw_all):
        if redraw_all:
            self.main.clear()
            self.cache.reset()

        data = self.main.get_komoot_data()
        csc = self.main.get_csc_data()
        #data.distance = csc.sim * 100
        y = 0
        y_1 = 45
        y_2 = y_1 + 60
        y_3 = y_2 + 50

        if self.cache.changed(0, data.direction) or self.cache.changed(1, self.get_color_from_dist(data)):
            self.show_direction(data, y)
            self.show_distance(data, y_1)

        if self.cache.changed(2, data.distance):
            self.show_distance(data, y_1)

        if self.cache.changed(3, data.street):
            self.show_street(data, y_2)

    
    def handle(self, id, long_click):
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