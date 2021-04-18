import struct

class NavData:
    def __init__(self):
        self.direction = 0
        self.distance = 0
        self.street = "?"
        self.msg_cnt = 0

    def on_data(self, data):
        val = struct.unpack("<IBI", data)
        self.street = (bytes(data)[9:]).decode()
        self.direction = val[1]
        self.distance = val[2]
        self.msg_cnt += 1
        #print("%u %u %s" % (self.direction, self.distance, self.street))
