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


#Color.red = st7789.color565(255, 0, 0)
#Color.green = st7789.color565(0, 255, 0)
#Color.white = st7789.color565(255, 255, 255)
#Color.black = st7789.color565(0, 0, 0)


# MOSI 19, SCLK 18, CS 5, DC 16, RST 23, BL 4
spi = machine.SPI(2, baudrate=30000000, polarity=1, phase=1, sck=machine.Pin(18), mosi=machine.Pin(19))
display = st7789.ST7789(
        spi, 135, 240,
        reset=machine.Pin(23, machine.Pin.OUT),
        cs=machine.Pin(5, machine.Pin.OUT),
        dc=machine.Pin(16, machine.Pin.OUT),
    )
display.init()

hal = Hal_esp32()

bc = BikeComputer(display, hal)


if bc.settings.bt.value == 1:
    b = BleCscManager()
    hal.set_bt(b)
    b.set_on_notify(bc.on_notify)
    b.set_on_state(bc.on_conn_state)

    while(True):
        #print("CS %d" %(b.conn_state))
        ms = 500
        bc.gui.cyclic_update()
        if b.conn_state == ConnState.disconnected or b.conn_state == ConnState.no_device:
            b.scan()
        elif b.conn_state == ConnState.found_device:
            b.connect()
        else:
            ms = 1000
        time.sleep_ms(ms)
