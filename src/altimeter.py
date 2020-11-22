import data_global as g

class Avg:
    def __init__(self, max):
        self._values = []
        self._max = max
        self.value = 0

    def add(self, val):
        self._values.append(val)
        if len(self._values) > self._max:
            self._values.pop(0)
        sum = 0    
        for v in self._values:
            sum += v
        self.value = sum / len(self._values)
        return self.value
    
    @property
    def is_ready(self):
        return len(self._values) == self._max

class Altimeter:
    def __init__(self):
        self._temperature = 0
        self._pressure = 0
        self._altitude = 0
        self._altitude_avg = 0
        self._avg = Avg(5)
        self._alt_sum = 0
        self._alt_last = None

    def update(self):
        #print('Temperature: {} degrees C'.format(self._sensor.temperature)) 
        #print('Pressure: {}hPa'.format(self._sensor.pressure))
        #print('Altitude: {} meters'.format(self._sensor.altitude))

        if g.altimeter:
            g.altimeter.update()
            self._temperature = g.altimeter.temperature
            self._pressure = g.altimeter.pressure
            self._altitude = g.altimeter.altitude
            self._altitude_avg = self._avg.add(self._altitude)

            if self._avg.is_ready:
                if self._alt_last == None:
                    self._alt_last = self._altitude_avg
                else:
                    delta = self._altitude_avg - self._alt_last
                    if delta > 0:
                        self._alt_sum += delta
                    self._alt_last = self._altitude_avg

        #print("Temp=%.2f°C, Pressure=%.2fhPa, Alt=%.2fm" % (self._temperature, self._pressure, self._altitude))

    @property
    def temperature(self):
        return self._temperature

    @property
    def altitude(self):
        return self._altitude

    @property
    def altitude_avg(self):
        return self._altitude_avg

    @property
    def pressure(self):
        return self._pressure

    @property
    def sum(self):
        return self._alt_sum
