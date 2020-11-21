import data_global as g

class Altimeter:
    def __init__(self):
        self._temperature = 0
        self._pressure = 0
        self._altitude = 0

    def update(self):
        #print('Temperature: {} degrees C'.format(self._sensor.temperature)) 
        #print('Pressure: {}hPa'.format(self._sensor.pressure))
        #print('Altitude: {} meters'.format(self._sensor.altitude))

        if g.altimeter:
            self._temperature = g.altimeter.temperature
            self._pressure = g.altimeter.pressure
            self._altitude = g.altimeter.altitude

        #print("Temp=%.2f°C, Pressure=%.2fhPa, Alt=%.2fm" % (self._temperature, self._pressure, self._altitude))

    @property
    def temperature(self):
        return self._temperature

    @property
    def altitude(self):
        return self._altitude

    @property
    def pressure(self):
        return self._pressure
