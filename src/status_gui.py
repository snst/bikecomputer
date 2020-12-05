import fonts
import const
from gui_base import *
from display import *
import data_global as g
from data_cache import *


class StatusGui(GuiBase):

    def __init__(self, main):
        GuiBase.__init__(self, main)
        g.bc.request_sensor_bat()
        g.bc.request_computer_bat()

    def get_title(self):
        return "status"

    def show(self, redraw_all):
        g.display.draw_text(fonts.pf_small, "bat  %.3f V" % (g.bc.computer_bat), 0, 10, align=Align.left)
        g.display.draw_text(fonts.pf_small, "csc bat  %d %%" % (g.bc.sensor_bat), 0, 40, align=Align.left)

    def handle(self, event):
        GuiBase.handle(self, event)
