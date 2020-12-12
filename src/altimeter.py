import data_global as g

class AltSum:
    def __init__(self):
        self.reset()

    def reset(self):
        self._sum = 0
        self._last_val = None

    def add(self, val, delta):
        if self._last_val == None:
            self._last_val = val
        else:
            diff = val - self._last_val
            if diff > delta:
                self._sum += diff
            if abs(diff) > delta:
                self._last_val = val
        
    @property
    def value(self):
        return self._sum
    
    def show(self):
        print("Alt %f" % (self._sum))


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
        self.alt_avg = CalcAvg()
        self.alt_sum = AltSum()
        self._alt_avg = 0
        self.reset_alt()

    def update(self):
        #print('Temperature: {} degrees C'.format(self._sensor.temperature)) 
        #print('Pressure: {}hPa'.format(self._sensor.pressure))
        #print('Altitude: {} meters'.format(self._sensor.altitude))

        if g.altimeter:
            g.altimeter.update()
            self._temperature = g.altimeter.temperature
            self._pressure = g.altimeter.pressure
            self._altitude = g.altimeter.altitude
            self._alt_avg = self.alt_avg.add(self._altitude, g.bc._settings.altimeter_values.value)
            self.alt_sum.add(self._alt_avg, g.bc._settings.altimeter_step.value/100)
            self._alt_min = min(self._alt_min, self._alt_avg)
            self._alt_max = max(self._alt_max, self._alt_avg)
            #print("%.2f %.2f , %.2f %.2f" % (self.alt_avg.alt, self.alt_kalman.alt, self.alt_avg.sum, self.alt_kalman.sum))
            #print("Temp=%.2f°C, Pressure=%.2fhPa, Alt=%.2fm" % (self._temperature, self._pressure, self._altitude))
            #print("%f," % (self._altitude))

    def reset_alt(self):
        self.alt_sum.reset()
        self._alt_min = 5000
        self._alt_max = 0

    @property
    def temperature(self):
        return self._temperature

    @property
    def altitude(self):
        return self._alt_avg

    @property
    def altitude_min(self):
        return self._alt_min

    @property
    def altitude_max(self):
        return self._alt_max

    @property
    def altitude_sum(self):
        return self.alt_sum.value

    @property
    def pressure(self):
        return self._pressure
