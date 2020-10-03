from menu_item import *


class MenuMain:
    def __init__(self):
        self.title = "Menu"
        self.items = [ MenuItem("Settings", "go_menu_settings"),
                       MenuItem("Reset", "go_menu_reset"),
                       MenuItem("Goal", "go_menu_goal")
        ]
        pass


class MenuReset:
    def __init__(self):
        self.title = "Reset"
        self.items = [ MenuItem("Trip", "do_reset_trip"),
                       MenuItem("Max", "do_reset_max"),
                       MenuItem("Avg", "do_reset_avg"),
        ]
        pass    


class MenuSettings:
    def __init__(self, data):
        self.title = "Setting"
        self.data = data
        self.led_on = MenuValueItem("led on", data.led_on)
        self.led_off = MenuValueItem("led off", data.led_off)
        self.led_time = MenuValueItem("time",  data.led_time)
        self.wheel_cm = MenuValueItem("wheel", data.wheel_cm)
        self.touch_ignore = MenuValueItem("touchign", data.touch_ignore)
        self.items = [ self.led_on,
                       self.led_off,
                       self.led_time,
                       self.wheel_cm,
                       self.touch_ignore,
                       MenuItem("save", "do_save_settings"),
        ]
        pass        


class MenuGoal:
    def __init__(self, data):
        self.title = "Goal"
        self.data = data
        self.dist = MenuValueItem("dist", data.dist)
        self.avg = MenuValueItem("avg", data.average)
        self.time = MenuValueItem("time", data.time)
        self.start = MenuItem("Start", "do_start_goal")
        self.items = [ self.dist,
                       self.avg,
                       self.time,
                       self.start
        ]
        pass    