import struct
from csc_val import *
from altitude_sum import *


class TripData:
    def __init__(self, id):
        self.id = id
        self.altitude = AltitudeSum()
        self.reset()

    def reset(self):
        self.wheel_counter = 0
        self.wheel_time = 0
        self.crank_counter = 0
        self.crank_time = 0
        self.speed_avg = 0
        self.speed_max = 0
        self.cadence_avg = 0
        self.trip_distance = 0
        self.trip_duration_min = 0
        self.sim = 10
        self.is_started = True
        self.altitude.reset()

    def process(self, cd):
        if self.is_started:
            if cd.has_valid_cadence:
                self.crank_counter += cd.crank_counter_delta
                self.crank_time += cd.crank_time_delta

            if cd.is_riding:
                self.speed_max = max(self.speed_max, cd.speed)
                self.wheel_counter += cd.wheel_counter_delta
                self.wheel_time += cd.wheel_time_delta

            self.cadence_avg = cd.calc_cadence(self.crank_counter, self.crank_time)
            self.speed_avg = cd.calc_speed_kmh(self.wheel_counter, self.wheel_time)
            self.trip_distance = cd.convert_wheel_count_to_km(self.wheel_counter)
            self.trip_duration_min = cd.convert_wheel_ticks_to_min(self.wheel_time)

    def enable(self, val):
        self.is_started = val
        self.altitude.enable(val)
