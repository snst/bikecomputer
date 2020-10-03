
class SettingVal:
    def __init__(self, value, min, max, is_float = False):
        self.value = value
        self.min = min
        self.max = max
        self.is_float = is_float


class DataCsc:
    def __init__(self):
        self.reset()
        pass

    def reset(self):
        self.speed = 0
        self.speed_avg = 0
        self.speed_max = 0
        self.cadence = 0
        self.cadence_avg = 0
        self.trip_distance = 0
        self.trip_duration = 0
        self.is_riding = False

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

class DataSetting:
    def __init__(self):
        self.led_time = SettingVal(0, 0, 15)
        self.led_on = SettingVal(7, 0, 10)
        self.led_off = SettingVal(3, 0, 10)
        self.touch_ignore = SettingVal(0, 0, 1)
        self.wheel_cm = SettingVal(214, 200, 230, True)
        pass

class BikeData:
    def __init__(self):
        self.csc = DataCsc()
        self.goal = DataGoal()
        self.settings = DataSetting()

