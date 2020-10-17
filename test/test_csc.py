import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
from csc import *
from data_settings import *
from data_csc import *

class TestCSCMethods(unittest.TestCase):

    def setUp(self):
        self.data = DataCsc()
        self.settings = DataSettings()
        self.csc = CSC(self.settings)

    def test_uninit(self):
        self.assertFalse(self.data.init)
        self.assertFalse(self.data.is_riding)

    def test_init(self):
        raw_data = struct.pack("<BIHHH", 0, 1322, 213, 771, 83)
        self.csc.process(raw_data, self.data)
        self.assertTrue(self.data.init)
        self.assertFalse(self.data.is_riding)
        self.assertEqual(self.data.wheel_counter.last_val, 1322)
        self.assertEqual(self.data.wheel_time.last_val, 213)
        self.assertEqual(self.data.crank_counter.last_val, 771)
        self.assertEqual(self.data.crank_time.last_val, 83)
        self.assertEqual(self.data.wheel_counter.sum, 0)
        self.assertEqual(self.data.wheel_time.sum, 0)
        self.assertEqual(self.data.crank_counter.sum, 0)
        self.assertEqual(self.data.crank_time.sum, 0)

    def test_overflow_unit16(self):
        self.data.wheel_time.sum = 0xFFFF1234
        self.data.wheel_time.last_val = 0xFFFF - 22
        self.data.wheel_time.calc_delta(33)
        self.data.wheel_time.add_delta()
        self.assertEqual(33+22, self.data.wheel_time.delta)
        self.assertEqual(0xFFFF1234+33+22, self.data.wheel_time.sum)

    def test_overflow_unit32(self):
        self.data.wheel_counter.sum = 0xFFFA1234
        self.data.wheel_counter.last_val = 0xFFFFFFFF - 2232
        self.data.wheel_counter.calc_delta(3233)
        self.data.wheel_counter.add_delta()
        self.assertEqual(3233+2232, self.data.wheel_counter.delta)
        self.assertEqual(0xFFFA1234+3233+2232, self.data.wheel_counter.sum)


    def test_calc_kmh(self):
        cnt = 12
        sec = 13
        kmh = cnt * self.settings.wheel_cm.value  / 1000 / (sec / 36)
        self.assertEqual(kmh, self.csc.calc_kmh(cnt, sec))

    def test_cadence(self):
        self.assertEqual(332*60/5, self.csc.calc_cadence(332, 5))
        
#    def test_average_cadence(self):
 #       self.assertEqual(332*60/5, self.csc.calc_average_cadence(332, 5))
  #      self.assertEqual((332+22)*60/(5+85), self.csc.calc_average_cadence(22, 85))

    def test_kmh(self):
        raw_data = struct.pack("<BIHHH", 0, 1322, 2213, 771, 83)
        self.csc.process(raw_data, self.data)
        raw_data = struct.pack("<BIHHH", 0, 1342, 6423, 1231, 323)
        self.csc.process(raw_data, self.data)
        delta_sec = (6423-2213) / 1024
        dist_km = (1342-1322) * self.settings.wheel_cm.value / 100000
        kmh =  dist_km * 3600 / delta_sec
        self.assertEqual(delta_sec/60, self.data.trip_duration_min)
        self.assertEqual(dist_km, self.data.trip_distance)
        self.assertEqual((int)(kmh*100), (int)(self.data.speed*100))
        self.assertTrue(self.data.is_riding)

if __name__ == '__main__':
    unittest.main()
