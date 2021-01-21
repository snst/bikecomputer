import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
site.addsitedir('./modules')  # Always appends to end
site.addsitedir('./emu')  # Always appends to end
from altitude_sum import *

class TestAltitudeSum(unittest.TestCase):

    def setUp(self):
        self.s = AltitudeSum()

    def test_init(self):
        self.assertEqual(0, self.s.sum)
        self.assertEqual(0, self.s.min)
        self.assertEqual(0, self.s.max)

    def test_riding(self):
        self.s.process(300, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(300, self.s.min)
        self.assertEqual(300, self.s.max)

        self.s.process(300, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(300, self.s.min)
        self.assertEqual(300, self.s.max)

        self.s.process(302, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(300, self.s.min)
        self.assertEqual(302, self.s.max)

        self.s.process(304, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(300, self.s.min)
        self.assertEqual(304, self.s.max)

        self.s.process(290, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(290, self.s.min)
        self.assertEqual(304, self.s.max)

        self.s.process(294, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(290, self.s.min)
        self.assertEqual(304, self.s.max)

        self.s.process(295, 5, True)
        self.assertEqual(5, self.s.sum)
        self.assertEqual(290, self.s.min)
        self.assertEqual(304, self.s.max)

        self.s.process(311, 5, True)
        self.assertEqual(21, self.s.sum)
        self.assertEqual(290, self.s.min)
        self.assertEqual(311, self.s.max)

        self.s.reset()
        self.assertEqual(0, self.s.sum)
        self.assertEqual(0, self.s.min)
        self.assertEqual(0, self.s.max)


    def test_not_riding(self):
        self.s.process(300, 5, False)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(0, self.s.min)
        self.assertEqual(0, self.s.max)

        self.s.process(310, 5, True)
        self.assertEqual(10, self.s.sum)
        self.assertEqual(310, self.s.min)
        self.assertEqual(310, self.s.max)

        self.s.process(320, 5, False)
        self.assertEqual(10, self.s.sum)
        self.assertEqual(310, self.s.min)
        self.assertEqual(310, self.s.max)

        self.s.process(324, 5, True)
        self.assertEqual(10, self.s.sum)
        self.assertEqual(310, self.s.min)
        self.assertEqual(324, self.s.max)

        self.s.process(325, 5, True)
        self.assertEqual(15, self.s.sum)
        self.assertEqual(310, self.s.min)
        self.assertEqual(325, self.s.max)


    def test_not_enabled(self):
        self.s.enable(False)
        self.s.process(300, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(0, self.s.min)
        self.assertEqual(0, self.s.max)

        self.s.process(310, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(0, self.s.min)
        self.assertEqual(0, self.s.max)

        self.s.enable(True)
        self.s.process(310, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(310, self.s.min)
        self.assertEqual(310, self.s.max)

        self.s.process(314, 5, True)
        self.assertEqual(0, self.s.sum)
        self.assertEqual(310, self.s.min)
        self.assertEqual(314, self.s.max)

        self.s.process(315, 5, True)
        self.assertEqual(5, self.s.sum)
        self.assertEqual(310, self.s.min)
        self.assertEqual(315, self.s.max)


if __name__ == '__main__':
    unittest.main()
