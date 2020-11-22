import st7789

class Layout:
    y_breadcrum = 10
    y_setting_text = 60
    y_setting_val = 125


class Button:
    left = 0
    right = 1
    short = 1 << 8 
    long = 1 << 9


class Event:
    go_main_menu = Button.right | Button.long
    toggle_komoot = Button.left | Button.short
    go_next_view = Button.right | Button.short
    go_next_meter = Button.left | Button.long
    menu_next = Button.right | Button.long
    menu_prev = Button.left | Button.long
    val_inc = Button.right | Button.short
    val_dec = Button.left | Button.short
    
class Color:
    black = st7789.color565(0, 0, 0)
    white = st7789.color565(255, 255, 255)
    grey = st7789.color565(44, 44, 44)
    red = st7789.color565(255, 0, 0)
    green = st7789.color565(0, 200, 0)    
    yellow = st7789.color565(200, 200, 0)    
    blue = st7789.color565(0, 0, 255)    

class Align:
    left = 0
    center = 1
    right = 2


class ConnState:
    disconnected = 0
    scanning = 1
    connecting = 2
    connected = 3
    no_device = 4
    found_device = 5
    off = 6

class StateFlags:
    riding = 1
    bt_on = 2