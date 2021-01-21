import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
site.addsitedir('./modules')  # Always appends to end
site.addsitedir('./emu')  # Always appends to end
from smooth import *

class TestSmooth(unittest.TestCase):

    def setUp(self):
        self.s = Smooth()

    def test_1(self):
        self.assertEqual(5, self.s.add(5, 3))
        self.assertEqual((5+8)/2, self.s.add(8, 3))
        self.assertEqual((5+8+2)/3, self.s.add(2, 3))
        self.assertEqual((8+2+9)/3, self.s.add(9, 3))
        self.assertEqual((2+9+6)/3, self.s.add(6, 3))

if __name__ == '__main__':
    unittest.main()
