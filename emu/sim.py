import threading
import time
import struct
from random import random
import math



class Sim:
    def __init__(self, bike_computer):
        self.gui = bike_computer.gui
        self.data = bike_computer.data
        #self.set_demo_data(self.data)
        self.csc = bike_computer.csc
        self.display = bike_computer.display
        self.wheel_counter = 0
        self.wheel_event = 0
        self.crank_counter = 0
        self.crank_event = 0
        self.last_ms = self.get_ms()
        self.s = 0
        self.display.set_callback(self.gui.tft.display_on)
        self.gui.tft.set_gui(self.gui)

    def set_demo_data(self, data):
        data.speed = 33.7
        data.speed_avg = 29.2
        data.speed_max = 44.2
        data.cadence = 93
        data.cadence_avg = 80
        data.trip_distance = 114.22
        data.trip_duration = (60*4 + 33 + 12)

    def get_ms(self):
        return int(round(time.time() * 1000))

    def generate_data2(self):
        #print("hello, Timer")
        self.data.speed += 0.1
        self.data.speed_avg += 0.01
        self.data.speed_max += 0.03
        self.data.cadence += 0.2
        self.data.cadence_avg += 0.1
        self.start()
        self.gui.tft.tk.after(10, self.gui.cyclic_update)

    def generate_data(self):
        now = self.get_ms()
        delta_ticks = (int)((now - self.last_ms) / 1000 * 1024)
        self.last_ms = now

        #delta_ticks = (int)(1024 + (100 * random()))
        #delta_ticks = (int)(2024 + 1012 * math.sin(self.s))
        delta_ticks = 1024
        self.s += 0.1

        val1 = struct.pack("<BIHHH", 0, self.wheel_counter,self.wheel_event & 0xFFFF, self.crank_counter & 0xFFFF, self.crank_event & 0xFFFF)
        self.csc.on_notify(val1)
        self.start()
        #self.gui.tft.tk.after(10, self.gui.cyclic_update)
        self.wheel_counter += 2
        self.wheel_event += delta_ticks
        self.crank_counter += 1
        self.crank_event += delta_ticks
        self.gui.cyclic_update()
        pass

    def start(self):
        self.t = threading.Timer(1.0, self.generate_data)
        self.t.start()