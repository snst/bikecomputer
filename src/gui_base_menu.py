import fonts
from const import *

class GuiBaseMenu:
    def __init__(self, main, menu):
        self.main = main
        self.menu = menu
        self.menu_selected_item = 0
        self.breadcrum = self.main.get_breadcrum() + ">" + self.get_title()

    def get_title(self):
        return self.menu.title

    def show(self, redraw_all):
        #print("gui_menu")
        self.main.clear()
        item = self.menu.items[self.menu_selected_item]
        self.main.tft.text(fonts.middle, self.breadcrum, 8, Layout.y_breadcrum)
        #self.main.tft.text(fonts.big, self.menu.title, 8, self.yoffset+0*self.rh)
        self.main.tft.text(fonts.big, item.name, 8, Layout.y_line1)

    def handle(self, id, long_click):
        #print("handler_menu")
        if long_click:
            if id == 0:
                self.long_click_left()
            else:
                self.long_click_right()
        else:
            if 0==id:
                self.short_click_left()
            else:
                self.short_click_right()

    def long_click_left(self):
        self.main.action_go_back()

    def long_click_right(self):
        self.main.do_action(self.menu.items[self.menu_selected_item].action)

    def short_click_left(self):
        if self.menu_selected_item>0:
            self.menu_selected_item -= 1
        else:
            self.menu_selected_item = len(self.menu.items)-1
        self.main.show()

    def short_click_right(self):
        if self.menu_selected_item<len(self.menu.items)-1:
            self.menu_selected_item += 1
        else:
            self.menu_selected_item = 0
        self.main.show()
