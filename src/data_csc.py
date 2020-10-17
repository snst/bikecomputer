import csc_val

class DataCsc:
    def __init__(self, id):
        self.reset()
        self.id = id
        self.goal = None
        pass

    def reset(self):
        self.init = False
        self.wheel_counter = csc_val.CscVal(csc_val.Max.uint32)
        self.wheel_time = csc_val.CscVal(csc_val.Max.uint16)
        self.crank_counter = csc_val.CscVal(csc_val.Max.uint16)
        self.crank_time = csc_val.CscVal(csc_val.Max.uint16)
        self.speed = 0
        self.speed_avg = 0
        self.speed_max = 0
        self.cadence = 0
        self.cadence_avg = 0
        self.trip_distance = 0
        self.trip_duration_min = 0
        self.is_riding = False

    def add_goal(self, goal):
        self.goal = goal

    def invalidate_shown_data(self):
        self.wheel_counter = None
        self.wheel_time = None
        self.crank_counter = None
        self.crank_time = None
        self.speed = None
        self.speed_avg = None
        self.speed_max = None
        self.cadence = None
        self.cadence_avg = None
        self.trip_distance = None
        self.trip_duration_min = None
        self.is_riding = None
