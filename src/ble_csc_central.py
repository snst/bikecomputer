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
        self.disconnect()
        pass

    def disconnect(self):
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._value_handle = None
        self._dsc_handle = None


class BLECscCentral:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._state_callback = self.print_state
        self.connections = []
        self._is_scanning = False
        self._reset()

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

    def _reset(self):
        #self._scan_callback = None
        self._conn_callback = None
        self._read_callback = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            #print("_IRQ_SCAN_RESULT")
            #print(decode_name(adv_data))
            s = decode_services(adv_data)
            #print(s)
            conn = self.find_client_by_service(s)
            if conn:
                #print("find_client_by_service")
                pass
            else:
                conn = self.find_client_by_addr(addr)

            if conn and conn._conn_handle == None:
                conn._addr_type = addr_type
                conn._addr = bytes(addr)  # Note: addr buffer is owned by caller so need to copy it.
                #conn._name = decode_name(adv_data) or "?"
                #self._ble.gap_scan(None)
                #self._state_callback(ConnState.found_device)
                print("found and connect: " + conn._name)
                self.connect(conn)
            #else:
            #    print("ignore found bt device")

        elif event == _IRQ_SCAN_DONE:
            #print("_IRQ_SCAN_DONE")
                #self._state_callback(ConnState.no_device)
            self._is_scanning = False
            pass

        elif event == _IRQ_PERIPHERAL_CONNECT:
            # Connect successful.
            conn_handle, addr_type, addr = data
            #self.print_ble("_IRQ_PERIPHERAL_CONNECT")
            conn = self.find_client_by_addr(addr)
            #if addr_type == self._addr_type and addr == self._addr:
            if conn:
                print("connect: " + conn._name)
                conn._conn_handle = conn_handle
                self._ble.gattc_discover_services(conn._conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # Disconnect (either initiated by us or the remote end).
            conn_handle, addr_type, addr = data
            #self.print_ble("_IRQ_PERIPHERAL_DISCONNECT")
            for conn in self.connections:
                if conn_handle == conn._conn_handle:
                    print("disconnected: " + conn._name)
                    conn.disconnect()
            #self._state_callback(ConnState.disconnected)

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            # Connected device returned a service.
            conn_handle, start_handle, end_handle, uuid = data
            #self.print_ble("_IRQ_GATTC_SERVICE_RESULT")
            #self.print_ble(uuid)
            for conn in self.connections:
                if conn_handle == conn._conn_handle and uuid == conn._service_uuid:
                    conn._start_handle, conn._end_handle = start_handle, end_handle
                    self._ble.gattc_discover_characteristics(
                        conn._conn_handle, conn._start_handle, conn._end_handle
                    )

        elif event == _IRQ_GATTC_SERVICE_DONE:
            # Service query complete.
            conn_handle, status = data
            #self.print_ble("_IRQ_GATTC_SERVICE_DONE")
            #if self._start_handle and self._end_handle:
            #    pass
                #self._ble.gattc_discover_characteristics(
                #    self._conn_handle, self._start_handle, self._end_handle
                #)
            #else:
            #    self.print_ble("Failed to find csc service.")

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            # Connected device returned a characteristic.
            conn_handle, def_handle, value_handle, properties, uuid = data
            #self.print_ble("_IRQ_GATTC_CHARACTERISTIC_RESULT")
            for conn in self.connections:
                if conn_handle == conn._conn_handle and uuid == conn._char_uuid:
                    conn._value_handle = value_handle
                    #print("found char for " + conn._name)
                    #=>self._ble.gattc_read(conn._conn_handle, conn._value_handle)
                    if conn._csc_desc != None:
                        self._ble.gattc_discover_descriptors(
                            conn._conn_handle, conn._start_handle, conn._end_handle)

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            # Characteristic query complete.
            conn_handle, status = data
            #self.print_ble("_IRQ_GATTC_CHARACTERISTIC_DONE")
            #if self._value_handle:
                # We've finished connecting and discovering device, fire the connect callback.
            #    if self._conn_callback:
            #        self._conn_callback()

                #self._ble.gattc_write(self._conn_handle, self._value_handle, struct.pack("<H", int(1)))
#                self._ble.gattc_discover_descriptors(
#                    self._conn_handle, self._start_handle, self._end_handle
#                )
            #else:
            #    self.print_ble("Failed to find csc characteristic.")

        elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
            # Called for each descriptor found by gattc_discover_descriptors().
            conn_handle, dsc_handle, uuid = data
            #self.print_ble("_IRQ_GATTC_DESCRIPTOR_RESULT")
            #print(uuid)
            for conn in self.connections:
                if conn_handle == conn._conn_handle and uuid == conn._csc_desc:
                    print("found _csc_desc:")
                    print(dsc_handle)
                    conn._dsc_handle = dsc_handle
                    #self._ble.gattc_write(conn._conn_handle, conn._dsc_handle, struct.pack("<H", int(1)))
                    _NOTIFY_ENABLE = const(1)
                    _INDICATE_ENABLE = const(2)
                    self._ble.gattc_write(conn._conn_handle, dsc_handle, struct.pack('<h', _NOTIFY_ENABLE), 1)

        elif event == _IRQ_GATTC_DESCRIPTOR_DONE:
             # Called once service discovery is complete.
             # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            #self.print_ble("_IRQ_GATTC_DESCRIPTOR_DONE")
            #self._state_callback(ConnState.connected)
            #self._ble.gattc_write(self._conn_handle, self._dsc_handle, struct.pack("<H", int(1)))

        elif event == _IRQ_GATTC_READ_RESULT:
            # A read completed successfully.
            #self.print_ble("_IRQ_GATTC_READ_RESULT")
            conn_handle, value_handle, char_data = data
            for conn in self.connections:
                if conn_handle == conn._conn_handle and conn._on_read:
                    conn._on_read(char_data)
            #if conn_handle == self._conn_handle and value_handle == self._value_handle:
                    #self._update_value(char_data)
                    #if self._read_callback:
                        #self._read_callback(self._value)
                        #self._read_callback = None

        elif event == _IRQ_GATTC_READ_DONE:
            # Read completed (no-op).
            conn_handle, value_handle, status = data

        elif event == _IRQ_GATTC_NOTIFY:
            #self.print_ble("_IRQ_GATTC_NOTIFY")
            # The ble_temperature.py demo periodically notifies its value.
            conn_handle, value_handle, notify_data = data
            for conn in self.connections:
                if conn_handle == conn._conn_handle and value_handle == conn._value_handle:
                    #self._update_value(notify_data)
                    if conn._on_notify:
                        conn._on_notify(notify_data)

    # Returns true if we've successfully connected and discovered characteristics.
    def is_connected(self):
        return self._conn_handle is not None and self._value_handle is not None

    # Find a device advertising the environmental sensor service.
    def scan(self, callback=None):
        if not self._is_scanning:
            print("scan")
            self._is_scanning = True
            self._state_callback(ConnState.scanning)
            self._ble.gap_scan(2000, 30000, 30000)
        #else:
            #print("skip scan")

# Connect to the specified device (otherwise use cached address from a scan).
    def connect(self, conn):
        print("connect() " +  conn._name)
        self._state_callback(ConnState.connecting)
        self._ble.gap_connect(conn._addr_type, conn._addr)
        return True

    # Disconnect from current device.
    def disconnect(self):
        if None == self._conn_handle:
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()

    # Issues an (asynchronous) read, will invoke callback with data.
    def read(self, callback):
        if not self.is_connected():
            return
        self._read_callback = callback
        self._ble.gattc_read(self._conn_handle, self._value_handle)

    # Sets a callback to be invoked when the device notifies us.
    def set_on_notify(self, callback):
        self._notify_callback = callback

    def set_on_state(self, callback):
        self._state_callback = callback

    def _update_value(self, data):
        # Data is sint16 in degrees Celsius with a resolution of 0.01 degrees Celsius.
        print("_update_value")
        for d in data:
            self.print_ble("%d %c" % (d,d))
        #self._value = struct.unpack("<BIHHH", data)
        #self.print_ble(self._value)
        #return self._value

    def value(self):
        return self._value



class BleCscManager:
    def __init__(self):
        self._on_state = None
        self.conn_state = ConnState.disconnected
        self.ble = bluetooth.BLE()
        self.central = BLECscCentral(self.ble)
        self.central.set_on_state(self.on_state)

    def on_state(self, state):
        #print("on_state(%d)" % (state))
        self.conn_state = state
        if self._on_state:
            self._on_state(state)

    def add_connection(self, conn):
        self.central.add_connection(conn)

    def scan(self):
        self.central.scan(callback=None)

    def connect(self):
        print("connect")
        self.central.connect()

    def set_on_notify(self, cb):
        self.central.set_on_notify(callback=cb)

    def set_on_state(self, cb):
        self._on_state = cb

    def reset(self):
        self.central._reset()

    def disconnect(self):
        print("bt disconnect")
        self.central.disconnect()

    def read(self, conn):
        #print(conn._conn_handle)
        #print(conn._value_handle)
        if None != conn._conn_handle and None != conn._value_handle:
            print("read!!!!")
            self.ble.gattc_read(conn._conn_handle, conn._value_handle)

def demo():
    b = BleCscManager()
    while(True):
        b.scan()
        b.loop()
        time.sleep_ms(1000)

if __name__ == "__main__":
    demo()