from data_store import *
from setting_val import *


filename = b'settings.cfg'

class DataSettings(DataStore):
    def __init__(self):
        self.led_time = SettingVal(0, 0, 15)
        self.led_on = SettingVal(7, 1, 10)
        self.led_off = SettingVal(3, 0, 10)
        self.touch_ignore = SettingVal(0, 0, 1)
        self.wheel_cm = SettingVal(214, 200, 230, True)
        self.long_click = SettingVal(300, 200, 500, False, 10)
        self.min_speed = SettingVal(5, 0, 10)
        self.min_cadence = SettingVal(10, 0, 50)
        self.csc_on = SettingVal(0, 0, 1)
        self.csc_smooth = SettingVal(3, 1, 20)
        self.nav_enabled = SettingVal(0, 0, 1)
        self.nav_flash_on = SettingVal(500, 100, 1000, False, 25)
        self.nav_all_on = SettingVal(500, 100, 1000)
        self.nav_auto_on = SettingVal(1, 0, 1)
        self.nav_red_color = SettingVal(300, 25, 2000, False, 25)
        self.nav_req_interval = SettingVal(2000, 500, 4000, False, 500)
        self.nav_street_dist = SettingVal(1000, 0, 5000, False, 250)
        self.altimeter_enabled = SettingVal(0, 0, 1)
        self.altimeter_values = SettingVal(5, 1, 10)
        self.altimeter_time_ms = SettingVal(500, 500, 10000, False, 500)
        self.altimeter_step = SettingVal(10, 0, 200, False, 5)
        pass

    def save(self):
        DataStore.save(self, filename)

    def load(self):
        DataStore.load(self, filename)