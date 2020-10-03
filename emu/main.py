import st7789
import site
import sys
site.addsitedir('./src')
import btn_handler
import sim
import bike_computer


tft = st7789.ST7789(None, 135, 240)

btn = btn_handler.ButtonHandler(tft)

bc = bike_computer.BikeComputer(tft, btn)


sim = sim.Sim(bc)
sim.start()

tft.mainloop()