import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
site.addsitedir('./modules')  # Always appends to end
site.addsitedir('./emu')  # Always appends to end
from data_cache import *

class TestDataCache(unittest.TestCase):

    def setUp(self):
        self.c = DataCache()

    def test_reset(self):
        val = 7
        self.assertTrue(self.c.changed(DataCache.CADENCE,val))
        self.assertTrue(self.c.changed(DataCache.SPEED,val))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val))
        self.assertFalse(self.c.changed(DataCache.SPEED,val))
        self.c.reset_val(DataCache.CADENCE)
        self.assertTrue(self.c.changed(DataCache.CADENCE,val))
        self.assertFalse(self.c.changed(DataCache.SPEED,val))

    def test_reset_all(self):
        val = 7
        self.assertTrue(self.c.changed(DataCache.CADENCE,val))
        self.assertTrue(self.c.changed(DataCache.SPEED,val))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val))
        self.assertFalse(self.c.changed(DataCache.SPEED,val))
        self.c.reset()
        self.assertTrue(self.c.changed(DataCache.CADENCE,val))
        self.assertTrue(self.c.changed(DataCache.SPEED,val))

    def test_int(self):
        val = 7
        val2 = 8
        self.assertTrue(self.c.changed(DataCache.CADENCE,val))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val))
        self.assertTrue(self.c.changed(DataCache.CADENCE,val2))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val2))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val2))

    def test_float(self):
        val = 7.33
        val2 = 7.34
        self.assertTrue(self.c.changed(DataCache.CADENCE,val))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val))
        self.assertTrue(self.c.changed(DataCache.CADENCE,val2))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val2))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val2))

    def test_string(self):
        val = "aaa"
        val2 = "aab"
        self.assertTrue(self.c.changed(DataCache.CADENCE,val))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val))
        self.assertTrue(self.c.changed(DataCache.CADENCE,val2))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val2))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val2))

    def test_bool(self):
        val = True
        val2 = False
        self.assertTrue(self.c.changed(DataCache.CADENCE,val))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val))
        self.assertTrue(self.c.changed(DataCache.CADENCE,val2))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val2))
        self.assertFalse(self.c.changed(DataCache.CADENCE,val2))

if __name__ == '__main__':
    unittest.main()
