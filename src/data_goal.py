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
        self.calc_required_average_km_h = 0
        pass

