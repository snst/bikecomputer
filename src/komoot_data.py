import struct

class KomootData:
    def __init__(self):
        self.direction = 0
        self.distance = 0
        self.street = "?"

    def on_data(self, data):
        val = struct.unpack("<IBI", data)
        self.street = (bytes(data)[9:]).decode()
        self.direction = val[1]
        self.distance = val[2]
        #print("%u %u %s" % (self.direction, self.distance, self.street))
