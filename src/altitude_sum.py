class AltitudeSum:
    def __init__(self):
        self.reset()

    def reset(self):
        self.sum = 0
        self._last_val = None
        self.min = 9999
        self.max = 0000

    def process(self, val, delta):
        self.min = min(self.min, val)
        self.max = max(self.max, val)
        if self._last_val == None:
            self._last_val = val
        else:
            diff = val - self._last_val
            if diff > delta:
                self.sum += diff
            if abs(diff) > delta:
                self._last_val = val
        
