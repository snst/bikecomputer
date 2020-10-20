from data_store import *
from setting_val import *


filename = "settings.cfg"

class DataSettings(DataStore):
    def __init__(self):
        self.led_time = SettingVal(0, 0, 15)
        self.led_on = SettingVal(7, 1, 10)
        self.led_off = SettingVal(3, 0, 10)
        self.touch_ignore = SettingVal(0, 0, 1)
        self.wheel_cm = SettingVal(214, 200, 230, True)
        self.long_click = SettingVal(30, 20, 50)
        self.min_speed = SettingVal(5, 1, 10)
        self.bt = SettingVal(0, 0, 1)
        pass

    def save(self, hal):
        DataStore.save(self, filename, hal)

    def load(self, hal):
        DataStore.load(self, filename, hal)