import data_global as g


class CalcAvg:
    def __init__(self, n=10):
        self._values = []
        self._avg = 0
    
    def add(self, val, n):
        self._values.append(val)
        while len(self._values) > n:
            self._values.pop(0)
        sum = 0
        for v in self._values:
            sum += v
        self._avg = sum / len(self._values)
        #print("avg %f" % (self._avg))
        return self._avg
    
    @property
    def count(self):
        return len(self._values)

    @property
    def value(self):
        return self._avg


class Altimeter:
    def __init__(self):
        self._temperature = 0
        self._pressure = 0
        self._altitude = 0
        self.filter = CalcAvg()
        self._alt_avg = 0

    def update(self):
        #print('Temperature: {} degrees C'.format(self._sensor.temperature)) 
        #print('Pressure: {}hPa'.format(self._sensor.pressure))
        #print('Altitude: {} meters'.format(self._sensor.altitude))

        if g.altimeter:
            g.altimeter.update()
            self._temperature = g.altimeter.temperature
            self._pressure = g.altimeter.pressure
            self._altitude = g.altimeter.altitude
            self._alt_avg = self.filter.add(self._altitude, g.bc._settings.altimeter_values.value)

    @property
    def temperature(self):
        return self._temperature

    @property
    def altitude(self):
        return self._alt_avg

    @property
    def pressure(self):
        return self._pressure
