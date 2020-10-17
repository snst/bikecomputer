import machine
import utime

SHORT_CLICK_MS = 300

class ButtonHandler:
    def __init__(self, pin):
        self.pin = pin
        self.button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.button.irq(self.on_irq, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        self.t = None
        self.ignore_touch = False
        self.timestamp = 0
        self.last_state = -1
        self.callback = None
        self.cnt = 0

    def on_irq(self, pin):
        val = pin.value()
        #print("i %d" % (val))
        if val == self.last_state:
            return

        self.last_state = val
        delta = self.get_delta()
        
        if val == 0:
            #print("Down")
            self.t = machine.Timer(-1)
            self.t.init(period=SHORT_CLICK_MS, mode=machine.Timer.ONE_SHOT, callback=self.on_timer)
        else:
            if self.t != None and delta < SHORT_CLICK_MS:
                #print("%d Short    %d" % (self.cnt, delta))
                self.cnt += 1
                if self.callback:
                    self.callback(False)
                self.t.deinit()
                self.t = None
            
    def on_timer(self, a):
        self.t = None
        delta = self.get_delta()
        #print("%d Long    %d" % (self.cnt, delta))
        self.cnt += 1
        if self.callback:
            self.callback(True)

    def get_delta(self):
        now = utime.ticks_ms()
        delta = now - self.timestamp
        self.timestamp = now
        return delta

    def set_callback(self, cb):
        self.callback = cb
        