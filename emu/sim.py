import threading
import time
import struct
from random import random
import math



class Sim:
    def __init__(self, bike_computer):
        self.gui = bike_computer.gui
        self._cycle_data = bike_computer._list_csc_data
        #self.set_demo_data(self.data)
        self.bc = bike_computer
        self.wheel_counter = 0
        self.wheel_event = 0
        self.crank_counter = 0
        self.crank_event = 0
        self.last_ms = self.get_ms()
        self.s = 0
        self.speed = 10
        self.paused = True

    def set_demo_data(self, data):
        data.speed = 33.7
        data.speed_avg = 29.2
        data.speed_max = 44.2
        data.cadence = 93
        data.cadence_avg = 80
        data.trip_distance = 114.22
        data.trip_duration_min = (60*4 + 33 + 12)

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
        #now = self.get_ms()
        #delta_ticks = (int)((now - self.last_ms) / 1000 * 1024)
        #self.last_ms = now

        #delta_ticks = (int)(1024 + (100 * random()))
        #delta_ticks = (int)(2024 + 1012 * math.sin(self.s))
        delta_ticks = (int)(1024)
        self.s += 0.1

        val1 = struct.pack("<BIHHH", 0, self.wheel_counter,self.wheel_event & 0xFFFF, self.crank_counter & 0xFFFF, self.crank_event & 0xFFFF)
        self.bc.on_notify(val1)
        self.start()
        #self.gui.tft.tk.after(10, self.gui.cyclic_update)
        self.wheel_counter += 5
        self.wheel_event += delta_ticks
        self.crank_counter += 1
        self.crank_event += delta_ticks
        self.gui.cyclic_update()
        pass

    def simulate(self, speed, sec, factor):

        s = 0
        while s < sec:

            dist = 2 * (speed * 1000) / 36
            n = (dist / 214)
            ng = (int) (n)

            delta_event = (int) (2 * 1024 / n * ng)

            self.wheel_counter += ng
            self.crank_counter += (int) (ng / 3)

            self.wheel_event += delta_event
            self.crank_event += delta_event

            val1 = struct.pack("<BIHHH", 0, self.wheel_counter,self.wheel_event & 0xFFFF, self.crank_counter & 0xFFFF, self.crank_event & 0xFFFF)
            self.bc.on_data_csc(val1)
            #self.gui.cyclic_update()

            time.sleep(1/factor)
            
            s += factor

    def sim1(self):
        while(True):
            i = 5
            #while (i<40):
            #    self.simulate(i, 10, 5)
            #    i += 1
            if not self.paused:
                self.simulate(self.speed, 60, 120)
            else:
                time.sleep(0.5)
            #self.simulate(15, 60, 30)
            #self.simulate(10, 60, 30)
            #self.simulate(15, 60, 30)

    def start(self):
        #self.t = threading.Timer(1.0, self.generate_data)
        self.t = threading.Thread(target=self.sim1)  
        self.t.start()



    def btn_callback(self, btn):
        if btn == 120: #x
            self.speed += 1#0.5
            self.bc.csc_data[0].sim += 1
            pass
        elif btn == 121: #y
            if self.speed > 1:
                self.speed -= 1#0.5
            self.bc.csc_data[0].sim -= 1
            pass
        elif btn == 32: #space
            self.paused = not self.paused
            pass

        print("sim_speed %f, paused=%d" % (self.speed, self.paused))