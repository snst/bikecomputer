from gui_main import *
from data_settings import *
from trip_data import *
from goal_data import *
from nav_data import *
from display_ctrl import *
from const import *
from button_handler import *
import data_global as g
from scheduler import *
from item_list import *
from env_data import *
from cycle_data import *

class BikeComputer:
    def __init__(self):
        self._settings = DataSettings()
        self._settings.load()
        self._scheduler = Scheduler(g.hal)
        self._env_data = EnvData()
        self._cycling = CycleData(self._settings)
        self._nav_data = NavData()
        self._display_ctrl = DisplayCtrl(self._settings)
        self._goal_data = GoalData(self._settings)
        self._goal_data.load()
        self.gui = GuiMain(self._settings, self._nav_data, self._goal_data, self._cycling, self._env_data)
        self._btn_left = ButtonHandler(g.hal, g.hal.btn_left, self.btn_event, Button.left, self._settings.long_click.value) 
        self._btn_right = ButtonHandler(g.hal, g.hal.btn_right, self.btn_event, Button.right, self._settings.long_click.value)

    def on_cycle_data(self, raw_data):
        self._cycling.queue_raw_data(raw_data)

    def task_process_csc_data(self):
        self._scheduler.insert(100, self.task_process_csc_data)
        while self._cycling.process():
            ms = g.hal.ticks_ms()
            for trip in self.gui.trip_list:
                trip.process(self._cycling, ms)
            self._goal_data.process(self._cycling, ms)

    def on_altitude_data(self, altitude):
        for trip in self.gui.trip_list:
            trip.altitude.process(altitude, self._settings.altimeter_step.value / 100, self._cycling.is_riding)

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
        self._scheduler.insert(500, self.task_update_gui)
        self.gui.cyclic_update()

    def add_task(self, ms, task):
        self._scheduler.insert(ms, task)

    def task_update_bt(self):
        self.add_task(5000, self.task_update_bt)
        try:
            if (self._settings.csc_on.value and not g.bt.is_csc_connected()) \
                or (self._settings.nav_enabled.value and not g.bt.is_nav_connected()):
                #print("g.bt.scan()")
                g.bt.scan(csc_enabled = self._settings.csc_on.value, komoot_enabled = self._settings.nav_enabled.value)
            #else:
                #print("g.bt.stop_scan()")
                #g.bt.stop_scan()
        except OSError as exc:
                print("BT: OSError %d" % exc.args[0])

    def task_read_komoot(self):
        self.add_task(self._settings.nav_req_interval.value, self.task_read_komoot)
        try:
            if self._settings.nav_enabled.value:
                g.bt.read_komoot()
        except OSError as exc:
                print("komoot: OSError %d" % exc.args[0])            

    def task_update_altimeter(self):
        self._scheduler.insert(self._settings.altimeter_time_ms.value, self.task_update_altimeter)
        if self._settings.altimeter_enabled.value:
            self._env_data.update_altitude()
            self.on_altitude_data(self._env_data.altitude)

    def task_read_bat(self):
        self.add_task(60000, self.task_read_bat)
        self.request_sensor_bat()
        self.request_computer_bat()

    def request_sensor_bat(self):
        g.bt.request_sensor_bat()

    def request_computer_bat(self):
        self._env_data.computer_bat_volt = g.hal.update_bat()

    def run(self):
        g.bt.register_cycle_callback(cycle_cb = self.on_cycle_data, bat_cb = self._env_data.on_sensor_bat)
        g.bt.register_komoot_callback(self._nav_data.on_data)
        self.task_update_bt()
        self.task_read_komoot()
        #self.task_read_bat()
        self.task_update_gui()
        self.task_update_altimeter()
        self.task_process_csc_data()
        while(True):
            try:
                self._scheduler.run()
            except OSError as exc:
                print("OSError %d" % exc.args[0])
