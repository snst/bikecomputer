
class Max:
    uint16 = 0xFFFF
    uint32 = 0xFFFFFFFF

class CscVal:
    def __init__(self, max): #ut
        self._last_val = 0
        self._max = max
        self.delta = 0

    def calc_delta(self, val): #ut
        if val >= self._last_val:
            self.delta = val - self._last_val
        else:
            self.delta = val + (self._max - self._last_val)
        self._last_val = val
 