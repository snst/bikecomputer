import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
site.addsitedir('./modules')  # Always appends to end
site.addsitedir('./emu')  # Always appends to end
from cycle_data import *
from data_settings import *


class TestCycleData(unittest.TestCase):

    def setUp(self):
        self.settings = DataSettings()
        self.t = CycleData(self.settings)

    def test_convert_wheel_ticks_to_min(self):
        self.assertEqual(728324 / 1024 / 60, self.t.convert_wheel_ticks_to_min(728324))

    def test_convert_wheel_count_to_km(self):
        self.assertEqual(728324 * self.settings.wheel_cm.value / 100000, self.t.convert_wheel_count_to_km(728324))

    def test_calc_speed_kmh(self):
        self.assertEqual(37344 * self.settings.wheel_cm.value * 36 * 1024 / ( 329 * 1000), self.t.calc_speed_kmh(37344, 329))
        self.assertEqual(0, self.t.calc_speed_kmh(37344, 0))

    def test_calc_cadence(self):
        # 6 in 3 sec = 2 * 60 = 120
        self.assertEqual(120, self.t.calc_cadence(6, 3072))
        self.assertEqual(0, self.t.calc_cadence(6, 0))

    def test_has_valid_cadence(self):
        self.assertTrue(self.t.calc_has_valid_cadence(self.settings.min_cadence.value))
        self.assertFalse(self.t.calc_has_valid_cadence(self.settings.min_cadence.value-1))
        self.assertTrue(self.t.calc_has_valid_cadence(Limits.max_valid_cadence))
        self.assertFalse(self.t.calc_has_valid_cadence(Limits.max_valid_cadence+1))

    def test_is_riding(self):
        self.assertTrue(self.t.calc_is_riding(self.settings.min_speed.value))
        self.assertFalse(self.t.calc_is_riding(self.settings.min_speed.value-1))
        self.assertTrue(self.t.calc_is_riding(Limits.max_valid_speed))
        self.assertFalse(self.t.calc_is_riding(Limits.max_valid_speed+1))


    def test_smooth_speed(self):
        self.assertEqual(7.3, self.t.smooth_speed(7.34))
        self.assertEqual(8, self.t.smooth_speed(8.64))

    def test_smooth_cadence(self):
        self.assertEqual(6, self.t.smooth_cadence(6.34))
        self.assertEqual(7, self.t.smooth_cadence(8.5))

    def test_calculate(self):
        self.t.calculate(2, 1024, 1, 1024)
        self.assertTrue(self.t.has_valid_cadence)
        self.assertTrue(self.t.is_riding)

        self.t.calculate(30, 1024, 10, 1024)
        self.assertEqual(self.t.cadence <= Limits.max_valid_cadence, self.t.has_valid_cadence)
        self.assertEqual(self.t.speed <= Limits.max_valid_speed, self.t.is_riding)


if __name__ == '__main__':
    unittest.main()
