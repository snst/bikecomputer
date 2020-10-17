

class SettingVal:
    def __init__(self, value, min, max, is_float = False):
        self.value = value
        self.min = min
        self.max = max
        self.is_float = is_float


class DataSettings:
    def __init__(self):
        self.led_time = SettingVal(0, 0, 15)
        self.led_on = SettingVal(7, 0, 10)
        self.led_off = SettingVal(3, 0, 10)
        self.touch_ignore = SettingVal(0, 0, 1)
        self.wheel_cm = SettingVal(214, 200, 230, True)
        self.long_click = SettingVal(30, 20, 50)
        self.min_speed = SettingVal(5, 1, 10)
        pass