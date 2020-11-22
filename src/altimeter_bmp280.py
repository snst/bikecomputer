import adafruit_bmp280 

class Altimeter_bmp280:
    def __init__(self, i2c):
        self._sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        self._sensor.sea_level_pressure = 1013.25
        self._sensor.mode = adafruit_bmp280.MODE_NORMAL
        self._sensor.standby_period = adafruit_bmp280.STANDBY_TC_500
        self._sensor.iir_filter = adafruit_bmp280.IIR_FILTER_X16
        self._sensor.overscan_pressure = adafruit_bmp280.OVERSCAN_X16
        self._sensor.overscan_temperature = adafruit_bmp280.OVERSCAN_X2
        # The sensor will need a moment to gather inital readings

    

    def update(self):
        #print('Temperature: {} degrees C'.format(self._sensor.temperature)) 
        #print('Pressure: {}hPa'.format(self._sensor.pressure))
        #print('Altitude: {} meters'.format(self._sensor.altitude))

        #print("Temp=%f°C, Pressure=%fhPa, Alt=%fm" % (self._sensor.temperature, self._sensor.pressure, self._sensor.altitude))
        pass
    
    @property
    def temperature(self):
        return self._sensor.temperature

    @property
    def altitude(self):
        return self._sensor.altitude

    @property
    def pressure(self):
        return self._sensor.pressure

