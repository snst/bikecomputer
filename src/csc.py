
import struct


class CSC:

    def __init__(self):
        self.wheel_counter = 0
        self.wheel_event = 0
        self.crank_counter = 0
        self.crank_event = 0
        self.init = False
        self.is_riding = False
        self.wheel_size_cm = 214
        self.speed_kmh = 0
        self.crank_sec_sum = 0
        self.crank_counter_sum = 0
        self.average_cadence = 0
        self.cadence = 0
        self.wheel_sec_sum = 0
        self.wheel_counter_sum = 0
        self.average_speed_kmh = 0

    def diff_uint32(self, now, last):
        diff = 0
        if now >= last:
            diff = now - last
        else:
            diff = now + (0xFFFFFFFF - last)
        return diff

    def diff_uint16(self, now, last):
        diff = 0
        if now >= last:
            diff = now - last
        else:
            diff = now + (0xFFFFFFFF - last)
        return diff

    def calc_kmh(self, counter_delta, time_delta):
        if time_delta > 0:
            return (self.wheel_size_cm * counter_delta * 3.6) / time_delta / 100.0
        else:
            return 0

    def calc_cadence(self, counter_delta, time_delta):
        if time_delta > 0:
            return counter_delta * 60 / time_delta
        else:
            return 0

    def calc_average_cadence(self, val, time):
        self.crank_counter_sum += val
        self.crank_sec_sum += time
        return self.calc_cadence(self.crank_counter_sum, self.crank_sec_sum)

    def calc_average_kmh(self, val, time):
        self.wheel_counter_sum += val
        self.wheel_sec_sum += time
        return self.calc_kmh(self.wheel_counter_sum, self.wheel_sec_sum)

    def unpack_data(self, data):
        val = struct.unpack("<BIHHH", data)
        return val[1], val[2], val[3], val[4]

    def on_notify(self, data):
        wheel_counter, wheel_event, crank_counter, crank_event = self.unpack_data(data)

        if self.init:
            wheel_counter_diff = self.diff_uint32(wheel_counter, self.wheel_counter)
            wheel_delta_sec = self.diff_uint16(wheel_event, self.wheel_event) / 1024.0
            crank_counter_diff = self.diff_uint16(crank_counter, self.crank_counter)
            crank_delta_sec = self.diff_uint16(crank_event, self.crank_event) / 1024.0
            
            self.is_riding = wheel_counter_diff > 0

            self.speed_kmh = self.calc_kmh(wheel_counter_diff, wheel_delta_sec)

            self.cadence = self.calc_cadence(crank_counter_diff, crank_delta_sec)

            if self.cadence > 30 and self.cadence < 200:
                self.average_cadence = self.calc_average_cadence(crank_counter_diff, crank_delta_sec)

            if self.speed_kmh > 5 and self.speed_kmh < 100:
                self.average_speed_kmh = self.calc_average_kmh(wheel_counter_diff, wheel_delta_sec)

            print("is_riding=%d, speed=%.2f/%.2f, cadence=%d/%d" % (self.is_riding, self.speed_kmh, self.average_speed_kmh, self.cadence, self.average_cadence))

        self.wheel_counter = wheel_counter
        self.wheel_event = wheel_event
        self.crank_counter = crank_counter
        self.crank_event = crank_event
        self.init = True
