import st7789
import site
import sys
site.addsitedir('./src')
import const
from sim import *
from bike_computer import *
from hal_emu import *



tft = st7789.ST7789(None, Display.width, Display.height)
hal = Hal_emu(tft)

bc = BikeComputer(tft, hal)

tft.set_gui(bc.gui)

bc.gui.set_callback_repaint(tft.update)

tft.update()

sim = Sim(bc)
sim.start()
hal.register_sim_callback(sim.btn_callback)

hal.mainloop()