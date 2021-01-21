class AltitudeSum:
    def __init__(self): #ut
        self.reset()
        self._enabled = True

    def reset(self): #ut
        self.sum = 0
        self._last_val = None
        self.min = 0
        self.max = 0

    def process(self, val, delta, is_riding): #ut
        is_enabled = self._enabled and is_riding
        if self._last_val == None or not is_enabled:
            self._last_val = val
        else:
            diff = val - self._last_val
            if diff >= delta:
                self.sum += diff
            if abs(diff) >= delta:
                self._last_val = val

        if is_enabled:
            self.min = val if self.min == 0 else min(self.min, val)
            self.max = max(self.max, val)
        
    def enable(self, enabled): #ut
        self._enabled = enabled