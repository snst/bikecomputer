import bike_gui
import bike_data
import display_dim
import csc

class BikeComputer:
    def __init__(self, tft, btn):
        self.btn = btn
        self.tft = tft
        self.data = bike_data.BikeData()
        self.display = display_dim.DisplayDim(self.data.settings)
        self.csc = csc.CSC(self.data)
        self.gui = bike_gui.BikeGUI(self.tft, self.csc, self.data)
        self.btn.set_settings(self.data.settings)
        self.btn.set_display(self.display)
        self.btn.set_click_cb(self.gui.handle_click)
