import threading
import time

class DisplayDim:
    def __init__(self, settings):
        self.display_on = False
        self.settings = settings
        self.t = None
        self.callback = None
        self.set_display_on()


    def is_display_on(self):
        return self.display_on

    def set_display_off(self):
        print("display off: %d" % (self.settings.led_off.value))
        self.display_on = False
        if self.callback != None:
            self.callback(self.display_on)

    def set_display_on(self):
        print("display on: %d for %d" % (self.settings.led_on.value, self.settings.led_time.value))
        self.display_on = True
        if self.callback != None:
            self.callback(self.display_on)

        if self.t != None:
            self.t.cancel()
            self.t = None

        if self.settings.led_time.value > 0:
            self.t = threading.Timer(self.settings.led_time.value, self.set_display_off)
            self.t.start()

    def set_callback(self, cb):
        self.callback = cb

    