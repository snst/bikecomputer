from altitude_data import *
from cycle_data import *
from env_data import *
from altitude_sum import *


class MeterData:
    def __init__(self, id, env_data, settings):
        self.id = id
        self.cycle_data = CycleData(id, settings)
        self.alt_data = AltitudeSum()
        self.env_data = env_data
        self.settings = settings
        pass