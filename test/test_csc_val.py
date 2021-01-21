import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
from csc_val import *

class TestCscVal(unittest.TestCase):

    def test_unit16(self):
        max = Max.uint16
        s = 0
        v = CscVal(max)
        self.assertEqual(0, v.delta)

        s += 33
        v.calc_delta(s)
        self.assertEqual(33, v.delta)

        s += 0
        v.calc_delta(s)
        self.assertEqual(0, v.delta)

        s += 3673
        v.calc_delta(s)
        self.assertEqual(3673, v.delta)

        s += 214
        v.calc_delta(s)
        self.assertEqual(214, v.delta)

        s -= 10
        v.calc_delta(s)
        self.assertEqual(max-10, v.delta)

        s += 1
        v.calc_delta(s)
        self.assertEqual(1, v.delta)

        s -= 1
        v.calc_delta(s)
        self.assertEqual(max-1, v.delta)

    def test_unit32(self):
        max = Max.uint32
        s = 0
        v = CscVal(max)
        self.assertEqual(0, v.delta)

        s += 33
        v.calc_delta(s)
        self.assertEqual(33, v.delta)

        s += 0
        v.calc_delta(s)
        self.assertEqual(0, v.delta)

        s += 3673
        v.calc_delta(s)
        self.assertEqual(3673, v.delta)

        s += 214
        v.calc_delta(s)
        self.assertEqual(214, v.delta)

        s -= 10
        v.calc_delta(s)
        self.assertEqual(max-10, v.delta)

        s += 1
        v.calc_delta(s)
        self.assertEqual(1, v.delta)

        s -= 1
        v.calc_delta(s)
        self.assertEqual(max-1, v.delta)


    """
    def setUp(self):
        self._settings = DataSettings()
        self.data = TripData(1, self._settings)

    def test_not_init(self):
        self.assertFalse(self.data.init)
        self.assertFalse(self.data.is_riding)




    def test_calc_kmh(self):
        cnt = 12
        sec = 13
        tc = sec * 1024
        kmh = cnt * self._settings.wheel_cm.value  / 1000 / (sec / 36)
        self.assertEqual(kmh, self.data.calc_kmh_from_csc_val(cnt, tc))

    def test_cadence(self):
        self.assertEqual(332*60/5, self.data.calc_cadence(332, 5))
        """
        
#    def test_average_cadence(self):
 #       self.assertEqual(332*60/5, self.csc.calc_average_cadence(332, 5))
  #      self.assertEqual((332+22)*60/(5+85), self.csc.calc_average_cadence(22, 85))

    """def test_kmh(self):
        raw_data = struct.pack("<BIHHH", 0, 1322, 2213, 771, 83)
        self.csc.process(raw_data, self.data)
        raw_data = struct.pack("<BIHHH", 0, 1342, 6423, 1231, 323)
        self.csc.process(raw_data, self.data)
        delta_sec = (6423-2213) / 1024
        dist_km = (1342-1322) * self._settings.wheel_cm.value / 100000
        kmh =  dist_km * 3600 / delta_sec
        self.assertEqual(delta_sec/60, self.data.trip_duration_min)
        self.assertEqual(dist_km, self.data.trip_distance)
        self.assertEqual((int)(kmh*100), (int)(self.data.speed*100))
        self.assertTrue(self.data.is_riding)"""


    """def test_init(self):
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
        self.assertEqual(self.data.crank_time.sum, 0)"""


if __name__ == '__main__':
    unittest.main()
