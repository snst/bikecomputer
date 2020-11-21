import bluetooth
import random
import struct
import time
import micropython
from const import *

from micropython import const
from ble_advertising import decode_services, decode_name


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_ADV_SCAN_IND = const(0x02)
_ADV_NONCONN_IND = const(0x03)

_CSC_ADDR = bytes([0xf4, 0xb8, 0x5e, 0x40, 0xea, 0xe4])
_CSC_SERVICE_UUID = bluetooth.UUID(0x1816)
_CSC_MEASUREMENT_UUID = bluetooth.UUID(0x2A5B)
_CSC_DESC_UUID = bluetooth.UUID(0x2902)
_CSC_CHAR = (
    _CSC_MEASUREMENT_UUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
)
_CSC_SERVICE = (
    _CSC_SERVICE_UUID,
    (_CSC_CHAR,),
)

class ConnData:
    def __init__(self, name, fix_addr = None, service_uuid = None, char_uuid = None, csc_desc = None, on_read = None, on_notify = None):
        self._name = name
        self._addr_type = None
        self._addr = fix_addr
        self._service_uuid = service_uuid
        self._char_uuid = char_uuid
        self._csc_desc = csc_desc
        self._on_read = on_read
        self._on_notify = on_notify
        self.reset()
        pass

    def reset(self):
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._value_handle = None
        self._dsc_handle = None


class BleCentral:
    def __init__(self):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._state_callback = self.print_state
        self.connections = []
        self._is_scanning = False

    def find_client_by_addr(self, addr):
        for conn in self.connections:
            if addr == conn._addr:
                return conn
        return None

    def find_client_by_service(self, services):
        for conn in self.connections:
            if conn._service_uuid in services:
                return conn
        return None


    def add_connection(self, conn):
        self.connections.append(conn)

    def print_state(self, state):
        print("print_state: %d" % (state))

    def print_ble(self, str):
        print(str)
        pass

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            #print("_IRQ_SCAN_RESULT")
            #print(decode_name(adv_data))

            # find client with fixed address
            conn = self.find_client_by_addr(addr)

            if None == conn:
                s = decode_services(adv_data)
                #print(s)
                conn = self.find_client_by_service(s)

            if conn and conn._conn_handle == None:
                conn._addr_type = addr_type
                conn._addr = bytes(addr)
                #self._ble.gap_scan(None)
                self.connect(conn)

        elif event == _IRQ_SCAN_DONE:
            #print("_IRQ_SCAN_DONE")
            self._is_scanning = False

        elif event == _IRQ_PERIPHERAL_CONNECT:
            #self.print_ble("_IRQ_PERIPHERAL_CONNECT")
            conn_handle, addr_type, addr = data
            conn = self.find_client_by_addr(addr)
            #if addr_type == self._addr_type and addr == self._addr:
            if conn:
                print("connected: " + conn._name)
                conn._conn_handle = conn_handle
                self._ble.gattc_discover_services(conn._conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            #self.print_ble("_IRQ_PERIPHERAL_DISCONNECT")
            conn_handle, addr_type, addr = data
            conn = self.find_conn(conn_handle)
            if conn:
                print("disconnected: " + conn._name)
                conn.reset()

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            #self.print_ble("_IRQ_GATTC_SERVICE_RESULT")
            conn_handle, start_handle, end_handle, uuid = data
            #self.print_ble(uuid)
            conn = self.find_conn(conn_handle)
            if conn and uuid == conn._service_uuid:
                conn._start_handle, conn._end_handle = start_handle, end_handle
                self._ble.gattc_discover_characteristics(
                    conn._conn_handle, conn._start_handle, conn._end_handle
                )

        elif event == _IRQ_GATTC_SERVICE_DONE:
            #self.print_ble("_IRQ_GATTC_SERVICE_DONE")
            conn_handle, status = data
            conn = self.find_conn(conn_handle)
            if conn and None == conn._start_handle:
                self.disconnect(conn)


        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            #self.print_ble("_IRQ_GATTC_CHARACTERISTIC_RESULT")
            conn_handle, def_handle, value_handle, properties, uuid = data
            conn = self.find_conn(conn_handle)
            if conn and uuid == conn._char_uuid:
                conn._value_handle = value_handle
                #print("found char for " + conn._name)
                #=>self._ble.gattc_read(conn._conn_handle, conn._value_handle)
                if conn._csc_desc != None:
                    self._ble.gattc_discover_descriptors(
                        conn._conn_handle, conn._start_handle, conn._end_handle)

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            #self.print_ble("_IRQ_GATTC_CHARACTERISTIC_DONE")
            conn_handle, status = data

        elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
            #self.print_ble("_IRQ_GATTC_DESCRIPTOR_RESULT")
            conn_handle, dsc_handle, uuid = data
            #print(uuid)
            conn = self.find_conn(conn_handle)
            if conn and uuid == conn._csc_desc:
                conn._dsc_handle = dsc_handle
                print("found desc: %s : %u" % (conn._name, dsc_handle))
                #self._ble.gattc_write(conn._conn_handle, conn._dsc_handle, struct.pack("<H", int(1)))
                _NOTIFY_ENABLE = const(1)
                _INDICATE_ENABLE = const(2)
                self._ble.gattc_write(conn._conn_handle, dsc_handle, struct.pack('<h', _NOTIFY_ENABLE), 1)

        elif event == _IRQ_GATTC_DESCRIPTOR_DONE:
            #self.print_ble("_IRQ_GATTC_DESCRIPTOR_DONE")
             # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            #self._ble.gattc_write(self._conn_handle, self._dsc_handle, struct.pack("<H", int(1)))

        elif event == _IRQ_GATTC_READ_RESULT:
            #self.print_ble("_IRQ_GATTC_READ_RESULT")
            conn_handle, value_handle, char_data = data
            conn = self.find_conn(conn_handle)
            if conn and value_handle == conn._value_handle and None != conn._on_read:
                conn._on_read(char_data)

        elif event == _IRQ_GATTC_READ_DONE:
            conn_handle, value_handle, status = data

        elif event == _IRQ_GATTC_NOTIFY:
            #self.print_ble("_IRQ_GATTC_NOTIFY")
            conn_handle, value_handle, notify_data = data
            conn = self.find_conn(conn_handle)
            if conn and value_handle == conn._value_handle and None != conn._on_notify:
                conn._on_notify(notify_data)

    def find_conn(self, conn_handle):
        for conn in self.connections:
            if conn_handle == conn._conn_handle:
                return conn
        return None

    # Find a device advertising the environmental sensor service.
    def scan(self, callback=None):
        if not self._is_scanning:
            #print("scan")
            self._is_scanning = True
            self._ble.gap_scan(2000, 30000, 30000)

    # Connect to the specified device (otherwise use cached address from a scan).
    def connect(self, conn):
        print("connect to " +  conn._name)
        self._ble.gap_connect(conn._addr_type, conn._addr)

    def disconnect(self, conn):
        if None != conn._conn_handle:
            print("disconnect " +  conn._name)
            self._ble.gap_disconnect(conn._conn_handle)


    def disconnect_all(self):
        for conn in self.connections:
            self.disconnect(conn)

    def read(self, conn):
        #print(conn._conn_handle)
        #print(conn._value_handle)
        if None != conn._conn_handle and None != conn._value_handle:
            #print("read!!!!")
            self._ble.gattc_read(conn._conn_handle, conn._value_handle)


def demo():
    pass

if __name__ == "__main__":
    demo()