class DataCache:
    TRIP_ID = 0
    SPEED = 1
    CADENCE = 2
    SPEED_AVG = 3
    SPEED_AVG_COLOR = 4
    TRIP_DISTANCE = 5
    TRIP_DURATION = 6
    TRIP_ALTITUDE = 7
    SPEED_COLOR = 8
    NAV_SHOW_STREET = 9
    NAV_DIRECTION = 10
    NAV_KM_OR_TIME = 11
    NAV_DISTANCE = 12
    NAV_STREET = 13
    SPEED_MAX = 14
    CADENCE_AVG = 15
    GOAL_FINISHED = 16
    GOAL_REMAINING_DISTANCE = 17
    GOAL_REMAINING_TIME = 18
    GOAL_PROGRESS_MAX = 19
    GOAL_PROGRESS_VAL = 20
    GOAL_PROGRESS_MARKER = 21
    NAV_DIST_100 = 22
    GOAL_REQUIRED_AVG_SPEED = 23

    def __init__(self):
        self._items = []
        pass
    
    def changed(self, index, value):
        while len(self._items) <= index:
            self._items.append(None)

        if self._items[index] != value:
            self._items[index] = value
            return True
        else:
            return False
    
    def reset(self, do_reset = True):
        if do_reset:
            for i in range(0, len(self._items)):
                self._items[i] = None

    def reset_val(self, index):
        if index < len(self._items):
            self._items[index] = None