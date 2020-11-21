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
from item_list import *
from altimeter import *

class BikeComputer:
    def __init__(self):
        self.settings = DataSettings()
        self.settings.load()
        self._list_csc_data = ItemList()
        self._list_csc_data.add(DataCsc(1))
        self._data_komoot = DataKomoot()
        self.display_ctrl = DisplayCtrl(self.settings)
        self.csc = csc.CSC(self.settings)
        self.gui = GuiMain(self.settings, self._list_csc_data, self._data_komoot)
        self.btn_left = ButtonHandler(g.hal, g.hal.btn_left, self.left, self.settings.long_click.value*10) 
        self.btn_right = ButtonHandler(g.hal, g.hal.btn_right, self.right, self.settings.long_click.value*10)
        self.last_notify_ms = 0
        self.notify_cnt = 0
        self._sch = Scheduler(g.hal)
        self._altimeter = Altimeter()
        self.task_update_gui()
        self.task_update_altimeter()

    def on_data_csc(self, raw_data):
        now = g.hal.ticks_ms()
        diff = now - self.last_notify_ms
        self.last_notify_ms = now
        self.notify_cnt += 1
        #print("on %u %ums" % (self.notify_cnt, diff))
        for data in self._list_csc_data._items:
            self.csc.process(raw_data, data)

    def on_data_komoot(self, raw_data):
        self._data_komoot.on_data(raw_data)

    def ignore_click(self, is_long):
        display_off = not self.display_ctrl.is_display_on()
        self.display_ctrl.set_display_on()
        return not is_long and display_off and self.settings.touch_ignore.value != 0

    def ls(self):
        self.gui.handle_click(Button.left, False)

    def ll(self):
        self.gui.handle_click(Button.left, True)

    def rs(self):
        self.gui.handle_click(Button.right, False)

    def rl(self):
        self.gui.handle_click(Button.right, True)

    def left(self, is_long):
        #print("left %s" % ("long" if long else "short"))
        if not self.ignore_click(is_long):
            #self.gui.handle_click(Button.left, is_long)
            self._sch.insert(1, self.ll if is_long else self.ls)


    def right(self, is_long):
        #print("right %s" % ("long" if long else "short"))
        if not self.ignore_click(is_long):
#            self.gui.handle_click(Button.right, is_long)
            self._sch.insert(1, self.rl if is_long else self.rs)

    def task_update_gui(self):
        #print("task_update_gui")
        self._sch.insert(500, self.task_update_gui)
        self.gui.cyclic_update()

    def task_update_altimeter(self):
        self._sch.insert(1000, self.task_update_altimeter)
        self._altimeter.update()


    def add_task(self, ms, task):
        self._sch.insert(ms, task)


    def task_update_bt(self):
        #print("task_update_bt")
        self.add_task(5000, self.task_update_bt)
        if self.settings.bt.value == 1:
            if not g.bt.is_csc_connected() or not g.bt.is_komoot_connected():
                g.bt.scan()

    def task_read_komoot(self):
        #print("task_read_komoot")
        self.add_task(4000, self.task_read_komoot)
        g.bt.read_komoot()

    def task_read_bat(self):
        self.add_task(5000, self.task_read_bat)
        g.hal.update_bat()


    def run(self):
        g.bt.set_on_csc(self.on_data_csc)
        g.bt.set_on_komoot(self.on_data_komoot)
        self.task_update_bt()
        self.task_read_komoot()
        self.task_read_bat()
        while(True):
            try:
                self._sch.run()
            except OSError:
                print("OSError")
