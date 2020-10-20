from gui_main import *
from data_settings import *
from data_csc import *
from data_goal import *
from display_ctrl import *
from const import *
from button_handler import *

import csc

class BikeComputer:
    def __init__(self, tft, hal):
        self.tft = tft
        self.hal = hal
        self.settings = DataSettings()
        self.settings.load(hal)
        self.csc_data = [ DataCsc(1) ]
        self.display_ctrl = DisplayCtrl(self.settings, hal)
        self.csc = csc.CSC(self.settings)
        self.gui = GuiMain(self.tft, self.hal, self.settings, self.csc_data)
        self.btn_left = ButtonHandler(hal, hal.btn_left, self.left, self.settings.long_click.value*10) 
        self.btn_right = ButtonHandler(hal, hal.btn_right, self.right, self.settings.long_click.value*10)
        self.last_notify_ms = 0
        self.notify_cnt = 0



    def on_notify(self, raw_data):
        now = self.hal.ticks_ms()
        diff = now - self.last_notify_ms
        self.last_notify_ms = now
        self.notify_cnt += 1
        print("on %u %ums" % (self.notify_cnt, diff))
        for data in self.csc_data:
            self.csc.process(raw_data, data)

    def on_info(self, txt):
        print(txt)
        self.gui.show_info(txt)

    def left(self, long):
        self.display_ctrl.set_display_on()
        print("left %s" % ("long" if long else "short"))
        self.gui.handle_click(Button.left, long)

    def right(self, long):
        self.display_ctrl.set_display_on()
        print("right %s" % ("long" if long else "short"))
        self.gui.handle_click(Button.right, long)

