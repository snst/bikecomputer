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
from data_komoot import *
from scheduler import *

#https://github.com/palto42/komoot-navi/blob/master/src/main.cpp
#static BLEUUID serviceUUID("71C1E128-D92F-4FA8-A2B2-0F171DB3436C"); // navigationServiceUUID
#static BLEUUID charUUID("503DD605-9BCB-4F6E-B235-270A57483026");    // navigationServiceNotifyCharacteristicUUI
#static BLEUUID heartUUID("6D75DBF0-D763-4147-942A-D97B1BC700CF");   // navigationServiceHeartbeatWriteCharacteristicUUID
#https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_temperature_central.py


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
sch = Scheduler(hal)

bc = BikeComputer(display, hal)

_CSC_ADDR = bytes([0xf4, 0xb8, 0x5e, 0x40, 0xea, 0xe4])
_CSC_SERVICE_UUID = bluetooth.UUID(0x1816)
_CSC_MEASUREMENT_UUID = bluetooth.UUID(0x2A5B)
_CSC_DESC_UUID = bluetooth.UUID(0x2902)

_KOMOOT_SERVICE_UUID = bluetooth.UUID("71c1e128-d92f-4fa8-a2b2-0f171db3436c")
_KOMOOT_CHAR_UUID = bluetooth.UUID("503dd605-9bcb-4f6e-b235-270a57483026")
_KOMOOT_DESC_UUID = bluetooth.UUID("4a982902-1cc4-e7c1-c757-f1267dd021e8")
#static BLEUUID heartUUID("6D75DBF0-D763-4147-942A-D97B1BC700CF");   // navigationServiceHeartbeatWriteCharacteristicUUID


#static BLEUUID charUUID("503DD605-9BCB-4F6E-B235-270A57483026");


#if bc.settings.bt.value == 1:

con_csc = ConnData(name = "csc", fix_addr = _CSC_ADDR, service_uuid = _CSC_SERVICE_UUID, char_uuid = _CSC_MEASUREMENT_UUID, csc_desc = _CSC_DESC_UUID, on_notify=bc.on_data_csc)
con_komoot = ConnData(name = "komoot", service_uuid = _KOMOOT_SERVICE_UUID, char_uuid = _KOMOOT_CHAR_UUID, csc_desc = None, on_read = bc.on_data_komoot)
b = BleCscManager()
b.add_connection(con_csc)
b.add_connection(con_komoot)

hal.set_bt(b)
#b.set_on_notify(bc.on_notify)
b.set_on_state(bc.on_conn_state)

def task_update_gui():
    #print("task_update_gui")
    sch.insert(500, task_update_gui)
    bc.gui.cyclic_update()

def task_update_bt():
    #print("task_update_bt")
    #if b.conn_state == ConnState.disconnected or b.conn_state == ConnState.no_device:
    sch.insert(1000, task_update_bt)
    if con_csc._conn_handle == None or con_csc._conn_handle == None:
        b.scan()

def task_read_komoot():
    #print("task_read_komoot")
    sch.insert(4000, task_read_komoot)
    b.read(con_komoot)

task_update_gui()
task_update_bt()
task_read_komoot()

while(True):
    
    #elif b.conn_state == ConnState.found_device:
    #    b.connect()
    #else:
    #    ms = 1000
    try:
        sch.run()
    except OSError:
        print("OSError")
