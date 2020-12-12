from cycle_data import *
import fonts
from const import *
import data_global as g
from helper import *


class GuiBase:
    x_desc = 6
    x_val = 35
    rh = 30
    def __init__(self, main):
        self.main = main

    def show_progress(self, y, h, max, val, marker=-1):
        if val > max:
            val = max
        p = 0
        m = 0
        if max > 0:
            p = (int)(135 / max * val)
            m = (int)(135 / max * marker)
        g.display.fill_rect(0, y, 135, h, Color.grey)
        if p > m:
            g.display.fill_rect(0, y, p, h, Color.green)
            g.display.fill_rect(0, y, m, h, Color.red)
        else:
            g.display.fill_rect(0, y, m, h, Color.red)
            g.display.fill_rect(0, y, p, h, Color.green)
        #if marker > 0:
            #g.display.fill_rect(0, y, m, 5, Color.red)

    #new
    def show_float_speed_old(self, val, x, y, font = fonts.pf_normal, color = Color.white, align = Align.right):
        if val > 999:
            val = 999
        if val < 0:
            val = 0
        ival = (int) (val)
        dval = (int)((val - ival)*10)
        #g.display.fill_rect(x, y, 3*font.WIDTH+10, font.height(), Color.black)
        if val < 100:
            g.display.draw_text(font, "%2d.%d" % (ival, dval), x, y, fg=color, align = align)
        else:
            g.display.draw_text(font, "%3d" % (ival), x + 10, y, fg=color, align = align)

    def show_float_speed(self, val, x, y, font = fonts.pf_normal, color = Color.white, align = Align.right):
        val = limit(val, 0, 999)
        ival = (int) (val)
        dval = (int)((val - ival)*10)
        mw = font.get_width('0')
        if align == Align.left:
            if ival < 10:
                mw *= -1
            elif ival < 100:
                mw *= -2
            else:
                mw *= -3
            mw -= font.get_width('.')
        if val < 100:
            g.display.draw_text(font, "%2d." % (ival), x-mw, y, fg=color, align = Align.right)
            g.display.draw_text(font, "%d" % (dval), x-mw, y, fg=color, align = Align.left)
        else:
            g.display.draw_text(font, "%3d" % (ival), x -mw, y, fg=color, align = Align.right)

    def show_float_time(self, val, x, y, align = Align.right, font = fonts.pf_normal):
        h = (int)(val / 60)
        m = val % 60
        mw = font.get_width('0')
        if align == Align.left:
            if h < 10:
                mw *= -1
            else:
                mw *= -2
            mw -= font.get_width(':')
        else:
            mw *= 2
        g.display.draw_text(font, "%d:" % (h), x-mw, y, align = Align.right)
        g.display.draw_text(font, "%.2d" % (m), x-mw, y, align = Align.left)


    def show_float_time_old(self, val, x, y, align = Align.right):
        h = (int)(val / 60)
        m = val % 60
        font = fonts.pf_normal
        g.display.draw_text(font, "%1d:%.2d" % (h,m), x, y, align = align)


    def show_big_speed(self, val, x, y, color):
        ival = (int) (val)
        dval = (int)((val - ival)*10)
        mw = fonts.pf_normal.get_width('0')
        g.display.draw_text(fonts.pf_huge, " %2d" % (ival), x-mw-3, y, fg=color, bg=Color.black, align=Align.right)
        g.display.draw_text(fonts.pf_normal, "%d" % (dval), x-mw, y, fg=color, bg=Color.black, align=Align.left)






    def show_speed_max(self, data, y):
        if self.cache.changed(6, data.speed_max):
            self.show_float_speed(data.speed_max, g.display.width, y)

    def show_cadence_avg(self, data, y):
        if self.cache.changed(7, data.cadence_avg):
            g.display.draw_text(fonts.pf_normal, "%2d" % (data.cadence_avg), g.display.width, y, align=Align.right)

    def show_desc(self, txt, y):
        g.display.draw_text(fonts.pf_small, txt, 3, y + fonts.pf_normal.height() - fonts.pf_small.height() - 10, align=Align.left)


    def handle(self, event = 0):
        #if self.main.is_kommot_gui_active():
        #    print("komoot")
        
        #print("handler_csc")
        if event == Event.go_main_menu:
            self.main.gui_show_main_menu()
        #elif event == Event.toggle_komoot:
        #    if self.main.is_kommot_gui_active():
        #        self.main.switch_to_next_gui()
        #    else:
        #        self.main.switch_to_prev_gui()
            #self.main.gui_toggle_komoot()
        elif event == Event.go_prev_view:
            self.main.switch_to_prev_gui()
        elif event == Event.go_next_view:
            self.main.switch_to_next_gui()
        elif event == Event.go_next_meter:
            self.main.gui_show_next_meter()

    def clear(self):
        self.main.clear()