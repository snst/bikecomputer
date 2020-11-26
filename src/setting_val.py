
class SettingVal:
    def __init__(self, value, min, max, is_float = False, step = 1):
        self.value = value
        self.min = min
        self.max = max
        self.step = step
        self.is_float = is_float
