from gui_main import *
from data_settings import *
from cycle_data import *
from goal_data import *
from komoot_data import *
from display_ctrl import *
from const import *
from button_handler import *
import data_global as g
from scheduler import *
from item_list import *
from altimeter import *

class BikeComputer:
    def __init__(self):
        self._settings = DataSettings()
        self._settings.load()
        self._scheduler = Scheduler(g.hal)
        self._cycle_data = [CycleData(1, self._settings)]
        self._komoot_data = KomootData()
        self._display_ctrl = DisplayCtrl(self._settings)
        self.gui = GuiMain(self._settings, self._cycle_data, self._komoot_data)
        self._btn_left = ButtonHandler(g.hal, g.hal.btn_left, self.btn_event, Button.left, self._settings.long_click.value) 
        self._btn_right = ButtonHandler(g.hal, g.hal.btn_right, self.btn_event, Button.right, self._settings.long_click.value)
        self._altimeter = Altimeter()
        #g.hal.gc()
        #self._last_notify_ms = 0
        #self._notify_cnt = 0

    def on_data_csc(self, raw_data):
        #now = g.hal.ticks_ms()
        #diff = now - self._last_notify_ms
        #self._last_notify_ms = now
        #self._notify_cnt += 1
        #print("on %u %ums" % (self._notify_cnt, diff))
        for data in self._cycle_data:
            data.process(raw_data)

    def on_data_komoot(self, raw_data):
        self._komoot_data.on_data(raw_data)

    def ignore_click(self, is_long):
        display_off = not self._display_ctrl.is_display_on()
        self._display_ctrl.set_display_on()
        return not is_long and display_off and self._settings.touch_ignore.value != 0

    def btn_left_short(self):
        self.gui.handle_click(Button.left, Button.short)

    def btn_left_long(self):
        self.gui.handle_click(Button.left, Button.long)

    def btn_right_short(self):
        self.gui.handle_click(Button.right, Button.short)

    def btn_right_long(self):
        self.gui.handle_click(Button.right, Button.long)

    def btn_event(self, btn_id, ev_type):
        is_long = ev_type == Button.long
        if not self.ignore_click(is_long):
            if btn_id == Button.left:
                self._scheduler.insert(1, self.btn_left_long if is_long else self.btn_left_short)
            elif btn_id == Button.right:
                self._scheduler.insert(1, self.btn_right_long if is_long else self.btn_right_short)

    def task_update_gui(self):
        #print("task_update_gui")
        self._scheduler.insert(500, self.task_update_gui)
        self.gui.cyclic_update()

    def add_task(self, ms, task):
        self._scheduler.insert(ms, task)

    def task_update_bt(self):
        #print("task_update_bt")
        self.add_task(5000, self.task_update_bt)
        if (self._settings.csc_on.value and not g.bt.is_csc_connected()) or (self._settings.komoot_enabled.value and not g.bt.is_komoot_connected()):
            g.bt.scan(csc_enabled = self._settings.csc_on.value, komoot_enabled = self._settings.komoot_enabled.value)

    def task_read_komoot(self):
        #print("task_read_komoot")
        self.add_task(4000, self.task_read_komoot)
        if self._settings.komoot_enabled.value:
            g.bt.read_komoot()

    def task_update_altimeter(self):
        self._scheduler.insert(100, self.task_update_altimeter)
        if self._settings.altimeter_enabled.value:
            self._altimeter.update()

    def task_read_bat(self):
        self.add_task(5000, self.task_read_bat)
        g.hal.update_bat()


    def run(self):
        g.bt.set_on_csc(self.on_data_csc)
        g.bt.set_on_komoot(self.on_data_komoot)
        self.task_update_bt()
        self.task_read_komoot()
        self.task_read_bat()
        self.task_update_gui()
        self.task_update_altimeter()
        while(True):
            try:
                self._scheduler.run()
            except OSError:
                print("OSError")
