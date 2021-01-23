import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
site.addsitedir('./modules')  # Always appends to end
site.addsitedir('./emu')  # Always appends to end
from goal_data import *
from data_settings import *

class TestGoalData(unittest.TestCase):

    def setUp(self):
        self.settings = DataSettings()
        self.g = GoalData(self.settings)
        self.g.is_started = True

    def test_behind_goal(self):
        self.g.trip_distance = 10
        self.g.optimal_distance_km = 10
        self.assertFalse(self.g.is_behind)
        self.g.optimal_distance_km = 11
        self.assertTrue(self.g.is_behind)

    def test_not_finished(self):
        self.g.target_dist_km.value = 60
        self.g.trip_distance = 40
        self.g.calculate_progress()
        self.assertEqual(20, self.g.remaining_distance_km)
        self.assertFalse(self.g.is_finished)
        self.assertTrue(self.g.is_started)

    def test_finished(self):
        self.g.target_dist_km.value = 60
        self.g.trip_distance = 61
        self.g.calculate_progress()
        self.assertEqual(0, self.g.remaining_distance_km)
        self.assertTrue(self.g.is_finished)
        self.assertFalse(self.g.is_started)

if __name__ == '__main__':
    unittest.main()
