import unittest
import struct
import site
import sys
from time import sleep
site.addsitedir('./src')  # Always appends to end
import display_dim
import bike_settings

class TestDisplayDim(unittest.TestCase):

    def display_cb(self, is_on):
        if is_on:
            self.on_cnt +=1
        else:
            self.off_cnt += 1

    def setUp(self):
        self.on_cnt = 0
        self.off_cnt = 0
        self.settings = bike_settings.BikeSettings()
        self.settings.led_time.value = 1
        self.display = display_dim.DisplayDim(self.settings)
        self.display.set_callback(self.display_cb)


    def test_init(self):
        self.assertTrue(self.display.is_display_on())
        self.assertEqual(self.on_cnt, 0)
        self.assertEqual(self.off_cnt, 0)

    def test_turn_off(self):
        self.display.set_display_on()
        self.assertTrue(self.display.is_display_on())
        self.assertEqual(self.on_cnt, 1)
        self.assertEqual(self.off_cnt, 0)
        sleep(self.settings.led_time.value)
        self.assertEqual(self.off_cnt, 1)
        self.assertFalse(self.display.is_display_on())

    def test_retrigger_on(self):
        self.display.set_display_on()
        sleep(self.settings.led_time.value / 2)
        self.display.set_display_on()
        self.assertTrue(self.display.is_display_on())
        sleep(self.settings.led_time.value * 0.8)
        self.assertEqual(self.on_cnt, 2)
        self.assertEqual(self.off_cnt, 0)
        self.assertTrue(self.display.is_display_on())
        sleep(self.settings.led_time.value * 0.2)
        self.assertEqual(self.off_cnt, 1)
        self.assertFalse(self.display.is_display_on())


if __name__ == '__main__':
    unittest.main()
