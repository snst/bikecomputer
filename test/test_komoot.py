# This Python file uses the following encoding: utf-8
import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
site.addsitedir('./modules')  # Always appends to end
site.addsitedir('./emu')  # Always appends to end
from nav_gui import *

class TestKomoot(unittest.TestCase):

    def setUp(self):
        self.kg = NavGui(None)
        pass

    def test_1(self):
        str_in = "äkbcö12ü45ßdäö"
        str_exp = "akbco12u45ssdao"
        str_out = self.kg.replace_street_str(str_in)
        self.assertEqual(str_exp, str_out)

if __name__ == '__main__':
    unittest.main()
