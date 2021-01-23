import struct
from csc_val import *
from smooth import *
from const import *

class CycleData:
    def __init__(self, settings):
        self.reset()
        self._settings = settings

    def reset(self):
        self.init = False
        self.wheel_counter = CscVal(Max.uint32)
        self.wheel_time = CscVal(Max.uint16)
        self.crank_counter = CscVal(Max.uint16)
        self.crank_time = CscVal(Max.uint16)
        self.speed = 0
        self._smooth_speed = Smooth()
        self.cadence = 0
        self._smooth_cadence = Smooth()
        self.is_riding = False
        self.sim = 10
        self.has_valid_cadence = False

    def calc_speed_kmh(self, wheel_counter, time_ticks):
        if time_ticks > 0:
            # wheel_counter * wheel_cm     3600
            # ------------------------  *  ---------------
            #         100 * 1000           time_ticks / 1024
            return (1024 * self._settings.wheel_cm.value * wheel_counter * 36) / (1000 * time_ticks)
        else:
            return 0

    def calc_cadence(self, counter_delta, time_ticks):
        if time_ticks > 0:
            return 1024 * counter_delta * 60 / time_ticks
        else:
            return 0

    def unpack_data(self, data):
        val = struct.unpack("<BIHHH", data)
        return val[1], val[2], val[3], val[4]
    
    def process(self, raw_data):
        wheel_counter, wheel_time, crank_counter, crank_time = self.unpack_data(raw_data)

        self.wheel_counter.calc_delta(wheel_counter)
        self.wheel_time.calc_delta(wheel_time)
        self.crank_counter.calc_delta(crank_counter)
        self.crank_time.calc_delta(crank_time)
        #self.wheel_counter.print("wc")
        #self.wheel_time.print("wt")
        #self.crank_counter.print("cc")
        #self.crank_time.print("ct")
        if self.init:
            self.calculate()
        self.init = True
        return self.init

    def calculate(self):
        #self.speed = round(self.calc_speed_kmh(self.wheel_counter.delta, self.wheel_time.delta), 1)
        speed = self.calc_speed_kmh(self.wheel_counter.delta, self.wheel_time.delta)
        self.speed = round(self._smooth_speed.add(speed, self._settings.csc_smooth.value), 1)
        #self.cadence = (int)(self.calc_cadence(self.crank_counter.delta, self.crank_time.delta))
        cadence = self.calc_cadence(self.crank_counter.delta, self.crank_time.delta)
        self.cadence = (int)(self._smooth_cadence.add(cadence, self._settings.csc_smooth.value))

        #print("r=%d, km/h=%f, cad=%d" % (self.is_riding, self.speed, self.cadence))
        self.is_riding = self.calc_is_riding(self.speed)
        self.has_valid_cadence = self.calc_has_valid_cadence(self.cadence)

    def calc_is_riding(self, speed):
        return speed <= Limits.max_valid_speed and speed >= self._settings.min_speed.value

    def calc_has_valid_cadence(self, cadence):
        return cadence >= self._settings.min_cadence.value and cadence <= Limits.max_valid_cadence

    def convert_wheel_count_to_km(self, wheel_count): #ut
        return wheel_count * self._settings.wheel_cm.value / 100000

    def convert_wheel_ticks_to_min(self, wheel_ticks): #ut
        return wheel_ticks / (60 * 1024)