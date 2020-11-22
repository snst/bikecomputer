
class Altimeter_emu:
    def __init__(self):

        self._temp = [22.0, 23.0]
        self._pressure = [997.0, 998.0]
        self._altitude = [312.0, 313.0]
        self._i = 0

    def update(self):
        self._i = (self._i + 1) % len(self._temp)
 
   
    @property
    def temperature(self):
        return self._temp[self._i]

    @property
    def altitude(self):
        return self._pressure[self._i]

    @property
    def pressure(self):
        return self._altitude[self._i]

