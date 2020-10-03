import time
import threading
from const import *

SHORT_CLICK_MS = 300

class ButtonHandler:
    def __init__(self, tft):
        tft.set_btn_callback(self.handle_touch_down, self.handle_touch_up)
        self.click_cb = None
        self.btn_timestamp = [0,0]
        self.last_btn_id = 0
        self.display = None
        self.ignore_touch = False
        self.settings = None
        self.t = None
        pass

    def set_settings(self, settings):
        self.settings = settings

    def set_display(self, display):
        self.display = display

    def get_ms(self):
        return int(round(time.time() * 1000))

    def btn_timer(self):
        #print("btn timeout")
        delta = self.get_ms() - self.btn_timestamp[self.last_btn_id]
        if delta > SHORT_CLICK_MS:
            if self.click_cb:
                self.click_cb(self.last_btn_id, True)
        #print("long click %d: %d" % (self.last_btn_id, delta))

    def handle_touch_down(self, id):
        self.ignore_touch = False if self.settings.touch_ignore == 1 else not self.display.is_display_on()
        self.display.set_display_on()

        if self.ignore_touch:
            print("ignore touch")

        #print("down %d" % (id))
        self.last_btn_id = id
        self.btn_timestamp[id] = self.get_ms()
        self.t = threading.Timer((SHORT_CLICK_MS+50)/1000, self.btn_timer)
        self.t.start()
        pass

    def handle_touch_up(self, id):
        if self.t:
            self.t.cancel()
        if self.ignore_touch:
            return            
        delta = self.get_ms() - self.btn_timestamp[id]
        if delta < SHORT_CLICK_MS:
            if self.click_cb:
                self.click_cb(id, False)
            #print("short click %d: %d" % (id, delta))

    def set_click_cb(self, cb):
        self.click_cb = cb
