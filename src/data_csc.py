import csc_val

class DataCsc:
    def __init__(self, id):
        self.reset()
        self.id = id
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
        self.trip_duration = 0
        self.is_riding = False