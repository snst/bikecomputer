import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
from csc import CSC


class TestCSCMethods(unittest.TestCase):

    def test_uninit(self):
        csc = CSC()
        self.assertFalse(csc.init)
        self.assertFalse(csc.is_riding)

    def test_init(self):
        csc = CSC()
        val1 = struct.pack("<BIHHH", 0, 1322, 213, 771, 83)
        csc.on_notify(val1)
        self.assertTrue(csc.init)
        self.assertFalse(csc.is_riding)
        self.assertEqual(csc.wheel_counter, 1322)
        self.assertEqual(csc.wheel_event, 213)
        self.assertEqual(csc.crank_counter, 771)
        self.assertEqual(csc.crank_event, 83)

    def test_overflow(self):
        csc = CSC()
        diff = csc.diff_uint32(33,(0xFFFFFFFF-22))
        self.assertEqual(33+22, diff)

    def test_calc_kmh(self):
        csc = CSC()
        cnt = 12
        sec = 13
        kmh = cnt * csc.wheel_size_cm  / 1000 / (sec / 36)
        self.assertEqual(kmh, csc.calc_kmh(cnt, sec))

    def test_cadence(self):
        csc = CSC()
        self.assertEqual(332*60/5, csc.calc_cadence(332, 5))
        
    def test_average_cadence(self):
        csc = CSC()
        self.assertEqual(332*60/5, csc.calc_average_cadence(332, 5))
        self.assertEqual((332+22)*60/(5+85), csc.calc_average_cadence(22, 85))

    def test_kmh(self):
        csc = CSC()
        val = struct.pack("<BIHHH", 0, 1322, 2213, 771, 83)
        csc.on_notify(val)
        val = struct.pack("<BIHHH", 0, 1342, 6423, 1231, 323)
        csc.on_notify(val)
        delta_sec = (6423-2213) / 1024
        kmh = (1342-1322) * csc.wheel_size_cm * 3.6 / delta_sec / 100
        self.assertEqual((6423-2213)/1024, delta_sec)
        self.assertEqual(kmh, csc.speed_kmh)
        self.assertTrue(csc.is_riding)

if __name__ == '__main__':
    unittest.main()
