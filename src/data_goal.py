from data_settings import SettingVal

class DataGoal:
    def __init__(self):
        self.target_time_min = SettingVal(60, 1, 500)
        self.target_dist_km = SettingVal(30, 1, 300, True)
        self.target_average_km_h = SettingVal(30, 10, 45, True)
        self.spent_time_ms = 0
        self.spent_distance_cm = 0
        self.remaining_distance_km = 0
        self.remaining_time_min = 0
        self.optimal_distance_km = 0
        self.calc_required_average_km_h = 0
        self.is_active = False

    def calculate_time(self, val, closed):
        if closed:
            self.target_time_min.value = 60 * self.target_dist_km.value / self.target_average_km_h.value

    def calculate_avg(self, val, closed):
        if closed:
            self.target_average_km_h.value = 60 * self.target_dist_km.value / self.target_time_min.value            

    def calculate_progress(self, data):
        if self.is_active:
            self.remaining_distance_km = max(0, self.target_dist_km.value - data.trip_distance)
            self.remaining_time_min = max(0, 60 * (self.target_dist_km.value - (self.target_average_km_h.value * data.trip_duration_min / 60)) / self.target_average_km_h.value)
            if self.remaining_time_min > 0 and self.remaining_distance_km > 0:
                self.calc_required_average_km_h = min(99.9, 60 * self.remaining_distance_km / self.remaining_time_min)
            else:
                self.calc_required_average_km_h = 0
            self.optimal_distance_km = self.target_average_km_h.value * data.trip_duration_min / 60
            pass
