class DisplayCtrl:
    def __init__(self, settings, hal):
        self.display_on = False
        self.settings = settings
        self.t = None
        self.callback = None
        self.hal = hal
        self.set_display_on()


    def is_display_on(self):
        return self.display_on

    def set_display_off(self, tim=None):
        #print("set_display_off")
        self.hal.set_backlight(self.settings.led_off.value)
        self.display_on = False
        if self.callback != None:
            self.callback(self.display_on)

    def set_display_on(self):
        self.hal.set_backlight(self.settings.led_on.value)
        self.display_on = True
        if self.callback != None:
            self.callback(self.display_on)

        self.hal.cancel_timer(self.t)

        if self.settings.led_time.value > 0:
            self.t = self.hal.start_timer(-1, (int)(self.settings.led_time.value*1000), self.set_display_off)

    def set_callback(self, cb):
        self.callback = cb

    