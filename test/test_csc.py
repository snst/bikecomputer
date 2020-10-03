import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
import csc
import bike_data


class TestCSCMethods(unittest.TestCase):

    def setUp(self):
        self.data = bike_data.BikeData()
        self.csc = csc.CSC(self.data)

    def test_uninit(self):
        self.assertFalse(self.csc.init)
        self.assertFalse(self.csc.is_riding)

    def test_init(self):
        val1 = struct.pack("<BIHHH", 0, 1322, 213, 771, 83)
        self.csc.on_notify(val1)
        self.assertTrue(self.csc.init)
        self.assertFalse(self.csc.is_riding)
        self.assertEqual(self.csc.wheel_counter, 1322)
        self.assertEqual(self.csc.wheel_event, 213)
        self.assertEqual(self.csc.crank_counter, 771)
        self.assertEqual(self.csc.crank_event, 83)

    def test_overflow(self):
        diff = self.csc.diff_uint32(33,(0xFFFFFFFF-22))
        self.assertEqual(33+22, diff)

    def test_calc_kmh(self):
        cnt = 12
        sec = 13
        kmh = cnt * self.csc.wheel_size_cm  / 1000 / (sec / 36)
        self.assertEqual(kmh, self.csc.calc_kmh(cnt, sec))

    def test_cadence(self):
        self.assertEqual(332*60/5, self.csc.calc_cadence(332, 5))
        
    def test_average_cadence(self):
        self.assertEqual(332*60/5, self.csc.calc_average_cadence(332, 5))
        self.assertEqual((332+22)*60/(5+85), self.csc.calc_average_cadence(22, 85))

    def test_kmh(self):
        val = struct.pack("<BIHHH", 0, 1322, 2213, 771, 83)
        self.csc.on_notify(val)
        val = struct.pack("<BIHHH", 0, 1342, 6423, 1231, 323)
        self.csc.on_notify(val)
        delta_sec = (6423-2213) / 1024
        kmh = (1342-1322) * self.csc.wheel_size_cm * 3.6 / delta_sec / 100
        self.assertEqual((6423-2213)/1024, delta_sec)
        self.assertEqual(kmh, self.csc.speed_kmh)
        self.assertTrue(self.csc.is_riding)

if __name__ == '__main__':
    unittest.main()
