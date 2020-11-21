from menu_item import *


class MenuMain:
    def __init__(self):
        self.title = "Menu"
        self.items = [ MenuItem("Goal", "gui_show_goal_menu"),
                       MenuItem("Settings", "go_menu_settings"),
                       MenuItem("Meter", "gui_show_meter_menu")
        ]
        pass


class MenuMeter:
    def __init__(self):
        self.title = "Reset"
        self.items = [ 
                       MenuItem("Add", "add_meter"),
                       MenuItem("Reset", "reset_meter"),
        ]
        pass    


class MenuSettings:
    def __init__(self, data):
        self.title = "Setting"
        self.data = data
        self.led_on = MenuValueItem("LED on", data.led_on)
        self.led_off = MenuValueItem("LED off", data.led_off)
        self.led_time = MenuValueItem("LED time",  data.led_time)
        self.touch_ignore = MenuValueItem("Off ign", data.touch_ignore)
        self.wheel_cm = MenuValueItem("Wheel cm", data.wheel_cm)
        self.min_speed = MenuValueItem("Min km/h", data.min_speed)
        self.long_click = MenuValueItem("Long clk", data.long_click)
        self.bluetooth = MenuValueItem("BLE on", data.bt)
        self.items = [ self.led_on,
                       self.led_off,
                       self.led_time,
                       self.wheel_cm,
                       self.min_speed,
                       self.touch_ignore,
                       self.long_click,
                       self.bluetooth,
                       MenuItem("BLE scan", "ble_reconnect"),
                       MenuItem("Save", "save_settings"),
        ]
        pass        


class MenuGoal:
    def __init__(self, data):
        self.title = "Goal"
        self.data = data
        self.dist = MenuValueItem("Dist", data.target_dist_km, data.calculate_time)
        self.avg = MenuValueItem("Avg", data.target_average_km_h, data.calculate_time)
        self.time = MenuValueItem("Time", data.target_time_min, data.calculate_avg)
        self.save = MenuItem("Save", "save_goal_settings")
        self.load = MenuItem("Load", "load_goal_settings")
        self.stop = MenuItem("Stop", "stop_goal")
        self.start = MenuItem("Start", "start_goal")
        self.items = [ self.dist,
                       self.avg,
                       self.time,
                       self.save,
                       self.load,
                       self.stop,
                       self.start
        ]
        pass    