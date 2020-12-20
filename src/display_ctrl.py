import data_global as g

class DisplayCtrl:
    def __init__(self, settings):
        self.display_on = False
        self._settings = settings
        self.t = None
        self.callback = None
        self.set_display_on()

    def is_display_on(self):
        return self.display_on

    def set_display_off(self, tim=None):
        #print("set_display_off")
        g.hal.set_backlight(self._settings.led_off.value)
        self.display_on = False
        if self.callback != None:
            self.callback(self.display_on)

    def set_display_complete_off(self):
        g.hal.set_backlight(0)
        self.display_on = False
        if self.callback != None:
            self.callback(self.display_on)


    def set_display_on(self):
        g.hal.set_backlight(self._settings.led_on.value)
        self.display_on = True
        if self.callback != None:
            self.callback(self.display_on)

        g.hal.cancel_timer(self.t)

        if self._settings.led_time.value > 0:
            self.t = g.hal.start_timer(-1, (int)(self._settings.led_time.value*1000), self.set_display_off)

    def set_callback(self, cb):
        self.callback = cb

    