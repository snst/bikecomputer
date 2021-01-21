import data_global as g
from trip_data import *

class TripStore:
    _name = b'meter.dat'

    def save(self, data):
        config = {}
        config['altsum'] = data.alt_data.sum
        config['altmin'] = data.alt_data.min
        config['altmax'] = data.alt_data.max
        config['wc'] = data.wheel_counter
        config['wt'] = data.wheel_time
        config['cc'] = data.crank_counter
        config['ct'] = data.crank_time
        config['speedmax'] = data.speed_max

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
                        data.wheel_counter = val
                    elif key == 'wt':
                        data.wheel_time = val
                    elif key == 'cc':
                        data.crank_counter = val
                    elif key == 'ct':
                        data.crank_time = val
                    elif key == 'speedmax':
                        data.speed_max = val
                    pass
        except Exception as e:
            print(e)
            pass
        
