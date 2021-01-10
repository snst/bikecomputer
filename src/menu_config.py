from menu_item import *
from goal_data import *

class MenuMain:
    def __init__(self, main):
        self.title = b'Menu'
        self.items = [ MenuItem(b'Display', lambda : main.go_menu_settings()),
                       MenuItem(b'CSC', lambda : main.gui_show_csc_menu()),
                       MenuItem(b'Altimeter', lambda : main.gui_show_altimeter_menu()),
                       MenuItem(b'Komoot', lambda : main.gui_show_komoot_menu()),
                       MenuItem(b'BLE;scan', lambda : main.ble_reconnect()),
                       MenuItem(b'Display;off', lambda: g.bc._display_ctrl.set_display_complete_off()),
                       MenuItem(b'Save', lambda : main.save_settings()),
        ]
        pass


class MenuMeter:
    def __init__(self, main, data):
        self.title = b'Meter'
        self.items = [ 
                       MenuItem(b'Stop' if data.is_started else b'Start', lambda : main.enable_meter(data, not data.is_started)),
                       MenuItem(b'Reset', lambda : main.reset_meter(data)),
                       MenuItem(b'Save', lambda : main.save_trip(data)),
                       MenuItem(b'Load', lambda : main.load_trip(data)),
                       MenuItem(b'+ Meter', lambda : main.add_trip()),
        ]
        if data.id != 1:
            self.items.append(MenuItem(b'- Meter', lambda : main.del_trip()))
        if not main._goal_visible:
            self.items.append(MenuItem(b'Goal', lambda: main.show_goal_meter(True)))
        if main._settings.komoot_enabled.value == 0:
            self.items.append(MenuItem(b'Komoot', lambda : main.enable_komoot()))
        pass    


class MenuSettings:
    def __init__(self, main):
        self.title = b'Display'
        self.data = main._settings
        self.led_on = MenuValueItem(b'LED;brightness on', self.data.led_on)
        self.led_off = MenuValueItem(b'LED;brightness off', self.data.led_off)
        self.led_time = MenuValueItem(b'LED;duration on',  self.data.led_time)
        self.touch_ignore = MenuValueItem(b'Ignore click;when LED off', self.data.touch_ignore)
        self.long_click = MenuValueItem(b'Long click;duration ms', self.data.long_click)
        self.items = [ self.led_on,
                       self.led_off,
                       self.led_time,
                       self.touch_ignore,
                       self.long_click,
                       MenuItem(b'Save', lambda : main.save_settings()),
        ]
        pass        

class MenuAltimeter:
    def __init__(self, main):
        self.title = b'Altimeter'
        self.data = main._settings
        self.altimeter_enabled = MenuValueItem(b'Enabled;altimeter', self.data.altimeter_enabled)
        self.altimeter_values = MenuValueItem(b'Number of;avg values', self.data.altimeter_values)
        self.altimeter_time_ms = MenuValueItem(b'Scan interval;ms', self.data.altimeter_time_ms)
        self.altimeter_step = MenuValueItem(b'Step cm', self.data.altimeter_step)
        self.items = [ 
                       self.altimeter_enabled,
                       self.altimeter_values,
                       self.altimeter_time_ms,
                       self.altimeter_step,
                       MenuItem(b'Save', lambda : main.save_settings()),
        ]
        pass        


class MenuCSC:
    def __init__(self, main):
        self.title = b'CSC'
        self.data = main._settings
        self.csc_on = MenuValueItem(b'Enable BLE', self.data.csc_on)
        self.wheel_cm = MenuValueItem(b'Wheel cm', self.data.wheel_cm)
        self.min_speed = MenuValueItem(b'Min km/h', self.data.min_speed)
        self.min_cadence = MenuValueItem(b'Min cadence', self.data.min_cadence)
        self.items = [ self.csc_on,
                       self.wheel_cm,
                       self.min_speed,
                       self.min_cadence,
                       MenuItem(b'Save', lambda : main.save_settings()),
        ]
        pass        

class MenuGoal:
    def __init__(self, main, data):
        self.title = b'Goal'
        self.data = data
        self.dist = MenuValueItem(b'Distance km', data.target_dist_km, data.calculate_time)
        self.avg = MenuValueItem(b'Average km/h', data.target_average_km_h, data.calculate_time)
        self.time = MenuValueItem(b'Time min', data.target_time_min, data.calculate_avg)
        self.items = [ MenuItem(b'Stop' if data.is_started else b'Start', lambda : main.enable_meter(data, not data.is_started)),
                       MenuItem(b'Reset', lambda : main.reset_meter(data)),
                       self.dist,
                       self.avg,
                       self.time,
                       MenuItem(b'Hide', lambda: main.show_goal_meter(False)),
                       MenuItem(b'Save', lambda : main.save_goal_settings()),
                       MenuItem(b'Load', lambda : main.load_goal_settings()),
        ]
        pass    


class MenuKomoot:
    def __init__(self, main):
        self.title = b'Komoot'
        self.data = main._settings
        self.komoot_enabled = MenuValueItem(b'Enable BLE', self.data.komoot_enabled)
        self.komoot_auto_on = MenuValueItem(b'Auto switch;on LED', self.data.komoot_auto_on)
        self.komoot_flash_on = MenuValueItem(b'Warn LED;before m', self.data.komoot_flash_on)
        self.komoot_all_on = MenuValueItem(b'Steady LED;before m', self.data.komoot_all_on)
        self.komoot_red_color = MenuValueItem(b'Red color;before m', self.data.komoot_red_color)
        self.komoot_req_interval = MenuValueItem(b'BLE update ms', self.data.komoot_req_interval)
        self.komoot_street_dist = MenuValueItem(b'Street;dist m', self.data.komoot_street_dist)
        self.items = [ self.komoot_enabled,
                       self.komoot_auto_on,
                       self.komoot_flash_on,
                       self.komoot_all_on,
                       self.komoot_red_color,
                       self.komoot_req_interval,
                       self.komoot_street_dist,
                       MenuItem(b'Save', lambda : main.save_settings()),

        ]
        pass                