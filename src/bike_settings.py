class SettingVal:
    def __init__(self, name, default_val, min_val, max_val, is_float = False, action = None):
        self.name = name
        self.value = default_val
        self.min = min_val
        self.max = max_val
        self.is_float = is_float
        self.action = action


class BikeSettings:
    def __init__(self):
        self.title = "Setting"
        self.led_on = SettingVal("led on", 5, 0, 10)
        self.led_off = SettingVal("led off", 4, 1, 9)
        self.led_time = SettingVal("time", 0, 0, 15)
        self.wheel_cm = SettingVal("wheel", 214, 200, 230, True)
        self.touch_ignore = SettingVal("touchign", 1, 0, 1)
        self.items = [ self.led_on,
                       self.led_off,
                       self.led_time,
                       self.wheel_cm,
                       self.touch_ignore,
                       SettingVal("save", None, None, None),
        ]
        pass


class GoalSettings:
    def __init__(self):
        self.title = "Goal"
        self.dist = SettingVal("dist", 30, 1, 200)
        self.avg = SettingVal("avg", 30, 10, 45)
        self.time = SettingVal("time", 60, 1, 300)
        self.start = SettingVal("Start", None, None, None, "do_start_goal")
        self.items = [ self.dist,
                       self.avg,
                       self.time,
                       self.start
        ]
        pass    