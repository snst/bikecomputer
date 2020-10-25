import threading
import time
import pygame
import json


class Hal_emu:
    btn_left = 97
    btn_right = 115

    def __init__(self, tft):
        self.t = None
        self.tft = tft
        self.clock = pygame.time.Clock()
        self.btn_callback = {}
        self.sim_callback = None
        pass

    def bt_reconnect(self):
        print("bt_reconnect")

    def set_backlight(self, val):
        print("hal: set_backlight %d" % (val))
        self.tft.set_brightness(val)

    def start_timer(self, id, ms, cb):
        t = threading.Timer(ms/1000, cb)
        t.start()
        return t

    def cancel_timer(self, t):
        if t != None:
            t.cancel()

    def register_sim_callback(self, cb):
        self.sim_callback = cb

    def register_button(self, pin, callback):
        self.btn_callback[pin] = callback
        return 0

    def ticks_ms(self):
        return int(round(time.time() * 1000))


    def json_load(self, x):
        return json.loads(x)

    def json_dump(self, x):
        return json.dumps(x)

    def mainloop(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                val = -1
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    val = 0
                    #x: 120
                    #y: 121
                    #space: 32
                    #self.btn_down(event.key)
                elif event.type == pygame.KEYUP:
                    val = 1
                    #self.btn_up(event.key)
                if val >= 0:
                    if event.key in self.btn_callback:
                        self.btn_callback[event.key](val)
                    elif val==0 and self.sim_callback:
                        self.sim_callback(event.key)


        pass        