import st7789
import site
import sys
site.addsitedir('./src')
site.addsitedir('./modules')
import const
from sim import *
from bike_computer import *
from hal_emu import *
from display import *
import data_global as g
from bt_manager_base import *


tft = st7789.ST7789(None, Display.width, Display.height)
g.display = Display(tft)
g.hal = Hal_emu(tft)
g.bt = BtManagerBase()

bc = BikeComputer()

tft.set_gui(bc.gui)

bc.gui.set_callback_repaint(tft.update)

tft.update()

sim = Sim(bc)
sim.start()
g.hal.register_sim_callback(sim.btn_callback)



t = threading.Thread(target=bc.run, args=())
t.start()

g.hal.mainloop()