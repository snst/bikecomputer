import random

class Altimeter_emu:
    def __init__(self):

        self._temp = 22
        self._pressure = 1000
        self._altitude = 300

    def update(self):
        self._altitude += random.uniform(-0.05, 0.5)
        self._temp += random.uniform(-0.5, 0.5)
        self._pressure += random.uniform(-1, 1)
    
    @property
    def temperature(self):
        return self._temp

    @property
    def altitude(self):
        return self._altitude

    @property
    def pressure(self):
        return self._pressure

