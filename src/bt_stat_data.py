import struct

class BtStatData:
    def __init__(self):
        self.cnt_connect = 0
        self.cnt_disconnect = 0
        self.cnt_scan_req = 0
        self.cnt_scan_res = 0
        self.cnt_read_req = 0
        self.cnt_read_res = 0
        self.cnt_notify_req = 0
        self.cnt_notify_res = 0
