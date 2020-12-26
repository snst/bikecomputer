import fonts
from const import *
from menu_item import *
import data_global as g


class GuiMenu:
    def __init__(self, main, menu):
        self.main = main
        self.menu = menu
        self.menu_selected_item = 0
        self.breadcrum = self.main.get_breadcrum() + b'>' + self.get_title()

    def get_selected_item(self):
        return self.menu.items[self.menu_selected_item]

    def get_title(self):
        return self.menu.title

    def show(self, redraw_all):
        #self.main.clear()
        item = self.get_selected_item()
        g.display.draw_text(fonts.f_narrow_small, self.breadcrum, 8, Layout.y_breadcrum)
        
        font = fonts.f_narrow_small if item.type == MenuItem.INT_ITEM or item.type == MenuItem.FLOAT_ITEM else fonts.f_narrow_text
        g.display.draw_text_multi(font, item.name, 0, Layout.y_setting_text, align=Align.center_sep)

        if item.type == MenuItem.INT_ITEM:
            g.display.draw_text(fonts.f_wide_normal, "%3d" %(item.data.value), 0, Layout.y_setting_val, align=Align.center)
        elif item.type == MenuItem.FLOAT_ITEM:
            g.display.draw_text(fonts.f_wide_normal, "%5.1f" %(item.data.value), 0, Layout.y_setting_val, align=Align.center)

    def handle(self, event):
        if event == Event.menu_prev:
            self.main.gui_stack_pop()
        elif event == Event.menu_next:
            self.handle_select()
        elif event == Event.val_inc:
            self.handle_inc()
        elif event == Event.val_dec:
            self.handle_dec()

    def handle_select(self):
        item = self.get_selected_item()
        if item.type == MenuItem.INT_ITEM or item.type == MenuItem.FLOAT_ITEM:
            self.main.action_go_edit_setting_value(item)
        else:
            item.action()

    def handle_dec(self):
        if self.menu_selected_item > 0:
            self.menu_selected_item -= 1
        else:
            self.menu_selected_item = len(self.menu.items)-1
        self.main.show()

    def handle_inc(self):
        if self.menu_selected_item < len(self.menu.items)-1:
            self.menu_selected_item += 1
        else:
            self.menu_selected_item = 0
        self.main.show()
