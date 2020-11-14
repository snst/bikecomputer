from gui_edit_value import *
from gui_csc import *
from gui_menu import *
from gui_komoot import *
from data_goal import *
from menu_config import *
from data_goal import *
from const import *
import fonts 
import math

class GuiMain:


    def __init__(self, tft, hal, settings, csc_data, komoot_data):
        self.conn_state = ConnState.disconnected
        self.callback_repaint = None
        self.tft = tft
        self.hal = hal
        self.settings = settings
        self.csc_data = csc_data
        self._komoot_data = komoot_data
        self.csc_index = 0
        self.active_gui = None
        self.gui_stack = []
        self.clear()
        self._gui_komoot = GuiKomoot(self)
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
        if isinstance(self.active_gui, GuiCsc) or isinstance(self.active_gui, GuiKomoot):
            self.active_gui.show(False)
            self.repaint()
        self.update_state()


    def show(self):
        #print("show")
        #self.clear()
        self.active_gui.show(True)
        self.repaint()

    def repaint(self):
        if self.callback_repaint:
            self.callback_repaint()
        #self.tft.update()
        self.update_state()
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
            csc_data.goal.load(self.hal)
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
        #print("do action:" + action)
        getattr(self, action)()

    def do_add_meter(self):
        #print("do_add_meter")
        n = len(self.csc_data) + 1
        self.csc_data.append(DataCsc(n))
        self.csc_index = n - 1
        self.action_go_csc()

    def do_reset_meter(self):
        #print("do_reset_meter")
        self.get_csc_data().reset()
        self.action_go_csc()

    def do_start_goal(self):
        csc_data = self.get_current_csc_data()
        csc_data.goal.is_started = True
        csc_data.goal.calculate_progress(csc_data)
        self.action_go_csc()

    def do_stop_goal(self):
        csc_data = self.get_current_csc_data()
        csc_data.goal.is_started = False
        self.action_go_csc()

    def do_save_settings(self):
        self.action_go_csc()
        #print("do_save_settings")
        self.settings.save(self.hal)

    def do_reconnect(self):
        self.hal.bt_reconnect()
        self.action_go_csc()

    def do_save_goal(self):
        self.get_current_csc_data().goal.save(self.hal)

    def do_load_goal(self):
        self.get_current_csc_data().goal.load(self.hal)

    def show_komoot(self):
        self.add_to_gui_stack(self._gui_komoot)
        pass

    def get_csc_data(self):
        return self.csc_data[self.csc_index]

    def next_csc(self):
        self.csc_index = (self.csc_index + 1) % len(self.csc_data)
        self.action_go_csc()

    def prev_csc(self):
        self.csc_index = (self.csc_index + len(self.csc_data) - 1) % len(self.csc_data)
        self.action_go_csc()        

    def callback_display_brightness_changed(self, val, closed):
        #print("callback_display_brightness_changed %d" % (val))
        self.hal.set_backlight(val)


    def text_aligned(self, font, text, x, y, align = Align.left):
    
        if align == Align.left:
            pass
        else:
            w = len(text) * font.WIDTH    
            if align == Align.center:
                x = (int)((Display.width-w) / 2)
            else:
                x = Display.width - w - x
        self.tft.text(font, text, x, y, Color.white, Color.black)

    def draw_multiple_line(self, font, text, y, align = Align.center):
        txt = text.split()
        n = len(txt)
        k=1
        for t in txt:
            self.text_aligned(font, t, 0, y - ((n-k)*font.HEIGHT), align)
            k += 1        

    def draw_multiple_line2(self, font, text, y, align = Align.center):
        w = font.WIDTH * len(text)
        lines = math.ceil(w / Display.width)
        n = int(math.ceil(len(text) / lines))
        txt = [text[i:i+n] for i in range(0, len(text), n)]

        k=0
        for t in txt:
            self.text_aligned(font, t, 0, y + k*font.HEIGHT, align)
            k += 1        


    def on_conn_state(self, state):
        self.conn_state = state

    def update_state(self):
        txt = ""
        if self.conn_state == ConnState.disconnected:
            txt = "Disconnected"
        elif self.conn_state == ConnState.scanning:
            txt = "Scanning    "
        elif self.conn_state == ConnState.connecting:
            txt = "Connecting  "
        elif self.conn_state == ConnState.connected:
            txt = "Connected   "
        elif self.conn_state == ConnState.no_device:
            txt = "No Device   "
        elif self.conn_state == ConnState.found_device:
            txt = "Found Device"

        txt += " R" if self.get_current_csc_data().is_riding else "  "
        self.text_aligned(fonts.middle, txt, 20, Display.height - fonts.middle.HEIGHT)

    def get_komoot_data(self):
        return self._komoot_data