import data_global as g
from meter_data import *

class TripStore:
    _name = b'meter.dat'
    def save(self, data):
        config = {}
        config['altsum'] = data.alt_data.sum
        config['altmin'] = data.alt_data.min
        config['altmax'] = data.alt_data.max
        config['wc'] = data.cycle_data.wheel_counter.sum
        config['wt'] = data.cycle_data.wheel_time.sum
        config['cc'] = data.cycle_data.crank_counter.sum
        config['ct'] = data.cycle_data.crank_time.sum
        config['speedmax'] = data.cycle_data.speed_max

        try:
            f = open(self._name, 'w')
            f.write(g.hal.json_dump(config))
            f.close()
        except Exception as e:
            print(e)
            pass

    def load(self, data):
        try:
            with open(self._name) as fp:
                config = g.hal.json_load(fp.read())
                for key, val in config.items():
                    if key == 'altsum':
                        data.alt_data.sum = val
                    elif key == 'altmin':
                        data.alt_data.min = val
                    elif key == 'altmax':
                        data.alt_data.max = val
                    elif key == 'wc':
                        data.cycle_data.wheel_counter.sum = val
                    elif key == 'wt':
                        data.cycle_data.wheel_time.sum = val
                    elif key == 'cc':
                        data.cycle_data.crank_counter.sum = val
                    elif key == 'ct':
                        data.cycle_data.crank_time.sum = val
                    elif key == 'speedmax':
                        data.cycle_data.speed_max = val
                    pass
        except Exception as e:
            print(e)
            pass
        pass
