import micropython
import machine
import st7789
import time
from machine import Timer
from machine import I2C
from const import *
from button_handler import *
from bike_computer import *
from hal_esp32 import *
from nav_data import *
import data_global as g
from bt_manager import *
from altimeter_bmp280 import *
from scheduler import *


#https://github.com/palto42/komoot-navi/blob/master/src/main.cpp
#static BLEUUID serviceUUID("71C1E128-D92F-4FA8-A2B2-0F171DB3436C"); // navigationServiceUUID
#static BLEUUID charUUID("503DD605-9BCB-4F6E-B235-270A57483026");    // navigationServiceNotifyCharacteristicUUI
#static BLEUUID heartUUID("6D75DBF0-D763-4147-942A-D97B1BC700CF");   // navigationServiceHeartbeatWriteCharacteristicUUID
#https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_temperature_central.py

# MOSI 19, SCLK 18, CS 5, DC 16, RST 23, BL 4

spi = machine.SPI(1, baudrate=30000000, polarity=1, phase=1, sck=machine.Pin(18), mosi=machine.Pin(19))
tft = st7789.ST7789(
        spi, 135, 240,
        reset=machine.Pin(23, machine.Pin.OUT),
        cs=machine.Pin(5, machine.Pin.OUT),
        dc=machine.Pin(16, machine.Pin.OUT),
    )
tft.init()

g.display = Display(tft)
g.hal = Hal_esp32()
g.scheduler = Scheduler(g.hal)

g.bt = BtManager()

i2c = I2C(1, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
g.altimeter = Altimeter_bmp280(i2c)

g.bc = BikeComputer()

def task_mem():
    g.bc.add_task(5000, task_mem)
    #print("mem: %d" % (gc.mem_free()))

#task_mem()
g.bc.start()

while(True):
    try:
        g.scheduler.run()
    except OSError as exc:
        print("OSError %d" % exc.args[0])
