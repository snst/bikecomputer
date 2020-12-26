class BtManagerEmu:
    def __init__(self):
        pass

    def read_komoot(self):
        pass

    def scan(self, csc_enabled, komoot_enabled):
        pass

    def reconnect_all(self):
        pass

    def is_csc_connected(self):
        return False

    def is_komoot_connected(self):
        return False

    def is_scanning(self):
        return True

    def register_cycle_callback(self, cb):
        pass

    def register_komoot_callback(self, cb):
        pass

    def register_cycle_callback(self, cycle_cb, bat_cb):
        pass

    def request_sensor_bat(self):
        pass