import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
site.addsitedir('./modules')  # Always appends to end
site.addsitedir('./emu')  # Always appends to end
from trip_data import *
from data_settings import *
from cycle_data import *

class TestDataStore(unittest.TestCase):

    def setUp(self):
        self.settings = DataSettings()
        self.t = TripData(1)
        self.cd = CycleData(self.settings)
        self.t.is_started = True
        self.cd.is_riding = True
        self.cd.has_valid_cadence = True
        self.cd.crank_counter.delta = 3
        self.cd.crank_time.delta = 2048
        self.cd.wheel_counter.delta = 2
        self.cd.wheel_time.delta = 1024
        self.cd.speed = 3
        self.t.process(self.cd)
        self.cd.crank_counter.delta = 4
        self.cd.crank_time.delta = 1024
        self.cd.wheel_counter.delta = 7
        self.cd.wheel_time.delta = 4096
        self.cd.speed = 5
        pass

    def test_started(self):
        self.t.process(self.cd)
        self.assertEqual(60*7/3,self.t.cadence_avg)
        self.assertEqual(self.cd.calc_speed_kmh(9, 5*1024),self.t.speed_avg)
        self.assertEqual(self.cd.convert_wheel_count_to_km(9),self.t.trip_distance)
        self.assertEqual(self.cd.convert_wheel_ticks_to_min(5*1024),self.t.trip_duration_min)
        self.assertEqual(5, self.t.speed_max)

        self.cd.speed = 8
        self.t.process(self.cd)
        self.assertEqual(60*11/4,self.t.cadence_avg)
        self.assertEqual(self.cd.calc_speed_kmh(16, 9*1024),self.t.speed_avg)
        self.assertEqual(self.cd.convert_wheel_count_to_km(16),self.t.trip_distance)
        self.assertEqual(self.cd.convert_wheel_ticks_to_min(9*1024),self.t.trip_duration_min)
        self.assertEqual(8, self.t.speed_max)

    def test_invalid_cadence(self):
        self.cd.has_valid_cadence = False
        self.t.process(self.cd)
        self.assertEqual(60*3/2,self.t.cadence_avg)

    def test_not_riding(self):
        self.cd.is_riding = False
        self.t.process(self.cd)
        self.assertEqual(3, self.t.speed_max)
        self.assertEqual(self.cd.calc_speed_kmh(2, 1*1024),self.t.speed_avg)
        self.assertEqual(self.cd.convert_wheel_count_to_km(2),self.t.trip_distance)
        self.assertEqual(self.cd.convert_wheel_ticks_to_min(1*1024),self.t.trip_duration_min)

    def test_not_started(self):
        self.t.enable(False)
        self.t.process(self.cd)
        self.assertEqual(3, self.t.speed_max)
        self.assertEqual(60*3/2,self.t.cadence_avg)


if __name__ == '__main__':
    unittest.main()
