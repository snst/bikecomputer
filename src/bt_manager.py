from ble_central import *
from bt_manager_base import *

class BtManager(BtManagerBase):
    _CSC_ADDR = bytes([0xf4, 0xb8, 0x5e, 0x40, 0xea, 0xe4])
    _CSC_SERVICE_UUID = bluetooth.UUID(0x1816)
    _CSC_MEASUREMENT_UUID = bluetooth.UUID(0x2A5B)
    _CSC_DESC_UUID = bluetooth.UUID(0x2902)

    _KOMOOT_SERVICE_UUID = bluetooth.UUID("71c1e128-d92f-4fa8-a2b2-0f171db3436c")
    _KOMOOT_CHAR_UUID = bluetooth.UUID("503dd605-9bcb-4f6e-b235-270a57483026")
    _KOMOOT_DESC_UUID = bluetooth.UUID("4a982902-1cc4-e7c1-c757-f1267dd021e8")

    def __init__(self):
        self._bt = BleCentral()
        self._con_csc = ConnData(name = "csc", fix_addr = self._CSC_ADDR, service_uuid = self._CSC_SERVICE_UUID, char_uuid = self._CSC_MEASUREMENT_UUID, csc_desc = self._CSC_DESC_UUID)
        self._con_komoot = ConnData(name = "komoot", service_uuid = self._KOMOOT_SERVICE_UUID, char_uuid = self._KOMOOT_CHAR_UUID, csc_desc = None)
        self._bt.add_connection(self._con_csc)
        self._bt.add_connection(self._con_komoot)

    def read_komoot(self):
        self._bt.read(self._con_komoot)

    def scan(self):
        self._bt.scan()

    def reconnect_all(self):
        self._bt.disconnect_all()

    def is_csc_connected(self):
        return self._con_csc._conn_handle != None

    def is_komoot_connected(self):
        return self._con_komoot._conn_handle != None        

    def is_scanning(self):
        return self._bt._is_scanning        

    def set_on_csc(self, cb):
        self._con_csc._on_notify = cb
        pass

    def set_on_komoot(self, cb):
        self._con_komoot._on_read = cb
        pass
