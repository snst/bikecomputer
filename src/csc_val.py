
class Max:
    uint16 = 0xFFFF
    uint32 = 0xFFFFFFFF

class CscVal:
    def __init__(self, max):
        self.sum = 0
        self.last_val = 0
        self.delta = 0
        self.max = max
        pass

    def reset(self):
        self.sum = 0

    def calc_delta(self, val):
        if val >= self.last_val:
            self.delta = val - self.last_val
        else:
            self.delta = val + (self.max - self.last_val)
        self.last_val = val
 
    def add_delta(self):
        print("add %u" % (self.delta))
        self.sum += self.delta

    def get_sum_in_min(self):
        return self.sum / (1024 * 60)

    def get_distance_in_km(self, wheel_cm):
        return self.sum * wheel_cm / 100000

    def print(self, str):
        print("%s: sum=%u, last=%u, delta=%u" % (str, self.sum, self.last_val, self.delta))