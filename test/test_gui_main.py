import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
site.addsitedir('./modules')  # Always appends to end
site.addsitedir('./emu')  # Always appends to end
from gui_main import *

class TestGuiMain(unittest.TestCase):

    def setUp(self):
        pass

    def test_a(self):
        self.assertEqual(0,0)

if __name__ == '__main__':
    unittest.main()
