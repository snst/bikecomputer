from data_settings import SettingVal
from data_store import *

filename = "goal.cfg"


class DataGoal(DataStore):
    def __init__(self):
        self.target_time_min = SettingVal(60, 1, 500)
        self.target_dist_km = SettingVal(30, 1, 300, True)
        self.target_average_km_h = SettingVal(30, 10, 45, True)
        self.remaining_distance_km = 0
        self.remaining_time_min = 0
        self.optimal_distance_km = 0
        self.calc_required_average_km_h = 0
        self.is_started = False
        self.has_distance_reached = False

    def calculate_time(self, val, closed):
        if closed:
            self.target_time_min.value = 60 * self.target_dist_km.value / self.target_average_km_h.value

    def calculate_avg(self, val, closed):
        if closed:
            self.target_average_km_h.value = 60 * self.target_dist_km.value / self.target_time_min.value     

    def calculate_progress(self, data):
        if self.is_started:
            self.remaining_distance_km = max(0, self.target_dist_km.value - data.trip_distance)
            self.remaining_time_min = max(0, 60 * (self.target_dist_km.value - (self.target_average_km_h.value * data.trip_duration_min / 60)) / self.target_average_km_h.value)
            if self.remaining_distance_km > 0: 
                if self.remaining_time_min > 0:
                    self.calc_required_average_km_h = min(99.9, 60 * self.remaining_distance_km / self.remaining_time_min)
                else: 
                    self.calc_required_average_km_h = 99.9
                self.has_distance_reached = False
            else:
                if not self.has_distance_reached:
                    self.has_distance_reached = True
                    self.calc_required_average_km_h = data.speed_avg

            self.optimal_distance_km = self.target_average_km_h.value * data.trip_duration_min / 60
            pass

    def is_behind(self, data):
        return data.trip_distance < self.optimal_distance_km


    def get_all_attributes(self):
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def save(self):
        DataStore.save(self, filename)

    def load(self):
        DataStore.load(self, filename)