import st7789

class Layout:
    y_breadcrum = 10
    y_line05 = 35
    y_line0 = 40
    y_line1 = 80
    y_line2 = 120

class Button:
    left = 0
    right = 1
    
class Color:
    black = st7789.color565(0, 0, 0)
    white = st7789.color565(255, 255, 255)
    grey = st7789.color565(44, 44, 44)
    red = st7789.color565(255, 0, 0)
    green = st7789.color565(0, 200, 0)    
    yellow = st7789.color565(200, 200, 0)    

class Display:
    width = 135
    height = 240

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