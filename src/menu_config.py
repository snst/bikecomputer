from menu_item import *


class MenuMain:
    def __init__(self):
        self.title = "Menu"
        self.items = [ MenuItem("Goal", "gui_show_goal_menu"),
                       MenuItem("Settings", "go_menu_settings"),
                       MenuItem("Meter", "gui_show_meter_menu"),
                       MenuItem("CSC", "gui_show_csc_menu"),
                       MenuItem("Komoot", "gui_show_komoot_menu"),
                       MenuItem("Altimeter", "gui_show_altimeter_menu"),
        ]
        pass


class MenuMeter:
    def __init__(self):
        self.title = "Reset"
        self.items = [ 
                       MenuItem("Reset", "reset_cycle_meter"),
                       MenuItem("Add", "add_meter"),
        ]
        pass    


class MenuSettings:
    def __init__(self, data):
        self.title = "Setting"
        self.data = data
        self.led_on = MenuValueItem("LED;brightness on", data.led_on)
        self.led_off = MenuValueItem("LED;brightness off", data.led_off)
        self.led_time = MenuValueItem("LED;duration on",  data.led_time)
        self.touch_ignore = MenuValueItem("Ignore click;when LED off", data.touch_ignore)
        self.long_click = MenuValueItem("Long click;duration ms", data.long_click)
        self.items = [ self.led_on,
                       self.led_off,
                       self.led_time,
                       self.touch_ignore,
                       self.long_click,
                       MenuItem("BLE scan", "ble_reconnect"),
                       MenuItem("Save", "save_settings"),
        ]
        pass        

class MenuAltimeter:
    def __init__(self, data):
        self.title = "alt"
        self.data = data
        self.altimeter_enabled = MenuValueItem("Enabled;altimeter", data.altimeter_enabled)
        self.altimeter_values = MenuValueItem("Number of;avg values", data.altimeter_values)
        self.altimeter_time_ms = MenuValueItem("Scan interval;ms", data.altimeter_time_ms)
        self.altimeter_step = MenuValueItem("Step cm", data.altimeter_step)
        self.items = [ 
                       MenuItem("Reset", "reset_altimeter"),
                       self.altimeter_enabled,
                       self.altimeter_values,
                       self.altimeter_time_ms,
                       self.altimeter_step,
                       MenuItem("Save", "save_settings"),
        ]
        pass        


class MenuCSC:
    def __init__(self, data):
        self.title = "csc"
        self.data = data
        self.csc_on = MenuValueItem("Enable BLE", data.csc_on)
        self.wheel_cm = MenuValueItem("Wheel cm", data.wheel_cm)
        self.min_speed = MenuValueItem("Min km/h", data.min_speed)
        self.min_cadence = MenuValueItem("Min cadence", data.min_cadence)
        self.items = [ self.csc_on,
                       self.wheel_cm,
                       self.min_speed,
                       self.min_cadence,
                       MenuItem("Save", "save_settings"),
        ]
        pass        

class MenuGoal:
    def __init__(self, data):
        self.title = "Goal"
        self.data = data
        self.dist = MenuValueItem("Distance km", data.target_dist_km, data.calculate_time)
        self.avg = MenuValueItem("Average km/h", data.target_average_km_h, data.calculate_time)
        self.time = MenuValueItem("Time min", data.target_time_min, data.calculate_avg)
        self.save = MenuItem("Save", "save_goal_settings")
        self.load = MenuItem("Load", "load_goal_settings")
        self.stop = MenuItem("Stop", "stop_goal")
        self.start = MenuItem("Start", "start_goal")
        self.reset = MenuItem("Reset", "reset_goal")
        start_stop = self.stop if data.is_started else self.start
        self.items = [ start_stop,
                       self.reset,
                       self.dist,
                       self.avg,
                       self.time,
                       self.save,
                       self.load,
        ]
        pass    


class MenuKomoot:
    def __init__(self, data):
        self.title = "Komoot"
        self.data = data
        self.komoot_enabled = MenuValueItem("Enable BLE", data.komoot_enabled)
        self.komoot_auto_on = MenuValueItem("Auto switch on;LED", data.komoot_auto_on)
        self.komoot_flash_on = MenuValueItem("Warn LED;before m", data.komoot_flash_on)
        self.komoot_all_on = MenuValueItem("Steady LED;before m", data.komoot_all_on)
        self.komoot_red_color = MenuValueItem("Red color;before m", data.komoot_red_color)
        self.komoot_req_interval = MenuValueItem("BLE update ms", data.komoot_req_interval)
        self.items = [ self.komoot_enabled,
                       self.komoot_auto_on,
                       self.komoot_flash_on,
                       self.komoot_all_on,
                       self.komoot_red_color,
                       self.komoot_req_interval,
                       MenuItem("Save", "save_settings"),

        ]
        pass                