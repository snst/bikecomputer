import micropython
import machine
import st7789
import time
from button_handler import *
from bike_computer import *
from const import *
from ble_csc_central import *
from hal_esp32 import *
from machine import Timer

Color.red = st7789.color565(255, 0, 0)
Color.green = st7789.color565(0, 255, 0)
Color.white = st7789.color565(255, 255, 255)
Color.black = st7789.color565(0, 0, 0)


print("m1")
# MOSI 19, SCLK 18, CS 5, DC 16, RST 23, BL 4
spi = machine.SPI(2, baudrate=30000000, polarity=1, phase=1, sck=machine.Pin(18), mosi=machine.Pin(19))
print("m2")
display = st7789.ST7789(
        spi, 135, 240,
        reset=machine.Pin(23, machine.Pin.OUT),
        cs=machine.Pin(5, machine.Pin.OUT),
        dc=machine.Pin(16, machine.Pin.OUT),
        #backlight=machine.Pin(4, machine.Pin.OUT),
    )
print("m3")
display.init()
print("m4")



hal = Hal_esp32()

bc = BikeComputer(display, hal)



def on_notify(data):
    bc.on_notify(data)
    bc.gui.cyclic_update()


#b = BleCscManager()
#b.set_callback_notify(on_notify)
#while(True):
#    b.scan()
#    b.loop()
#    time.sleep_ms(1000)