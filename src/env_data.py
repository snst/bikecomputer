import data_global as g
from smooth import *

class EnvData:
    def __init__(self):
        self.sensor_bat_percent = 0
        self.computer_bat_volt = 0
        self.temperature = 0
        self.pressure = 0
        self.altitude = 0
        self._alt_filter = Smooth()

    def on_sensor_bat(self, data):
        self.sensor_bat_percent = data[0]

    def update_altitude(self):
        #print('Temperature: {} degrees C'.format(self._sensor.temperature)) 
        #print('Pressure: {}hPa'.format(self._sensor.pressure))
        #print('Altitude: {} meters'.format(self._sensor.altitude))

        if g.altimeter:
            g.altimeter.update()
            self.temperature = g.altimeter.temperature
            self.pressure = g.altimeter.pressure
            self.altitude = self._alt_filter.add(g.altimeter.altitude, g.bc._settings.altimeter_values.value)
