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
from bt_manager_emu import *
from altimeter_emu import *
from scheduler import *



tft = st7789.ST7789(None, Display.width, Display.height)
g.display = Display(tft)
g.hal = Hal_emu(tft)
g.scheduler = Scheduler(g.hal)
g.bt = BtManagerEmu()

g.altimeter = Altimeter_emu()

g.bc = BikeComputer()

tft.set_gui(g.bc.gui)

g.bc.gui.set_callback_repaint(tft.update)

tft.update()

sim = Sim(g.bc)
sim.start()
g.hal.register_sim_callback(sim.btn_callback)
g.bc.start()

def main_loop():
    while(True):
        try:
            g.scheduler.run()
        except OSError as exc:
            print("OSError %d" % exc.args[0])

t = threading.Thread(target=main_loop, args=())
t.start()

g.hal.mainloop()