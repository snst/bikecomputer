import machine
import utime
import ujson
import time



class Hal_esp32:
    btn_left = 0
    btn_right = 35
    def __init__(self):
        self.t = None
        self.bt = None
        #self.tft = tft
        self.pin_cb = []
        self.led_pwm = machine.PWM(machine.Pin(4),5000)
        pass

    def set_bt(self, bt):
        self.bt = bt

    def set_backlight(self, val):
        #print("hal: set_backlight %d" % (val))
        self.led_pwm.duty((int)(val*102))
        #self.tft.set_brightness(val)

    def start_timer(self, id, ms, cb):
        #print("start_timer %d" %(ms))
        t = machine.Timer(id)
        t.init(period=ms, mode=machine.Timer.ONE_SHOT, callback=cb)
        return t    

    def cancel_timer(self, t):
        if t != None:
            t.deinit()

    def register_button(self, id, callback):
        #print("register_button %d" %(id))
        pin = machine.Pin(id, machine.Pin.IN, machine.Pin.PULL_UP)
        pin.irq(self.on_irq, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        self.pin_cb.append([pin, callback])

    def on_irq(self, pin):
        #print(pin)
        val = pin.value()
        for cb in self.pin_cb:
            if pin is cb[0]:
                cb[1](val)
        #print("on_irq %d: %d" %(pin.id, val))
        #self.pin_cb[pin.id](val)

    def ticks_ms(self):
        return utime.ticks_ms()


    def json_load(self, x):
        return ujson.loads(x)

    def json_dump(self, x):
        return ujson.dumps(x)        

    def bt_reconnect(self):
        if self.bt:
            self.bt.disconnect_all()
        pass

    def sleep_ms(self, ms):
        time.sleep_ms(ms)