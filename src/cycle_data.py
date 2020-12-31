import struct
from csc_val import *

class CycleData:
    def __init__(self, id, settings):
        self.reset()
        self.id = id
        self.goal = None
        self._settings = settings

    def reset(self):
        self.init = False
        self.wheel_counter = CscVal(Max.uint32)
        self.wheel_time = CscVal(Max.uint16)
        self.crank_counter = CscVal(Max.uint16)
        self.crank_time = CscVal(Max.uint16)
        self.speed = 0
        self.speed_avg = 0
        self.speed_max = 0
        self.cadence = 0
        self.cadence_avg = 0
        self.trip_distance = 0
        self.trip_duration_min = 0
        self.is_riding = False
        self.sim = 10
        self.is_started = True



    def calc_kmh_from_csc_val(self, wheel_counter, time_counter):
        if time_counter > 0:
            # wheel_counter * wheel_cm     3600
            # ------------------------  *  ---------------
            #         100 * 1000           time_counter / 1024
            return (self._settings.wheel_cm.value * wheel_counter * 36) / (1000 * time_counter / 1024)
        else:
            return 0

    def calc_cadence_from_csc_val(self, crank_counter, time_delta):
        if time_delta > 0:
            return (crank_counter * 60 * 1024) / time_delta
        else:
            return 0


    def calc_kmh(self, counter_delta, time_delta):
        if time_delta > 0:
            return (self._settings.wheel_cm.value * counter_delta * 3.6) / time_delta / 100.0
        else:
            return 0

    def calc_cadence(self, counter_delta, time_delta):
        if time_delta > 0:
            return counter_delta * 60 / time_delta
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

        self.process_data()

    def process_data(self):
        if self.init:
            self.calculate_current_data()
            if self.is_started:
                self.calculate_accumulated_data()
        self.init = True


    def calculate_current_data(self):
        self.speed = self.calc_kmh_from_csc_val(self.wheel_counter.delta, self.wheel_time.delta)
        self.cadence = self.calc_cadence_from_csc_val(self.crank_counter.delta, self.crank_time.delta)

    def calculate_accumulated_data(self):
        if self.cadence >= self._settings.min_cadence.value and self.cadence < 140:
            self.crank_counter.add_delta()
            self.crank_time.add_delta()
        self.cadence_avg = self.calc_cadence_from_csc_val(self.crank_counter.sum, self.crank_time.sum)

        valid_speed = self.speed < 100
        self.is_riding = valid_speed and self.speed >= self._settings.min_speed.value

        if valid_speed:
            self.speed_max = max(self.speed_max, self.speed)

            if self.is_riding:
                self.wheel_counter.add_delta()
                self.wheel_time.add_delta()
        self.speed_avg = self.calc_kmh_from_csc_val(self.wheel_counter.sum, self.wheel_time.sum)

        self.trip_distance = self.wheel_counter.get_distance_in_km(self._settings.wheel_cm.value)
        self.trip_duration_min = self.wheel_time.get_sum_in_min()

    def enable(self, val):
        self.is_started = val