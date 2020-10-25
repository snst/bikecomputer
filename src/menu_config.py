from menu_item import *


class MenuMain:
    def __init__(self):
        self.title = "Menu"
        self.items = [ MenuItem("Goal", "go_menu_goal"),
                       MenuItem("Settings", "go_menu_settings"),
                       MenuItem("Meter", "go_menu_meter")
        ]
        pass


class MenuMeter:
    def __init__(self):
        self.title = "Reset"
        self.items = [ 
                       MenuItem("Add", "do_add_meter"),
                       MenuItem("Reset", "do_reset_meter"),
        ]
        pass    


class MenuSettings:
    def __init__(self, data):
        self.title = "Setting"
        self.data = data
        self.led_on = MenuValueItem("LED on", data.led_on)
        self.led_off = MenuValueItem("LED off", data.led_off)
        self.led_time = MenuValueItem("LED time",  data.led_time)
        self.touch_ignore = MenuValueItem("Off ignore", data.touch_ignore)
        self.wheel_cm = MenuValueItem("Wheel cm", data.wheel_cm)
        self.min_speed = MenuValueItem("min km/h", data.min_speed)
        self.long_click = MenuValueItem("Long click", data.long_click)
        self.bluetooth = MenuValueItem("BT on", data.bt)
        self.items = [ self.led_on,
                       self.led_off,
                       self.led_time,
                       self.wheel_cm,
                       self.min_speed,
                       self.touch_ignore,
                       self.long_click,
                       self.bluetooth,
                       MenuItem("dis- connect", "do_reconnect"),
                       MenuItem("save", "do_save_settings"),
        ]
        pass        


class MenuGoal:
    def __init__(self, data):
        self.title = "Goal"
        self.data = data
        self.dist = MenuValueItem("Dist", data.target_dist_km, data.calculate_time)
        self.avg = MenuValueItem("Avg", data.target_average_km_h, data.calculate_time)
        self.time = MenuValueItem("Time", data.target_time_min, data.calculate_avg)
        self.save = MenuItem("Save", "do_save_goal")
        self.load = MenuItem("Load", "do_load_goal")
        self.stop = MenuItem("Stop", "do_stop_goal")
        self.start = MenuItem("Start", "do_start_goal")
        self.items = [ self.dist,
                       self.avg,
                       self.time,
                       self.save,
                       self.load,
                       self.stop,
                       self.start
        ]
        pass    