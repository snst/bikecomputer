from menu_item import *
from goal_data import *

class MenuMain:
    def __init__(self):
        self.title = "Menu"
        self.items = [ MenuItem("Display", "go_menu_settings"),
                       MenuItem("CSC", "gui_show_csc_menu"),
                       MenuItem("Altimeter", "gui_show_altimeter_menu"),
                       MenuItem("Komoot", "gui_show_komoot_menu"),
                       MenuItem("BLE scan", "ble_reconnect"),
                       LambdaMenuItem("Display off", lambda: g.bc._display_ctrl.set_display_complete_off),
                       MenuItem("Save", "save_settings"),
        ]
        pass


class MenuMeter:
    def __init__(self, main, data):
        self.title = "Reset"
        self.items = [ 
                       LambdaMenuItem("Stop" if data.cycle_data.is_started else "Start", lambda : main.enable_meter(data, not data.cycle_data.is_started)),
                       LambdaMenuItem("Reset", lambda : main.reset_meter(data)),
                       MenuItem("Add meter", "add_meter"),
        ]
        if data.id != 1:
            self.items.append(MenuItem("Del meter", "del_meter"))
        if not main._goal_visible:
            self.items.append(LambdaMenuItem("Show goal", lambda: main.show_goal_meter(True)))
        pass    


class MenuSettings:
    def __init__(self, data):
        self.title = "Display"
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
                       MenuItem("Save", "save_settings"),
        ]
        pass        

class MenuAltimeter:
    def __init__(self, main, meter, data):
        self.title = "alt"
        self.data = data
        self.altimeter_enabled = MenuValueItem("Enabled;altimeter", data.altimeter_enabled)
        self.altimeter_values = MenuValueItem("Number of;avg values", data.altimeter_values)
        self.altimeter_time_ms = MenuValueItem("Scan interval;ms", data.altimeter_time_ms)
        self.altimeter_step = MenuValueItem("Step cm", data.altimeter_step)
        self.items = [ 
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
    def __init__(self, main, data):
        self.title = "Goal"
        self.data = data
        self.dist = MenuValueItem("Distance km", data.target_dist_km, data.calculate_time)
        self.avg = MenuValueItem("Average km/h", data.target_average_km_h, data.calculate_time)
        self.time = MenuValueItem("Time min", data.target_time_min, data.calculate_avg)
        self.items = [ LambdaMenuItem("Stop" if data.is_started else "Start", lambda : main.enable_meter(data, not data.is_started)),
                       LambdaMenuItem("Reset", lambda : main.reset_meter(data)),
                       self.dist,
                       self.avg,
                       self.time,
                       LambdaMenuItem("Hide", lambda: main.show_goal_meter(False)),
                       MenuItem("Save", "save_goal_settings"),
                       MenuItem("Load", "load_goal_settings"),
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