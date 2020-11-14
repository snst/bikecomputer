from data_komoot import *
import fonts
import const
from gui_base import *


class GuiKomoot(GuiBase):
    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.old_data = DataKomoot()
        self.old_color = None

    def get_title(self):
        return "komoot"

    def get_color_from_dist(self, data):
        return Color.red if data.distance < 1000 else Color.white

    def show_distance(self, data, y):

        print("d %u" % (data.distance))
        if data.distance < 1000:
            str = "%3d" % data.distance
            self.main.text(fonts.huge, str, 80, y)
        else:
            str = "%2d " % (data.distance / 1000)
            self.main.text(fonts.huge, str, 80, y)
            str = "%d" % ((data.distance % 1000) / 100)
            self.main.text(fonts.bign, str, 86 + 2*fonts.huge.WIDTH, y)
#        elif data.distance < 10000:
#            str = "%d.%d" % ((data.distance / 1000), ((data.distance % 1000) / 100))
#        else:
#            str = "%3d" % (data.distance / 1000)


    def show_direction(self, data, y):
        #self.main.text(fonts.big, ">%02d" % (data.direction), 0, y)
        self.main.text(fonts.font_komoot, "%c" % (chr(46+data.direction)), 0, 0, fg=self.get_color_from_dist(data))

    def show_street(self, data, y):
        self.main.tft.fill_rect(0, y, Display.width, fonts.big.HEIGHT * 3, Color.black)
        self.main.draw_multiple_line2(fonts.big, "%s" % (data.street), y)

    def show(self, redraw_all):
        if redraw_all:
            self.main.clear()
            self.old_data.street = ""
            self.old_data.distance = -1
            self.old_data.direction = -1
            self.old_color = None

        data = self.main.get_komoot_data()
        csc = self.main.get_csc_data()
        data.distance = csc.sim * 100
        y = 0
        y_1 = 45
        y_2 = y_1 + 60
        y_3 = y_2 + 50

        if self.old_data.direction != data.direction or self.old_color != self.get_color_from_dist(data):
            self.show_direction(data, y)
            self.old_data.direction = data.direction
            self.old_color = self.get_color_from_dist(data)

        if self.old_data.distance != data.distance:
            self.show_distance(data, y_1)
            self.old_data.distance = data.distance

        if self.old_data.street != data.street:
            self.show_street(data, y_2)
            self.old_data.street = data.street

    
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