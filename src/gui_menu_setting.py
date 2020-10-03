import fonts
import gui_base_menu
from const import *

class GuiMenuSetting(gui_base_menu.GuiBaseMenu):

    def get_selected_item(self):
        return self.menu.items[self.menu_selected_item]


    def show(self, redraw_all):
        super().show(redraw_all)
        #print("gui_menu")
        item = self.get_selected_item()
        if item.value != None:
            if item.is_float:
                self.main.tft.text(fonts.big, "%7.1f" %(item.value), 8, Layout.y_line2)
            else:
                self.main.tft.text(fonts.big, "%5d" %(item.value), 8, Layout.y_line2)


    def long_click_right(self):
        item = self.get_selected_item()
        if item.value != None:
            self.main.action_go_edit_setting_value(item)
        elif item.action != None:
            self.main.do_action(item.action)
