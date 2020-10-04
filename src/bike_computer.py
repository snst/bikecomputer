from gui_main import *
from data_settings import *
from data_csc import *
import display_dim
import csc

class BikeComputer:
    def __init__(self, tft, btn):
        self.btn = btn
        self.tft = tft
        self.settings = DataSettings()
        self.csc_data = [ DataCsc(1) ]
        #self.data = bike_data.BikeData()
        self.display = display_dim.DisplayDim(self.settings)
        self.csc = csc.CSC(self.settings)
        self.gui = GuiMain(self.tft, self.settings, self.csc_data)
        self.btn.set_settings(self.settings)
        self.btn.set_display(self.display)
        self.btn.set_click_cb(self.gui.handle_click)

    def on_notify(self, raw_data):
        for d in self.csc_data:
            self.csc.process(raw_data, d)
