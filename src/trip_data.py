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
        self.crank_counter = 0
        self.speed_avg = 0
        self.speed_max = 0
        self.cadence_avg = 0
        self.trip_distance = 0
        self.trip_duration_sum_ms = 0
        self.trip_duration_part_ms = 0
        self.trip_duration_start_ms = 0
        self.cadence_duration_sum_ms = 0
        self.cadence_duration_part_ms = 0
        self.cadence_duration_start_ms = 0
        self.sim = 10
        self.is_started = True
        self.altitude.reset()
        self.trip_paused = False
        self.cadence_paused = False

    def process(self, cd, ms):
        trip_paused = True
        cadence_paused = True

        if self.is_started:
            if cd.has_valid_cadence and self.cadence_duration_start_ms > 0:
                self.crank_counter += cd.crank_counter_delta
                self.cadence_duration_part_ms = ms - self.cadence_duration_start_ms
                cadence_paused = False

            if cd.is_riding and self.trip_duration_start_ms > 0:
                self.speed_max = max(self.speed_max, cd.speed)
                self.wheel_counter += cd.wheel_counter_delta
                self.trip_duration_part_ms = ms - self.trip_duration_start_ms
                trip_paused = False

        if trip_paused:
            if not self.trip_paused: # switch from not paused -> paused
                self.trip_duration_sum_ms += self.trip_duration_part_ms
                self.trip_duration_part_ms = 0
            self.trip_duration_start_ms = ms

        if cadence_paused:
            if not self.cadence_paused: # switch from not paused -> paused
                self.cadence_duration_sum_ms += self.cadence_duration_part_ms
                self.cadence_duration_part_ms = 0
            self.cadence_duration_start_ms = ms

        self.trip_paused = trip_paused
        self.cadence_paused = cadence_paused
        self.cadence_avg = cd.calc_cadence_from_ms(self.crank_counter, self.cadence_duration_ms)
        #print("cadence ms/tck %d %d" % (self.cadence_avg, self.cadence_avg_ticks))
        self.speed_avg = cd.calc_speed_kmh_from_ms(self.wheel_counter, self.trip_duration_ms)
        self.trip_distance = cd.convert_wheel_count_to_km(self.wheel_counter)

    def enable(self, val):
        self.is_started = val
        self.altitude.enable(val)

    @property
    def trip_duration_ms(self):
        return (self.trip_duration_sum_ms + self.trip_duration_part_ms)

    @property
    def trip_duration_sec(self):
        return self.trip_duration_ms / 1000

    @property
    def trip_duration_min(self):
        return self.trip_duration_ms / 60000

    @property
    def cadence_duration_ms(self):
        return (self.cadence_duration_sum_ms + self.cadence_duration_part_ms)
