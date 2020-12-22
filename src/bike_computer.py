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
from meter_data import *
from env_data import *

class BikeComputer:
    def __init__(self):
        self._settings = DataSettings()
        self._settings.load()
        self._scheduler = Scheduler(g.hal)
        self.env_data = EnvData()
        self.meter_list = []
        self.add_meter_instance()
        self.komoot_data = KomootData()
        self._display_ctrl = DisplayCtrl(self._settings)
        self._goal_data = GoalData(self._settings)
        self._goal_data.load()
        self.gui = GuiMain(self._settings, self.meter_list, self.komoot_data, self._goal_data)
        self._btn_left = ButtonHandler(g.hal, g.hal.btn_left, self.btn_event, Button.left, self._settings.long_click.value) 
        self._btn_right = ButtonHandler(g.hal, g.hal.btn_right, self.btn_event, Button.right, self._settings.long_click.value)
        self._altimeter = Altimeter()

    def on_cycle_data(self, raw_data):
        for meter in self.meter_list:
            meter.cycle_data.process(raw_data)
        #self._goal_data.process(raw_data)

    def on_altitude_data(self, altitude):
        for meter in self.meter_list:
            meter.alt_data.process(altitude, self._settings.altimeter_step.value / 100, meter.cycle_data.is_riding)

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
        if (self._settings.csc_on.value and not g.bt.is_csc_connected()) or (self._settings.komoot_enabled.value and not g.bt.is_komoot_connected()):
            g.bt.scan(csc_enabled = self._settings.csc_on.value, komoot_enabled = self._settings.komoot_enabled.value)

    def task_read_komoot(self):
        self.add_task(self._settings.komoot_req_interval.value, self.task_read_komoot)
        if self._settings.komoot_enabled.value:
            g.bt.read_komoot()

    def task_update_altimeter(self):
        self._scheduler.insert(self._settings.altimeter_time_ms.value, self.task_update_altimeter)
        if None != self._altimeter and self._settings.altimeter_enabled.value:
            self._altimeter.update()
            self.on_altitude_data(self._altimeter.altitude)

    def task_read_bat(self):
        self.add_task(5000, self.task_read_bat)
        self.request_sensor_bat()
        self.request_computer_bat()

    def request_sensor_bat(self):
        g.bt.request_sensor_bat()

    def request_computer_bat(self):
        self.env_data.computer_bat_volt = g.hal.update_bat()

    def run(self):
        g.bt.register_cycle_callback(cycle_cb = self.on_cycle_data, bat_cb = self.env_data.on_sensor_bat)
        g.bt.register_komoot_callback(self.komoot_data.on_data)
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

    def get_current_meter(self):
        return self.gui.get_current_meter()

    def get_current_cycle_data(self):
        return self.gui.get_current_meter().cycle_data

    def reset_current_altimeter(self):
        self.get_current_meter().alt_data.reset()

    def add_meter_instance(self):
        id = len(self.meter_list) + 1
        meter = MeterData(id, self.env_data, self._settings)
        self.meter_list.append(meter)
        return meter
     
    def get_goal(self):
        return self._goal_data