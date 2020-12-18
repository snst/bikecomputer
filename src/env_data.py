class EnvData:
    def __init__(self):
        self.sensor_bat_percent = 0
        self.computer_bat_volt = 0

    def on_sensor_bat(self, data):
        self.sensor_bat_percent = data[0]
