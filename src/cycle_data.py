import struct
from csc_val import *
from smooth import *
from const import *

class SmoothSpeed:
    def __init__(self, n):
        self.n = n
        self.elem = []

    def add(self, delta_counter, delta_ticks):
        sum_counter = 0
        sum_ticks = 0
        self.elem.append((delta_counter, delta_ticks))
        while len(self.elem) > self.n:
            del self.elem[0]
        for e in self.elem:
            sum_counter += e[0]
            sum_ticks += e[1]
        l = len(self.elem)
        return (sum_counter/l, sum_ticks/l)


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
        self.smooth_speed2  = SmoothSpeed(3)

    def calc_speed_kmh_from_ms(self, wheel_counter, time_ms):
        if time_ms > 0:
            # wheel_counter * wheel_cm     3600
            # ------------------------  *  ---------------
            #         100 * 1000           time_ms / 1000
            return (self._settings.wheel_cm.value * wheel_counter * 36) / (time_ms)
        else:
            return 0

    def calc_speed_kmh(self, wheel_counter, time_ticks):
        if time_ticks > 0:
            # wheel_counter * wheel_cm     3600
            # ------------------------  *  ---------------
            #         100 * 1000           time_ticks / 1024
            return (1024 * self._settings.wheel_cm.value * wheel_counter * 36) / (1000 * time_ticks)
        else:
            return 0

    def calc_cadence_from_ms(self, counter_delta, ms_delta):
        if ms_delta > 0:
            return 1000 * counter_delta * 60 / ms_delta
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
            self.calculate(self.wheel_counter_delta, self.wheel_time_delta, self.crank_counter_delta, self.crank_time_delta)
        self.init = True
        return self.init

    def calculate(self, wheel_counter_delta, wheel_time_delta, crank_counter_delta, crank_time_delta):
        wc, wt = self.smooth_speed2.add(wheel_counter_delta, wheel_time_delta)
        self.speed = self.calc_speed_kmh(wc, wt)
        #speed = self.calc_speed_kmh(wheel_counter_delta, wheel_time_delta)
        #self.speed = self.smooth_speed(speed)

        cadence = self.calc_cadence(crank_counter_delta, crank_time_delta)
        self.cadence = self.smooth_cadence(cadence)

        self.is_riding = self.calc_is_riding(self.speed)
        self.has_valid_cadence = self.calc_has_valid_cadence(self.cadence)

    def smooth_speed(self, speed):
        return round(self._smooth_speed.add(speed, self._settings.csc_smooth.value), 1)

    def smooth_cadence(self, cadence):
        return (int)(self._smooth_cadence.add(cadence, self._settings.csc_smooth.value))

    def calc_is_riding(self, speed):
        return speed <= Limits.max_valid_speed and speed >= self._settings.min_speed.value

    def calc_has_valid_cadence(self, cadence):
        return cadence >= self._settings.min_cadence.value and cadence <= Limits.max_valid_cadence

    def convert_wheel_count_to_km(self, wheel_count): #ut
        return wheel_count * self._settings.wheel_cm.value / 100000

    def convert_wheel_ticks_to_sec(self, wheel_ticks): #ut
        return wheel_ticks / 1024

    @property
    def wheel_counter_delta(self):
        return self.wheel_counter.delta

    @property
    def wheel_time_delta(self):
        return self.wheel_time.delta

    @property
    def crank_counter_delta(self):
        return self.crank_counter.delta

    @property
    def crank_time_delta(self):
        return self.crank_time.delta                        