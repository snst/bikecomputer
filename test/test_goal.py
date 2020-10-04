import unittest
import struct
import site
import sys
site.addsitedir('./src')  # Always appends to end
import goal_calc
from data_settings import *
from data_goal import *

class TestGoal(unittest.TestCase):

    def setUp(self):
        self.goal = DataGoal()
        self.gc = goal_calc.GoalCalc(self.goal)

    def test_1(self):
        self.goal.target_dist_km = SettingVal(60,0,0,True)
        self.goal.target_average_km_h = SettingVal(30,0,0,True)
        self.goal.spent_time_ms = 60*60*1000
        self.goal.spent_distance_cm = 30*1000*100
        self.gc.calc()
        self.assertEqual(30, self.goal.remaining_distance_km)
        self.assertEqual(60, self.goal.remaining_time_min)
        self.assertEqual(30, self.goal.calc_required_average_km_h)

    def test_2(self):
        self.goal.target_dist_km = SettingVal(60,0,0,True)
        self.goal.target_average_km_h = SettingVal(30,0,0,True)
        self.goal.spent_time_ms = 60*60*1000
        self.goal.spent_distance_cm = 15*1000*100
        self.gc.calc()
        self.assertEqual(45, self.goal.remaining_distance_km)
        self.assertEqual(60, self.goal.remaining_time_min)
        self.assertEqual(45, self.goal.calc_required_average_km_h)

    def test_3(self):
        self.goal.target_dist_km = SettingVal(60,0,0,True)
        self.goal.target_average_km_h = SettingVal(30,0,0,True)
        self.goal.spent_time_ms = 60*60*1000
        self.goal.spent_distance_cm = 45*1000*100
        self.gc.calc()
        self.assertEqual(15, self.goal.remaining_distance_km)
        self.assertEqual(60, self.goal.remaining_time_min)
        self.assertEqual(15, self.goal.calc_required_average_km_h)

    def test_3(self):
        self.goal.target_dist_km = SettingVal(60,0,0,True)
        self.goal.target_average_km_h = SettingVal(30,0,0,True)
        self.goal.spent_time_ms = 30*60*1000
        self.goal.spent_distance_cm = 30*1000*100
        self.gc.calc()
        self.assertEqual(30, self.goal.remaining_distance_km)
        self.assertEqual(90, self.goal.remaining_time_min)
        self.assertEqual(20, self.goal.calc_required_average_km_h)

if __name__ == '__main__':
    unittest.main()
