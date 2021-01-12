class Smooth:
    def __init__(self):
        self._values = []
        
    def add(self, val, n):
        self._values.append(val)
        while len(self._values) > n:
            self._values.pop(0)
        sum = 0
        for val in self._values:
            sum += val
        sum = sum / len(self._values)
        return sum
