from data_komoot import *
import fonts
import const
from gui_base import *


class GuiKomoot(GuiBase):
    def __init__(self, main):
        GuiBase.__init__(self, main)

    def get_title(self):
        return "komoot"


    def show_distance(self, data, y):
        self.main.text(fonts.big, "%dm" % (data.distance), 0, y)

    def show_direction(self, data, y):
        self.main.text(fonts.big, ">%2d" % (data.direction), 0, y)

    def show_street(self, data, y):
        self.main.text(fonts.big, "%s" % (data.street), 0, y)

    def show(self, redraw_all):
        if redraw_all:
            self.main.clear()

        data = self.main.get_komoot_data()
        y = 0
        y_1 = 65
        y_2 = y_1 + 60
        y_3 = y_2 + 50

        self.show_direction(data, y)
        self.show_distance(data, y_1)
        self.show_street(data, y_2)

    
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