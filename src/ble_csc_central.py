import bluetooth
import random
import struct
import time
import micropython

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


class BLECscCentral:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
#        self._ble.irq(handler=self._irq)
        self._ble.irq(self._irq)

        self._reset()

    def _reset(self):
        # Cached name and address from a successful scan.
        self._name = None
        self._addr_type = None
        self._addr = None

        # Cached value (if we have one)
        self._value = None

        # Callbacks for completion of various operations.
        # These reset back to None after being invoked.
        self._scan_callback = None
        self._conn_callback = None
        self._read_callback = None

        # Persistent callback for when new data is notified from the device.
        self._notify_callback = None

        # Connected device.
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._value_handle = None
        self._dsc_handle = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            #print("FD\n")
            #print(decode_name(adv_data))
            #print(addr)
            #if adv_type in (_ADV_IND, _ADV_DIRECT_IND) and _ENV_SENSE_UUID in decode_services(
            #    adv_data
            #):
            if addr == _CSC_ADDR:
                # Found a potential device, remember it and stop scanning.
                self._addr_type = addr_type
                self._addr = bytes(
                    addr
                )  # Note: addr buffer is owned by caller so need to copy it.
                self._name = decode_name(adv_data) or "?"
                self._ble.gap_scan(None)

        elif event == _IRQ_SCAN_DONE:
            if self._scan_callback:
                if self._addr:
                    # Found a device during the scan (and the scan was explicitly stopped).
                    self._scan_callback(self._addr_type, self._addr, self._name)
                    self._scan_callback = None
                else:
                    # Scan timed out.
                    self._scan_callback(None, None, None)

        elif event == _IRQ_PERIPHERAL_CONNECT:
            # Connect successful.
            print("_IRQ_PERIPHERAL_CONNECT")
            conn_handle, addr_type, addr = data
            if addr_type == self._addr_type and addr == self._addr:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(self._conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # Disconnect (either initiated by us or the remote end).
            print("_IRQ_PERIPHERAL_DISCONNECT")
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                # If it was initiated by us, it'll already be reset.
                self._reset()

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            # Connected device returned a service.
            conn_handle, start_handle, end_handle, uuid = data
            print("_IRQ_GATTC_SERVICE_RESULT")
            print(uuid)
            if conn_handle == self._conn_handle and uuid == _CSC_SERVICE_UUID:
                self._start_handle, self._end_handle = start_handle, end_handle

        elif event == _IRQ_GATTC_SERVICE_DONE:
            # Service query complete.
            print("_IRQ_GATTC_SERVICE_DONE")
            if self._start_handle and self._end_handle:
                self._ble.gattc_discover_characteristics(
                    self._conn_handle, self._start_handle, self._end_handle
                )
            else:
                print("Failed to find csc service.")

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            print("_IRQ_GATTC_CHARACTERISTIC_RESULT")
            print(data)
            # Connected device returned a characteristic.
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle and uuid == _CSC_MEASUREMENT_UUID:
                self._value_handle = value_handle

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            print("_IRQ_GATTC_CHARACTERISTIC_DONE")
            # Characteristic query complete.
            if self._value_handle:
                # We've finished connecting and discovering device, fire the connect callback.
                if self._conn_callback:
                    self._conn_callback()

                print("w1")
                #self._ble.gattc_write(self._conn_handle, self._value_handle, struct.pack("<H", int(1)))
                self._ble.gattc_discover_descriptors(
                    self._conn_handle, self._start_handle, self._end_handle
                )

                print("w2")
            else:
                print("Failed to find csc characteristic.")

        elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
            # Called for each descriptor found by gattc_discover_descriptors().
            conn_handle, dsc_handle, uuid = data
            print("_IRQ_GATTC_DESCRIPTOR_RESULT")
            print(data)
            if conn_handle == self._conn_handle and uuid == _CSC_DESC_UUID:
                self._dsc_handle = dsc_handle
        elif event == _IRQ_GATTC_DESCRIPTOR_DONE:
             # Called once service discovery is complete.
             # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            print("_IRQ_GATTC_DESCRIPTOR_DONE")
            self._ble.gattc_write(self._conn_handle, self._dsc_handle, struct.pack("<H", int(1)))
        elif event == _IRQ_GATTC_READ_RESULT:
            # A read completed successfully.
            print("_IRQ_GATTC_READ_RESULT")
            conn_handle, value_handle, char_data = data
            if conn_handle == self._conn_handle and value_handle == self._value_handle:
                self._update_value(char_data)
                if self._read_callback:
                    self._read_callback(self._value)
                    self._read_callback = None

        elif event == _IRQ_GATTC_READ_DONE:
            # Read completed (no-op).
            conn_handle, value_handle, status = data

        elif event == _IRQ_GATTC_NOTIFY:
            #print("_IRQ_GATTC_NOTIFY")
            # The ble_temperature.py demo periodically notifies its value.
            conn_handle, value_handle, notify_data = data
            if conn_handle == self._conn_handle and value_handle == self._value_handle:
                #self._update_value(notify_data)
                if self._notify_callback:
                    self._notify_callback(notify_data)

    # Returns true if we've successfully connected and discovered characteristics.
    def is_connected(self):
        return self._conn_handle is not None and self._value_handle is not None

    # Find a device advertising the environmental sensor service.
    def scan(self, callback=None):
        self._addr_type = None
        self._addr = None
        self._scan_callback = callback
        self._ble.gap_scan(2000, 30000, 30000)

    # Connect to the specified device (otherwise use cached address from a scan).
    def connect(self, addr_type=None, addr=None, callback=None):
        self._addr_type = addr_type or self._addr_type
        self._addr = addr or self._addr
        self._conn_callback = callback
        if self._addr_type is None or self._addr is None:
            return False
        self._ble.gap_connect(self._addr_type, self._addr)
        return True

    # Disconnect from current device.
    def disconnect(self):
        if not self._conn_handle:
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
    def on_notify(self, callback):
        self._notify_callback = callback

    def _update_value(self, data):
        # Data is sint16 in degrees Celsius with a resolution of 0.01 degrees Celsius.
        print(data)
        self._value = struct.unpack("<BIHHH", data)
        print(self._value)
        return self._value

    def value(self):
        return self._value



class BleCscManager:
    def __init__(self):
        print("b1")
        self.ble = bluetooth.BLE()
        print("b2")
        self.central = BLECscCentral(self.ble)
        print("b3")
        self.central.on_notify(callback=self.on_notify)
        self.on_info = None

    def show_info(self, txt):
        if self.on_info:
            self.on_info(txt)

    def on_scan(self, addr_type, addr, name):
        if addr_type is not None:
            print("Found csc sensor:", addr_type, addr, name)
            self.central.connect()
        else:
            #nonlocal not_found
            self.not_found = True
            self.show_info("No sensor")

    def on_notify(self, data):
        print("on_notify")

    def scan(self):
        self.not_found = False
        self.show_info("Scanning ")
        self.central.scan(callback=self.on_scan)


    def loop(self):
        while not self.central.is_connected():
            time.sleep_ms(100)
            if self.not_found:
                return
                

        self.show_info("Connected")
        #while self.central.is_connected():
        #    time.sleep_ms(2000)

        #self.show_info("Disconnected")

    def is_connected(self):
        ret = self.central.is_connected()
        if not ret:
            self.show_info("Disconnected")
        return ret

    def set_callback_notify(self, cb):
        self.central.on_notify(callback=cb)

    def set_callback_info(self, cb):
        self.on_info = cb

def demo():
    b = BleCscManager()
    while(True):
        b.scan()
        b.loop()
        time.sleep_ms(1000)

if __name__ == "__main__":
    demo()