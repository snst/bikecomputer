import micropython
import machine
import st7789
import time
from button_handler import *
from bike_computer import *
from const import *
from ble_central import *
from hal_esp32 import *
from machine import Timer
from data_komoot import *
import data_global as g

#https://github.com/palto42/komoot-navi/blob/master/src/main.cpp
#static BLEUUID serviceUUID("71C1E128-D92F-4FA8-A2B2-0F171DB3436C"); // navigationServiceUUID
#static BLEUUID charUUID("503DD605-9BCB-4F6E-B235-270A57483026");    // navigationServiceNotifyCharacteristicUUI
#static BLEUUID heartUUID("6D75DBF0-D763-4147-942A-D97B1BC700CF");   // navigationServiceHeartbeatWriteCharacteristicUUID
#https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_temperature_central.py

# MOSI 19, SCLK 18, CS 5, DC 16, RST 23, BL 4

spi = machine.SPI(2, baudrate=30000000, polarity=1, phase=1, sck=machine.Pin(18), mosi=machine.Pin(19))
tft = st7789.ST7789(
        spi, 135, 240,
        reset=machine.Pin(23, machine.Pin.OUT),
        cs=machine.Pin(5, machine.Pin.OUT),
        dc=machine.Pin(16, machine.Pin.OUT),
    )
tft.init()

g.display = Display(tft)
g.hal = Hal_esp32()

bc = BikeComputer()

_CSC_ADDR = bytes([0xf4, 0xb8, 0x5e, 0x40, 0xea, 0xe4])
_CSC_SERVICE_UUID = bluetooth.UUID(0x1816)
_CSC_MEASUREMENT_UUID = bluetooth.UUID(0x2A5B)
_CSC_DESC_UUID = bluetooth.UUID(0x2902)

_KOMOOT_SERVICE_UUID = bluetooth.UUID("71c1e128-d92f-4fa8-a2b2-0f171db3436c")
_KOMOOT_CHAR_UUID = bluetooth.UUID("503dd605-9bcb-4f6e-b235-270a57483026")
_KOMOOT_DESC_UUID = bluetooth.UUID("4a982902-1cc4-e7c1-c757-f1267dd021e8")
#static BLEUUID heartUUID("6D75DBF0-D763-4147-942A-D97B1BC700CF");   // navigationServiceHeartbeatWriteCharacteristicUUID


#static BLEUUID charUUID("503DD605-9BCB-4F6E-B235-270A57483026");

#machine.freq()          # get the current frequency of the CPU
#machine.freq(80000000) # set the CPU frequency to 240 MHz
print("freq: %u" % (machine.freq() ))
#if bc.settings.bt.value == 1:

con_csc = ConnData(name = "csc", fix_addr = _CSC_ADDR, service_uuid = _CSC_SERVICE_UUID, char_uuid = _CSC_MEASUREMENT_UUID, csc_desc = _CSC_DESC_UUID, on_notify=bc.on_data_csc)
con_komoot = ConnData(name = "komoot", service_uuid = _KOMOOT_SERVICE_UUID, char_uuid = _KOMOOT_CHAR_UUID, csc_desc = None, on_read = bc.on_data_komoot)
bt = BleCentral()
bt.add_connection(con_csc)
bt.add_connection(con_komoot)

g.hal.set_bt(bt)

def task_update_bt():
    #print("task_update_bt")
    bc.add_task(5000, task_update_bt)
    if bc.settings.bt.value == 1:
        if con_csc._conn_handle == None or con_komoot._conn_handle == None:
            bt.scan()

def task_read_komoot():
    #print("task_read_komoot")
    bc.add_task(4000, task_read_komoot)
    bt.read(con_komoot)

task_update_bt()
task_read_komoot()

while(True):
    try:
        bc._sch.run()
    except OSError:
        print("OSError")
