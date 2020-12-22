import fonts
from const import *
from gui_menu import *
import data_global as g


class GuiEditValue:
    def __init__(self, main, item):
        self.main = main
        self.edit_val = item.data.value
        #print("edit_val %f" % (self.edit_val))
        self.item = item
        self.breadcrum = self.main.get_breadcrum()
        self.edit_decimal_place = False
        pass

    def get_title(self):
        return b'"edit'

    def show(self, redraw_all):
        #print("gui_edit_setting_value")
        g.display.draw_text(fonts.pf_small, self.breadcrum, 8, Layout.y_breadcrum)
        #g.display.draw_text(fonts.pf_text, self.item.name, 0, Layout.y_setting_text, align=Align.center)
        font = fonts.pf_small if self.item.type == MenuItem.INT_ITEM or self.item.type == MenuItem.FLOAT_ITEM else fonts.pf_text
        g.display.draw_text_multi(font, self.item.name, 0, Layout.y_setting_text, align=Align.center_sep)

        if self.item.type == MenuItem.FLOAT_ITEM:
            #x = self.main.get_text_center_pos(fonts.huge, 5)
            x = 75
            g.display.draw_text(fonts.pf_normal, "  %3d" %(self.edit_val), x, Layout.y_setting_val, Color.white if self.edit_decimal_place else Color.red, align=Align.right)
            g.display.draw_text(fonts.pf_normal, ".", x, Layout.y_setting_val, align=Align.left)
            g.display.draw_text(fonts.pf_normal, "%1d  " %(self.edit_val*10%10), x + 5, Layout.y_setting_val, Color.red if self.edit_decimal_place else Color.white, align=Align.left)
        elif self.item.type == MenuItem.INT_ITEM:
            g.display.draw_text(fonts.pf_normal, "  %3d  " %(self.edit_val), 0, Layout.y_setting_val, Color.red, align=Align.center)


    def handle(self, event):
        #print("handler_edit_setting_value")
        if event == Event.menu_next:
            if (self.item.type == MenuItem.FLOAT_ITEM) and not self.edit_decimal_place:
                self.edit_decimal_place = True
                self.main.show()
            else:
                self.item.data.value = self.edit_val
                #print("set val %f" % (self.edit_val))
                if self.item.callback_changed:
                    self.item.callback_changed(self.edit_val, True)
                self.main.gui_stack_pop()
        elif event == Event.menu_prev:
            if (self.item.type == MenuItem.FLOAT_ITEM) and self.edit_decimal_place:
                self.edit_decimal_place = False
                self.main.show()
            else:
                self.main.gui_stack_pop()
        else:
            step = self.item.data.step/10 if self.edit_decimal_place else self.item.data.step
            if event == Event.val_dec:
                self.edit_val = self.edit_val - step if self.edit_val > self.item.data.min else self.item.data.max
            elif event == Event.val_inc:
                self.edit_val = self.edit_val + step if self.edit_val < self.item.data.max else self.item.data.min
            self.edit_val = round(self.edit_val,2)
            if self.item.callback_changed:
                self.item.callback_changed(self.edit_val, False)
            self.main.show()
