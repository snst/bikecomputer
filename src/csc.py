
import struct

class CSC:

    def __init__(self, settings):
        self.settings = settings

    def calc_kmh_from_csc_val(self, wheel_counter, time_counter):
        if time_counter > 0:
            # wheel_counter * wheel_cm     3600
            # ------------------------  *  ---------------
            #         100 * 1000           time_counter / 1024
            return (self.settings.wheel_cm.value * wheel_counter * 36) / (1000 * time_counter / 1024)
        else:
            return 0

    def calc_cadence_from_csc_val(self, crank_counter, time_delta):
        if time_delta > 0:
            return (crank_counter * 60 * 1024) / time_delta
        else:
            return 0


    def calc_kmh(self, counter_delta, time_delta):
        if time_delta > 0:
            return (self.settings.wheel_cm.value * counter_delta * 3.6) / time_delta / 100.0
        else:
            return 0

    def calc_cadence(self, counter_delta, time_delta):
        if time_delta > 0:
            return counter_delta * 60 / time_delta
        else:
            return 0

    def unpack_data(self, data):
        val = struct.unpack("<BIHHH", data)
        return val[1], val[2], val[3], val[4]

    
    def process(self, raw_data, data):
        wheel_counter, wheel_time, crank_counter, crank_time = self.unpack_data(raw_data)

        data.wheel_counter.calc_delta(wheel_counter)
        data.wheel_time.calc_delta(wheel_time)
        data.crank_counter.calc_delta(crank_counter)
        data.crank_time.calc_delta(crank_time)

        if data.init:

            data.speed = self.calc_kmh_from_csc_val(data.wheel_counter.delta, data.wheel_time.delta)

            data.cadence = self.calc_cadence_from_csc_val(data.crank_counter.delta, data.crank_time.delta)

            if data.cadence > 10 and data.cadence < 200:
                data.crank_counter.add_delta()
                data.crank_time.add_delta()
                data.cadence_avg = self.calc_cadence_from_csc_val(data.crank_counter.sum, data.crank_time.sum)

            valid_speed = data.speed < 100
            data.is_riding = valid_speed and data.speed > self.settings.min_speed.value

            if valid_speed:
                data.speed_max = max(data.speed_max, data.speed)

                if data.is_riding:
                    data.wheel_counter.add_delta()
                    data.wheel_time.add_delta()
                    data.speed_avg = self.calc_kmh_from_csc_val(data.wheel_counter.sum, data.wheel_time.sum)
    

            #print("is_riding=%d, speed=%.2f/%.2f, cadence=%d/%d" % (self.is_riding, self.speed_kmh, self.average_speed_kmh, self.cadence, self.average_cadence))
            data.trip_distance = data.wheel_counter.get_distance_in_km(self.settings.wheel_cm.value)
            data.trip_duration_min = data.wheel_time.get_sum_in_min()

            if data.goal != None:
                self.calc_goal(data)

        data.init = True


    def calc_goal(self, data):
        data.goal.calculate_progress(data)
