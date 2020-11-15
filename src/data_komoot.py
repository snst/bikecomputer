import struct


class DataKomoot:
    def __init__(self):
        self.direction = 0
        self.distance = 0
        self.street = "Bahnhof Str."
        pass

    def on_data(self, data):
        print("k:on_data")
        #d = bytes(data)[:9]
        val = struct.unpack("<IBI", data)
        #print(val)
        self.street = (bytes(data)[9:]).decode()
        #print(s)
        self.direction = val[1]
        self.distance = val[2]
        print("%u %u %s" % (self.direction, self.distance, self.street))
        pass