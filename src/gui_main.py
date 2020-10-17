from gui_edit_value import *
from gui_csc import *
from gui_menu import *
from data_goal import *
from menu_config import *
from data_goal import *
from const import *

class GuiMain:


    def __init__(self, tft, hal, settings, csc_data):
        self.callback_repaint = None
        self.tft = tft
        self.hal = hal
        self.settings = settings
        self.csc_data = csc_data
        self.csc_index = 0
        self.active_gui = None
        self.gui_stack = []
        self.clear()
        self.add_to_gui_stack(GuiCsc(self))
        pass

    def text2(self, font, text, x, y, fg = Color.white, bg = Color.black):
        cx = 0
        for char in text:
            ch = ord(char)
            if font.FIRST <= ch < font.LAST:
                self.tft.text(font, "%c" % char, x+cx, y, fg, bg)
            else:
                self.tft.rect(x+cx, y, font.WIDTH, font.HEIGHT, 0)
            cx += font.WIDTH

    def get_text_center_pos(self, font, n):
        space = 2
        w = n * (font.WIDTH + space)
        x = (int)((Display.width - w) / 2)
        return x


    def text(self, font, text, x, y, fg = Color.white, bg = Color.black):
        space = 2
        w = 0
        cx = 0

        if x < 0: # center
            x = self.get_text_center_pos(font, len(text))

        for char in text:
            ch = ord(char)
            if font.FIRST <= ch < font.LAST:
                self.tft.text(font, "%c" % char, x+cx, y, fg, bg)
                w = space
                cx += font.WIDTH
            else:
                w = font.WIDTH + space
            self.tft.fill_rect(x+cx, y, w, font.HEIGHT, bg)
            cx += w

    def get_current_csc_data(self):
        return self.csc_data[self.csc_index]

    def set_callback_repaint(self, cb):
        self.callback_repaint = cb

    def clear(self):
        self.tft.fill(Color.black)
        #print("clear")


    def cyclic_update(self):
        #print("update")
        if isinstance(self.active_gui, GuiCsc):
            self.active_gui.show(False)
            self.repaint()


    def show(self):
        #print("show")
        #self.clear()
        self.active_gui.show(True)
        self.repaint()

    def repaint(self):
        if self.callback_repaint:
            self.callback_repaint()
        #self.tft.update()
        pass

    def activate_gui(self, gui):
        self.active_gui = gui
        self.show()

    def handle_click(self, id, long_click):
        self.active_gui.handle(id, long_click)

    def get_breadcrum(self):
        val = ""
        itergui = iter(self.gui_stack)
        next(itergui)
        for g in itergui:
            val = val + ">" + g.get_title()
        #if len(self.gui_stack) > 1:
         #   gui = self.gui_stack[-1]
          #  val = gui.breadcrum + ">" + gui.title
        return val

    def go_menu_main(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMain()))

    def go_menu_meter(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMeter()))

    def go_menu_goal(self):
        csc_data = self.get_current_csc_data()
        if csc_data.goal == None:
            csc_data.goal = DataGoal()

        self.add_to_gui_stack(GuiMenu(self, MenuGoal(csc_data.goal)))

    def go_menu_settings(self):

        m = MenuSettings(self.settings)
        m.led_on.set_value_changed_callback(self.callback_display_brightness_changed)
        m.led_off.set_value_changed_callback(self.callback_display_brightness_changed)
        self.add_to_gui_stack(GuiMenu(self, m))


    def action_go_csc(self):
        while len(self.gui_stack) > 1:
            self.gui_stack.pop()
        self.activate_gui(self.gui_stack[0])

    def action_go_edit_setting_value(self, item):
        self.add_to_gui_stack(GuiEditValue(self, item))

    def action_go_back(self):
        self.gui_stack.pop()
        self.activate_gui(self.gui_stack[-1])

    def add_to_gui_stack(self, gui):
        self.gui_stack.append(gui)
        self.activate_gui(gui)

    def do_action(self, action):
        print("do action:" + action)
        getattr(self, action)()

    def do_add_meter(self):
        print("do_add_meter")
        n = len(self.csc_data) + 1
        self.csc_data.append(DataCsc(n))
        self.csc_index = n - 1
        self.action_go_csc()

    def do_reset_meter(self):
        print("do_reset_meter")
        self.get_csc_data().reset()
        self.action_go_csc()

    def do_start_goal(self):
        csc_data = self.get_current_csc_data()
        csc_data.goal.is_active = True
        self.action_go_csc()

    def do_stop_goal(self):
        csc_data = self.get_current_csc_data()
        csc_data.goal.is_active = False
        self.action_go_csc()

    def do_save_settings(self):
        self.action_go_csc()
        print("do_save_settings")

    def get_csc_data(self):
        return self.csc_data[self.csc_index]

    def next_csc(self):
        self.csc_index = (self.csc_index + 1) % len(self.csc_data)
        self.action_go_csc()

    def prev_csc(self):
        self.csc_index = (self.csc_index + len(self.csc_data) - 1) % len(self.csc_data)
        self.action_go_csc()        

    def callback_display_brightness_changed(self, val, closed):
        print("callback_display_brightness_changed %d" % (val))
        self.hal.set_backlight(val)


    def draw_centered(self, font, text, y):
        w = len(text) * font.WIDTH    
        x = (int)((135-w) / 2)
        self.tft.text(font, text, x, y, Color.white, Color.black)
        #print("dc")
        #print(text)

    def draw_multiple_line(self, font, text, y):
        txt = text.split()
        n = len(txt)
        k=1
        for t in txt:
            self.draw_centered(font, t, y - ((n-k)*font.HEIGHT))
            k += 1        