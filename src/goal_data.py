from data_settings import SettingVal
from data_store import *
from trip_data import *
from const import *

filename = b'goal.cfg'


class GoalData(DataStore, TripData):
    def __init__(self, settings):
        TripData.__init__(self, 0)
        self.target_time_min = SettingVal(60, 1, 500)
        self.target_dist_km = SettingVal(30, 1, 300, True)
        self.target_average_km_h = SettingVal(30, 10, 45, True)
        self.remaining_distance_km = 0
        self.remaining_time_sec = 0
        self.optimal_distance_km = 0
        self.calc_required_average_km_h = 0
        self.is_finished = False
        self.is_started = False

    def calculate_time(self, val, closed):
        if closed:
            self.target_time_min.value = 60 * self.target_dist_km.value / self.target_average_km_h.value

    def calculate_avg(self, val, closed):
        if closed:
            self.target_average_km_h.value = 60 * self.target_dist_km.value / self.target_time_min.value     

    def calculate_progress(self):
        if self.is_started:
            self.remaining_distance_km = max(0, self.target_dist_km.value - self.trip_distance)
            self.remaining_time_sec = max(0, 3600 * (self.target_dist_km.value - (self.target_average_km_h.value * self.trip_duration_sec / 3600)) / self.target_average_km_h.value)
            if self.remaining_distance_km > 0: 
                if self.remaining_time_sec > 0:
                    self.calc_required_average_km_h = min(Limits.goal_max_required_speed, 3600 * self.remaining_distance_km / self.remaining_time_sec)
                else: 
                    self.calc_required_average_km_h = Limits.goal_max_required_speed
                self.is_finished = False
            else:
                if not self.is_finished:
                    self.is_finished = True
                    self.calc_required_average_km_h = self.speed_avg
                    self.is_started = False

            self.optimal_distance_km = self.target_average_km_h.value * self.trip_duration_sec / 3600
            pass

    @property
    def is_behind(self): #ut
        return self.trip_distance < self.optimal_distance_km

    def get_all_attributes(self):
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def save(self):
        DataStore.save(self, filename)

    def load(self):
        DataStore.load(self, filename)

    def process_data(self, cd):
        TripData.process_data(self, cd)
        self.calculate_progress()

    def enable(self, enabled):
        TripData.enable(self, enabled)
        if enabled:
            self.calculate_progress()
