import st7789
import site
import sys
site.addsitedir('./src')
import btn_handler
import bike_gui
import bike_data
import sim
import bike_settings
import display_dim
import csc


settings = bike_settings.BikeSettings()
goal = bike_settings.GoalSettings()

display = display_dim.DisplayDim(settings)

tft = st7789.ST7789(None, 135, 240)

btn = btn_handler.ButtonHandler(tft, display, settings)

data = bike_data.BikeData()

csc = csc.CSC(data)


gui = bike_gui.BikeGUI(tft, csc, data, settings, goal)

btn.set_click_cb(gui.handle_click)



sim = sim.Sim(data, gui, csc, display)
sim.start()


#tft.line(10,10,20,50, st7789.RED)
#tft.fill_rect(50, 60, 20, 10, st7789.GREEN)
#tft.rect(50, 80, 20, 10, st7789.BLUE)
#tft.pixel(25,25,st7789.YELLOW)
#tft.text(font1, "ABCDEF", 5, 5, color=st7789.GREEN)

#gui.show()

#def cycle():
    #print("cycle")
#    gui.cyclic_update()
#    tft.tk.after(500, cycle)
    

#tft.tk.after(1, cycle)
tft.mainloop()