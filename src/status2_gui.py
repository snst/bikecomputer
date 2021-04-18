import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class Status2Gui(GuiBase):
    def __init__(self, main):
        GuiBase.__init__(self, main)
        g.hal.gc_collect()

    def get_title(self):
        return b'status2'

    def show(self, redraw):
        self.cache.reset(redraw)
        y = 0
        ys = fonts.f_wide_smaller.height() + 8
        i = 0
        self.show_val(redraw, y + i*ys, "scan", "%d/%d" % (g.bt.stat.cnt_scan_req, g.bt.stat.cnt_scan_res), i, 4)
        i += 1
        self.show_val(redraw, y + i*ys, "conn", "%d/%d" % (g.bt.stat.cnt_connect, g.bt.stat.cnt_disconnect), i, 4)
        i += 1
        self.show_val(redraw, y + i*ys, "read", "%d/%d" % (g.bt.stat.cnt_read_req, g.bt.stat.cnt_read_res), i, 4)
        i += 1
        self.show_val(redraw, y + i*ys, "not", "%d/%d" % (g.bt.stat.cnt_notify_req, g.bt.stat.cnt_notify_res), i, 5)
        i += 1
        self.show_val(redraw, y + i*ys, "c/n", "%d/%d" % (self.cycling.msg_cnt, self.nav.msg_cnt), i, 5)

    def handle(self, event):
        GuiBase.handle(self, event)
