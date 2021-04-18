import bluetooth
import random
import struct
import time
import micropython
import data_global as g
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


class ServiceData:
    NOTIFY_ENABLE = const(1)
    INDICATE_ENABLE = const(2)
    def __init__(self, name, service_uuid = None, char_uuid = None, notify = False, on_read = None, on_notify = None):
        #self._name = name
        self._service_uuid = service_uuid
        self._char_uuid = char_uuid
        self._csc_desc = None #csc_desc
        self._notify = notify
        self._on_read = on_read
        self._on_notify = on_notify
        self.reset()
        pass

    def reset(self):
        self._value_handle = None
        self._dsc_handle = None
        self._def_handle = None
        self._start_handle = None
        self._end_handle = None

class ConnData:
    def __init__(self, name, fix_addr = None):
        self._name = name
        self._addr_type = None
        self._addr = fix_addr
        self.enabled = True
        self.reset()
        self.services = []
        pass

    def reset(self):
        self._conn_handle = None

    def add_service(self, service):
        self.services.append(service)

    def find_service(self, uuid):
        for s in self.services:
            if s._service_uuid == uuid:
                return s
        return None

    def find_char(self, uuid):
        for s in self.services:
            if s._char_uuid == uuid:
                return s
        return None

    def find_desc(self, uuid):
        for s in self.services:
            if s._csc_desc == uuid:
                return s
        return None

    def find_value_handle(self, handle):
        for s in self.services:
            if s._value_handle == handle:
                return s
        return None


class BleCentral:
    def __init__(self, stat):
        self.stat = stat
        self._ble = bluetooth.BLE()
        self._ble.config(rxbuf=1024)
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

    def find_client_by_service(self, service):
        for conn in self.connections:
            if conn.find_service(service):
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
                services = decode_services(adv_data)
                #print(s)
                for s in services:
                    conn = self.find_client_by_service(s)

            if conn and conn.enabled and conn._conn_handle == None:
                conn._addr_type = addr_type
                conn._addr = bytes(addr)
                self.connect(conn)

        elif event == _IRQ_SCAN_DONE:
            #print("_IRQ_SCAN_DONE")
            self._is_scanning = False
            self.stat.cnt_scan_res += 1

        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            #self.print_ble("_IRQ_PERIPHERAL_CONNECT, ch=%u" % (conn_handle))
            self.stat.cnt_connect += 1
            conn = self.find_client_by_addr(addr)
            if conn:
                #print("connected: " + conn._name)
                conn._conn_handle = conn_handle
               #self._ble.gattc_discover_services(conn._conn_handle)
                self._ble.gattc_discover_characteristics(conn._conn_handle, 1, 0xFFFF)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, addr_type, addr = data
            self.stat.cnt_disconnect += 1
            #self.print_ble("_IRQ_PERIPHERAL_DISCONNECT, ch=%u" % (conn_handle))
            conn = self.find_conn(conn_handle)
            if conn:
                #print("disconnected: " + conn._name)
                conn.reset()

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start_handle, end_handle, uuid = data
            #self.print_ble("_IRQ_GATTC_SERVICE_RESULT, ch=%u, sh=%u, eh=%u, %s" % (conn_handle, start_handle, end_handle, uuid))
            conn = self.find_conn(conn_handle)
            if conn:
                srv = conn.find_service(uuid)
                if srv:
                    srv._start_handle, srv._end_handle = start_handle, end_handle
                    #self.print_ble("Found srv! %s, sh=%u, eh=%u, %s" % (conn._name, srv._start_handle, srv._end_handle, uuid))
                    #self._ble.gattc_discover_characteristics(conn._conn_handle, srv._start_handle, srv._end_handle)

        elif event == _IRQ_GATTC_SERVICE_DONE:
            conn_handle, status = data
            #self.print_ble("_IRQ_GATTC_SERVICE_DONE, ch=%u" % (conn_handle))
            conn = self.find_conn(conn_handle)
            #if conn and None == conn._start_handle:
            #    self.disconnect(conn)


        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            #self.print_ble("_IRQ_GATTC_CHARACTERISTIC_RESULT, ch=%u, dh=%u, vh=%u, %s" % (conn_handle, def_handle, value_handle, uuid))
            conn = self.find_conn(conn_handle)
            if conn:
                srv = conn.find_char(uuid)
                if srv:
                    srv._value_handle = value_handle
                    srv._def_handle = def_handle
                    #if srv._notify == ServiceData.NOTIFY_ENABLE:
                    #    print("NOTIFY_ENABLE!!!")
                    #    self.enable_notify(conn, srv)

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            conn_handle, status = data
            #self.print_ble("_IRQ_GATTC_CHARACTERISTIC_DONE, ch=%u" % (conn_handle))
            g.scheduler.insert(500, lambda : self.request_notify())

            #conn = self.find_conn(conn_handle)
            #if conn:
            #    for srv in conn.services:
            #        if srv._notify == ServiceData.NOTIFY_ENABLE:
            #            print("NOTIFY_ENABLE!")
            #            self.enable_notify(conn, srv)
#                        g.scheduler.insert(500, lambda : self.enable_notify2(conn._conn_handle, srv._value_handle))
#                        g.scheduler.insert(500, lambda : self.enable_notify2(0, 18))
                        #self._ble.gattc_write(conn._conn_handle, srv._value_handle + 1, struct.pack('<h', _NOTIFY_ENABLE), 1)
                        #notify = ServiceData.NOTIFY_ENABLE

#                if srv._notify:
#                    self._ble.gattc_write(conn._conn_handle, srv._value_handle + 1, struct.pack('<h', _NOTIFY_ENABLE), 1)


        elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
            conn_handle, dsc_handle, uuid = data
            #self.print_ble("_IRQ_GATTC_DESCRIPTOR_RESULT, ch=%u, dh=%u, %s" % (conn_handle, dsc_handle, uuid))
            conn = self.find_conn(conn_handle)
            srv = conn.find_desc(uuid)
            if conn and srv:
                srv._dsc_handle = dsc_handle
                #print("found desc: %s : %u" % (conn._name, dsc_handle))
                #self._ble.gattc_write(conn._conn_handle, conn._dsc_handle, struct.pack("<H", int(1)))
                #_NOTIFY_ENABLE = const(1)
                #_INDICATE_ENABLE = const(2)
                #print("dsc handle %d" % (dsc_handle))
                #self._ble.gattc_write(conn._conn_handle, srv._dsc_handle, struct.pack('<h', _NOTIFY_ENABLE), 1)
                #self._ble.gattc_write(conn._conn_handle, srv._value_handle+1, struct.pack('<H', _NOTIFY_ENABLE), 1)

        elif event == _IRQ_GATTC_DESCRIPTOR_DONE:
             # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            #self.print_ble("_IRQ_GATTC_DESCRIPTOR_DONE, ch=%u" % (conn_handle))
            #self._ble.gattc_write(self._conn_handle, self._dsc_handle, struct.pack("<H", int(1)))

        elif event == _IRQ_GATTC_READ_RESULT:
            #self.print_ble("_IRQ_GATTC_READ_RESULT")
            conn_handle, value_handle, char_data = data
            self.stat.cnt_read_res += 1
            conn = self.find_conn(conn_handle)
            if conn:
                srv = conn.find_value_handle(value_handle)
                if srv and srv._on_read:
                    srv._on_read(char_data)

        elif event == _IRQ_GATTC_READ_DONE:
            conn_handle, value_handle, status = data

        elif event == _IRQ_GATTC_NOTIFY:
            #self.print_ble("_IRQ_GATTC_NOTIFY")
            self.stat.cnt_notify_res += 1
            conn_handle, value_handle, notify_data = data
            conn = self.find_conn(conn_handle)
            if conn:
                srv = conn.find_value_handle(value_handle)
                if srv and srv._on_notify:
                    srv._on_notify(notify_data)

        elif event == _IRQ_GATTC_INDICATE:
            #self.print_ble("_IRQ_GATTC_INDICATE")
            # A server has sent an indicate request.
            conn_handle, value_handle, notify_data = data

    def find_conn(self, conn_handle):
        for conn in self.connections:
            if conn_handle == conn._conn_handle:
                return conn
        return None

    def request_notify(self):
        #print("request_notify")
        for conn in self.connections:
            for srv in conn.services:
                if srv._notify:
                    self.enable_notify(conn, srv)


    def enable_notify(self, conn, service):
        #print("enable_notify")
        if conn._conn_handle != None and service._value_handle != None:
            #print("req notify %d, %d" % (conn._conn_handle, service._value_handle))
            self._ble.gattc_write(conn._conn_handle, service._value_handle + 1, struct.pack('<h', 1), 1)
            self.stat.cnt_notify_req += 1

    # Find a device advertising the environmental sensor service.
    def scan(self, callback=None):
        #if not self._is_scanning:
        #print("+scan")
        self._is_scanning = True
        self._ble.gap_scan(2000, 30000, 30000)
        self.stat.cnt_scan_req += 1

    def stop_scan(self):
        #print("+stop_scan")
        #self._is_scanning = True
        self._ble.gap_scan(None)

    # Connect to the specified device (otherwise use cached address from a scan).
    def connect(self, conn):
        #print("connect to " +  conn._name)
        self._ble.gap_connect(conn._addr_type, conn._addr)

    def disconnect(self, conn):
        if None != conn._conn_handle:
            #print("disconnect " +  conn._name)
            self._ble.gap_disconnect(conn._conn_handle)
            conn.reset()


    def disconnect_all(self):

        self._ble.active(False)
        time.sleep(0.5)
        self._ble.active(True)

        time.sleep(0.5)
        for conn in self.connections:
            #self.disconnect(conn)
            conn.reset()


    def read(self, conn, srv):
        try:
            if None != conn._conn_handle and None != srv._value_handle:
                #print("READ %d %d" % (conn._conn_handle, srv._value_handle))
                self._ble.gattc_read(conn._conn_handle, srv._value_handle)
                self.stat.cnt_read_req += 1
        except OSError as exc:
            print("ble:read:err: %d" % exc.args[0])


def demo():
    pass

if __name__ == "__main__":
    demo()