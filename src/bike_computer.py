from gui_main import *
from data_settings import *
from data_csc import *
from data_goal import *
from data_komoot import *
from display_ctrl import *
from const import *
from button_handler import *
import data_global as g
import csc
from scheduler import *


class BikeComputer:
    def __init__(self):
        self.settings = DataSettings()
        self.settings.load()
        self.csc_data = [ DataCsc(1) ]
        self._data_komoot = DataKomoot()
        self.display_ctrl = DisplayCtrl(self.settings)
        self.csc = csc.CSC(self.settings)
        self.gui = GuiMain(self.settings, self.csc_data, self._data_komoot)
        self.btn_left = ButtonHandler(g.hal, g.hal.btn_left, self.left, self.settings.long_click.value*10) 
        self.btn_right = ButtonHandler(g.hal, g.hal.btn_right, self.right, self.settings.long_click.value*10)
        self.last_notify_ms = 0
        self.notify_cnt = 0
        self._sch = Scheduler(g.hal)
        self.task_update_gui()

    def on_data_csc(self, raw_data):
        now = g.hal.ticks_ms()
        diff = now - self.last_notify_ms
        self.last_notify_ms = now
        self.notify_cnt += 1
        #print("on %u %ums" % (self.notify_cnt, diff))
        for data in self.csc_data:
            self.csc.process(raw_data, data)

    def on_data_komoot(self, raw_data):
        self._data_komoot.on_data(raw_data)

    def on_conn_state(self, state):
        #print(txt)
        self.gui.on_conn_state(state)

    def ignore_click(self, is_long):
        display_off = not self.display_ctrl.is_display_on()
        self.display_ctrl.set_display_on()
        return not is_long and display_off and self.settings.touch_ignore.value != 0

    def left(self, is_long):
        #print("left %s" % ("long" if long else "short"))
        if not self.ignore_click(is_long):
            self.gui.handle_click(Button.left, is_long)

    def right(self, is_long):
        #print("right %s" % ("long" if long else "short"))
        if not self.ignore_click(is_long):
            self.gui.handle_click(Button.right, is_long)

    def task_update_gui(self):
        #print("task_update_gui")
        self._sch.insert(500, self.task_update_gui)
        self.gui.cyclic_update()

    def add_task(self, ms, task):
        self._sch.insert(ms, task)