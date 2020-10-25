import fonts
from const import *
from menu_item import *

class GuiMenu:
    def __init__(self, main, menu):
        self.main = main
        self.menu = menu
        self.menu_selected_item = 0
        self.breadcrum = self.main.get_breadcrum() + ">" + self.get_title()

    def get_selected_item(self):
        return self.menu.items[self.menu_selected_item]

    def get_title(self):
        return self.menu.title



    def show(self, redraw_all):
        #print("gui_menu")
        self.main.clear()
        item = self.get_selected_item()
        self.main.text(fonts.middle, self.breadcrum, 8, Layout.y_breadcrum)
        #self.main.tft.text(fonts.big, item.name, 8, Layout.y_line1)
        self.main.draw_multiple_line(fonts.big, item.name, Layout.y_line1)

        if item.type == MenuItem.INT_ITEM:
            self.main.text(fonts.huge, "%3d" %(item.data.value), -1, Layout.y_line2)
        elif item.type == MenuItem.FLOAT_ITEM:
            self.main.text(fonts.huge, "%5.1f" %(item.data.value), -1, Layout.y_line2)


    def handle(self, id, long_click):
        #print("handler_menu")
        if long_click:
            if id == Button.left:
                self.long_click_left()
            else:
                self.long_click_right()
        else:
            if id == Button.left:
                self.short_click_left()
            else:
                self.short_click_right()

    def long_click_left(self):
        self.main.action_go_back()

    def long_click_right(self):

        item = self.get_selected_item()
        if item.type == MenuItem.INT_ITEM or item.type == MenuItem.FLOAT_ITEM:
            self.main.action_go_edit_setting_value(item)
        else:
            self.main.do_action(item.action)

    def short_click_left(self):
        if self.menu_selected_item > 0:
            self.menu_selected_item -= 1
        else:
            self.menu_selected_item = len(self.menu.items)-1
        self.main.show()

    def short_click_right(self):
        if self.menu_selected_item < len(self.menu.items)-1:
            self.menu_selected_item += 1
        else:
            self.menu_selected_item = 0
        self.main.show()
