import fonts
from const import *

class GuiEditValue:
    def __init__(self, main, item):
        self.main = main
        self.edit_val = item.value
        self.item = item
        self.breadcrum = self.main.get_breadcrum()
        self.edit_decimal_place = False
        pass

    def get_title(self):
        return "edit"

    def show(self, redraw_all):
        #print("gui_edit_setting_value")
        self.main.tft.text(fonts.middle, self.breadcrum, 8, Layout.y_breadcrum)
        self.main.tft.text(fonts.big, "+/-", 40, Layout.y_line05)
        self.main.tft.text(fonts.big, self.item.name, 8, Layout.y_line1)
        if self.item.is_float:
            self.main.tft.text(fonts.big, "%5d" %(self.edit_val), 8, Layout.y_line2, Color.white if self.edit_decimal_place else Color.red)
            self.main.tft.text(fonts.big, ".", 8+5*16, Layout.y_line2)
            self.main.tft.text(fonts.big, "%1d" %(self.edit_val*10%10), 8+6*16, Layout.y_line2, Color.red if self.edit_decimal_place else Color.white)
        else:
            self.main.tft.text(fonts.big, "%5d" %(self.edit_val), 8, Layout.y_line2, Color.red)


    def handle(self, id, long_click):
        #print("handler_edit_setting_value")
        if long_click:
            if id == Button.right:
                if self.item.is_float and not self.edit_decimal_place:
                    self.edit_decimal_place = True
                    self.main.show()
                else:
                    self.item.value = self.edit_val
                    self.main.action_go_back()
            elif id == Button.left:
                if self.item.is_float and self.edit_decimal_place:
                    self.edit_decimal_place = False
                    self.main.show()
                else:
                    self.main.action_go_back()
        else:
            step = 0.1 if self.edit_decimal_place  else 1
            if 0 == id:
                self.edit_val = self.edit_val - step if self.edit_val > self.item.min else self.item.max
            else:
                self.edit_val = self.edit_val + step if self.edit_val < self.item.max else self.item.min
            self.main.show()