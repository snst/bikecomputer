import data_global as g
from kalman import *

class AltSum:
    def __init__(self, avg):
        self.sum = 0
        self.alt = None
        self._avg = avg

    def update(self, val):
        new_alt = self._avg.update(val)
        self.add(new_alt)

    def add(self, new_alt):
        if self.alt != None and new_alt > self.alt:
            self.sum += (new_alt - self.alt)
        self.alt = new_alt

class Avg:
    def __init__(self, max):
        self._values = []
        self._max = max
        self.value = 0

    def update(self, val):
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
        self.alt_avg = AltSum(Avg(5))
        self.alt_kalman = AltSum(Kalman(0.092, 1, 1.129))

    def update(self):
        #print('Temperature: {} degrees C'.format(self._sensor.temperature)) 
        #print('Pressure: {}hPa'.format(self._sensor.pressure))
        #print('Altitude: {} meters'.format(self._sensor.altitude))

        if g.altimeter:
            g.altimeter.update()
            self._temperature = g.altimeter.temperature
            self._pressure = g.altimeter.pressure
            self._altitude = g.altimeter.altitude
            self.alt_avg.update(self._altitude)
            self.alt_kalman.update(self._altitude)
            #print("%.2f %.2f , %.2f %.2f" % (self.alt_avg.alt, self.alt_kalman.alt, self.alt_avg.sum, self.alt_kalman.sum))
            #print("Temp=%.2f°C, Pressure=%.2fhPa, Alt=%.2fm" % (self._temperature, self._pressure, self._altitude))
            print("%f," % (self._altitude))

    def reset_alt(self):
        self.alt_avg.sum = 0
        self.alt_kalman.sum = 0

    @property
    def temperature(self):
        return self._temperature

    @property
    def altitude(self):
        return self._altitude

    @property
    def altitude_min(self):
        return 323.3

    @property
    def altitude_max(self):
        return 2823.3


    #@property
    #def altitude_avg(self):
    #    return self._altitude_avg

    #@property
    #def altitude_avg_k(self):
    #    return self._altitude_avg_k

    @property
    def pressure(self):
        return self._pressure

    #@property
    #def sum(self):
    #    return self._alt_sum

    #@property
    #def sum_k(self):
    #    return self._alt_sum_k
