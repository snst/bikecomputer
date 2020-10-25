import fonts
from const import *
from gui_menu import *

class GuiEditValue:
    def __init__(self, main, item):
        self.main = main
        self.edit_val = item.data.value
        print("edit_val %f" % (self.edit_val))
        self.item = item
        self.breadcrum = self.main.get_breadcrum()
        self.edit_decimal_place = False
        pass

    def get_title(self):
        return "edit"

    def show(self, redraw_all):
        #print("gui_edit_setting_value")
        self.main.text(fonts.middle, self.breadcrum, 8, Layout.y_breadcrum)
        #self.main.tft.text(fonts.big, "+/-", 40, Layout.y_line05)
        #self.main.tft.text(fonts.big, self.item.name, 8, Layout.y_line1)
        self.main.draw_multiple_line(fonts.big, self.item.name, Layout.y_line1)
        if self.item.type == MenuItem.FLOAT_ITEM:
            x = self.main.get_text_center_pos(fonts.huge, 5)
            self.main.text(fonts.huge, "%3d" %(self.edit_val), x, Layout.y_line2, Color.white if self.edit_decimal_place else Color.red)
            self.main.text(fonts.huge, ".", x + 3 * (fonts.huge.WIDTH + 2), Layout.y_line2)
            self.main.text(fonts.huge, "%1d" %(self.edit_val*10%10), x + 4 * (fonts.huge.WIDTH + 2), Layout.y_line2, Color.red if self.edit_decimal_place else Color.white)
        elif self.item.type == MenuItem.INT_ITEM:
            self.main.text(fonts.huge, "%3d" %(self.edit_val), -1, Layout.y_line2, Color.red)


    def handle(self, id, long_click):
        #print("handler_edit_setting_value")
        if long_click:
            if id == Button.right:
                if (self.item.type == MenuItem.FLOAT_ITEM) and not self.edit_decimal_place:
                    self.edit_decimal_place = True
                    self.main.show()
                else:
                    self.item.data.value = self.edit_val
                    #print("set val %f" % (self.edit_val))
                    if self.item.callback_changed:
                        self.item.callback_changed(self.edit_val, True)
                    self.main.action_go_back()
            elif id == Button.left:
                if (self.item.type == MenuItem.FLOAT_ITEM) and self.edit_decimal_place:
                    self.edit_decimal_place = False
                    self.main.show()
                else:
                    self.main.action_go_back()
        else:
            step = 0.1 if self.edit_decimal_place  else 1
            if Button.left == id:
                self.edit_val = self.edit_val - step if self.edit_val > self.item.data.min else self.item.data.max
            elif Button.right == id:
                self.edit_val = self.edit_val + step if self.edit_val < self.item.data.max else self.item.data.min
            self.edit_val = (int) (self.edit_val*10)
            self.edit_val /= 10
            if self.item.callback_changed:
                self.item.callback_changed(self.edit_val, False)
            self.main.show()
