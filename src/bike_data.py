class BikeData:
    def __init__(self):
        self.reset()

    def reset(self):
        self.speed = 0
        self.speed_avg = 0
        self.speed_max = 0
        self.cadence = 0
        self.cadence_avg = 0
        self.trip_distance = 0
        self.trip_duration = 0

