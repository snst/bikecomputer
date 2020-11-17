class BtManagerBase:
    def __init__(self):
        pass

    def read_komoot(self):
        pass

    def scan(self):
        pass

    def reconnect_all(self):
        pass

    def is_csc_connected(self):
        return True

    def is_komoot_connected(self):
        return True

    def is_scanning(self):
        return True

    def set_on_csc(self, cb):
        pass

    def set_on_komoot(self, cb):
        pass
