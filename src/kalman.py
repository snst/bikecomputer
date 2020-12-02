class Kalman:
    def __init__(self, mea_e = 0.01, est_e = 1, q = 0.01):
        self._err_measure = mea_e
        self._err_estimate = est_e
        self._q = q
        self._current_estimate = 0
        self._last_estimate = None
        self._kalman_gain = 0


    def update(self, mea):
        if self._last_estimate == None:
            self._last_estimate = mea
        self._kalman_gain = self._err_estimate/(self._err_estimate + self._err_measure)
        self._current_estimate = self._last_estimate + self._kalman_gain * (mea - self._last_estimate)
        self._err_estimate =  (1.0 - self._kalman_gain)*self._err_estimate + abs(self._last_estimate - self._current_estimate) * self._q
        self._last_estimate = self._current_estimate
        return self._current_estimate

