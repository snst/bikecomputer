class Smooth:
    def __init__(self):
        self._values = []
        
    #ut
    def add(self, val, n): 
        self._values.append(val)
        while len(self._values) > n:
            self._values.pop(0)
        sum = 0
        for val in self._values:
            sum += val
        sum = sum / len(self._values)
        return sum


class SmoothPair:
    def __init__(self):
        self._values = []

    def add(self, a, b, n):
        sum_a = 0
        sum_b = 0
        self._values.append((a, b))
        while len(self._values) > n:
            self._values.pop(0)
        for val in self._values:
            sum_a += val[0]
            sum_b += val[1]
        l = len(self._values)
        return (sum_a/l, sum_b/l)
