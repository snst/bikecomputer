from ble_central import *
from bt_manager_base import *

class BtManager(BtManagerBase):
    _CSC_ADDR = bytes([0xf4, 0xb8, 0x5e, 0x40, 0xea, 0xe4])
    _CSC_SERVICE_UUID = bluetooth.UUID(0x1816)
    _CSC_MEASUREMENT_UUID = bluetooth.UUID(0x2A5B)
    _CSC_DESC_UUID = bluetooth.UUID(0x2902)

    _KOMOOT_SERVICE_UUID = bluetooth.UUID("71c1e128-d92f-4fa8-a2b2-0f171db3436c")
    _KOMOOT_CHAR_UUID = bluetooth.UUID("503dd605-9bcb-4f6e-b235-270a57483026")
    #_KOMOOT_DESC_UUID = bluetooth.UUID("4a982902-1cc4-e7c1-c757-f1267dd021e8")
    _KOMOOT_DESC_UUID = bluetooth.UUID(0x2803)
    #_KOMOOT_DESC_UUID = bluetooth.UUID("503dd605-9bcb-4f6e-b235-270a57483026")
    #_KOMOOT_DESC_UUID = bluetooth.UUID(0x2902)

    _BAT_SERVICE_UUID = bluetooth.UUID(0x180F)
    _BAT_LEVEL_UUID = bluetooth.UUID(0x2A19)


    def __init__(self):
        self._bt = BleCentral()
        self._csc_service = ServiceData("csc", service_uuid = self._CSC_SERVICE_UUID, 
                                        char_uuid = self._CSC_MEASUREMENT_UUID, 
                                        notify = ServiceData.NOTIFY_ENABLE)
        self._csc_bat_service = ServiceData("bat", service_uuid = self._BAT_SERVICE_UUID, 
                                        char_uuid = self._BAT_LEVEL_UUID)

        self._con_csc = ConnData(name = "bike", fix_addr = self._CSC_ADDR)
        self._con_csc.add_service(self._csc_service)
        self._con_csc.add_service(self._csc_bat_service)


        self._komoot_service = ServiceData("komoot", service_uuid = self._KOMOOT_SERVICE_UUID, 
                                        char_uuid = self._KOMOOT_CHAR_UUID)
        self._con_komoot = ConnData(name = "komoot")
        self._con_komoot.add_service(self._komoot_service)

        self._bt.add_connection(self._con_csc)
        self._bt.add_connection(self._con_komoot)

    def read_komoot(self):
        self._bt.read(self._con_komoot, self._komoot_service)

    def scan(self, csc_enabled, komoot_enabled):
        self._con_csc.enabled = csc_enabled
        self._con_komoot.enabled = komoot_enabled
        self._bt.scan()

    def reconnect_all(self):
        self._bt.disconnect_all()

    def is_csc_connected(self):
        return self._con_csc._conn_handle != None

    def is_komoot_connected(self):
        return self._con_komoot._conn_handle != None        

    def is_scanning(self):
        return self._bt._is_scanning        

    def register_cycle_callback(self, cycle_cb, bat_cb):
        self._csc_service._on_notify = cycle_cb
        self._csc_bat_service._on_read = bat_cb
        pass

    def register_komoot_callback(self, cb):
        self._komoot_service._on_read = cb
        pass

    def request_sensor_bat(self):
        self._bt.read(self._con_csc, self._csc_bat_service)
        self._bt.enable_notify(self._con_csc, self._csc_service)
        #self._bt.enable_notify(self._con_komoot, self._komoot_service)
