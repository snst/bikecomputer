
class ButtonHandler:
    def __init__(self, hal, pin, callback, longclick_ms):
        self.pin = pin
        self.hal = hal
        self.button = hal.register_button(pin, self.on_button)
        self.t = None
        self.ignore_touch = False
        self.timestamp = 0
        self.last_state = -1
        self.callback = None
        self.cnt = 0
        self.set_callback(callback)
        self.longclick_ms = longclick_ms

    def on_button(self, val):
        #print("i %d" % (val))
        if val == self.last_state:
            return

        self.last_state = val
        delta = self.get_delta()
        
        if val == 0:
            #print("Down")
            #self.t = machine.Timer(-1)
            #self.t.init(period=SHORT_CLICK_MS, mode=machine.Timer.ONE_SHOT, callback=self.on_timer)
            self.t = self.hal.start_timer(1, self.longclick_ms, self.on_timer)
        else:
            if self.t != None and delta < self.longclick_ms - 50:
                self.hal.cancel_timer(self.t)
                self.t = None
                #print("%d Short    %d" % (self.cnt, delta))
                self.cnt += 1
                if self.callback:
                    self.callback(False)
            
    def on_timer(self, tim=None):
        if self.t != None:
            delta = self.get_delta()
            self.t = None
            #print("%d Long    %d" % (self.cnt, delta))
            self.cnt += 1
            if self.callback:
                self.callback(True)

    def get_delta(self):
        now = self.hal.ticks_ms()
        delta = now - self.timestamp
        self.timestamp = now
        return delta

    def set_callback(self, cb):
        self.callback = cb
        