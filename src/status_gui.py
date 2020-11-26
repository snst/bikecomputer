import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class StatusGui(GuiBase):

    def __init__(self, main):
        GuiBase.__init__(self, main)
        self.cache = DataCache(8)

    def get_title(self):
        return "status"

    def show(self, redraw_all):
        if redraw_all:
            self.cache.reset()

        g.display.draw_text(fonts.pf_small, "vbat  %.3f" % (g.hal.read_bat()), 0, 10, align=Align.left)

    def handle(self, event):
        GuiBase.handle(self, event)
