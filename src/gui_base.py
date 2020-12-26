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

    def show_float_speed(self, val, x, y, font = fonts.f_wide_normal, color = Color.white, align = Align.right, short = False):
        val = limit(val, 0, 999)
        ival = (int) (val)
        dval = (int)((val - ival)*10)
        mw = fonts.f_wide_smaller.get_width('0')
        if not short or ival < 100:
            g.display.draw_text(fonts.f_wide_normal, "%2d" % (ival), x-mw, y, fg=color, align = Align.right)
            g.display.draw_text(fonts.f_wide_smaller, "%d" % (dval), x-mw, y, fg=color, align = Align.left)
        else:
            g.display.draw_text(fonts.f_wide_normal, "%3d" % (ival), x, y, fg=color, align = Align.right)

    def show_float_time(self, val, x, y, align = Align.right, font = fonts.f_wide_normal):
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
        g.display.draw_text(font, "%d:" % (h), x-mw, y, align = Align.right, htrim=True)
        g.display.draw_text(font, "%.2d" % (m), x-mw, y, align = Align.left, htrim=True)

    def show_float_time_old(self, val, x, y, align = Align.right):
        h = (int)(val / 60)
        m = val % 60
        font = fonts.f_wide_normal
        g.display.draw_text(font, "%1d:%.2d" % (h,m), x, y, align = align)

    def show_big_speed(self, val, x, y, color=Color.white):
        ival = (int) (val)
        dval = (int)((val - ival)*10)
        mw = fonts.f_wide_normal.get_width(b'0')
        g.display.draw_text(fonts.f_wide_big, " %2d" % (ival), x-mw+2, y, fg=color, bg=Color.black, align=Align.right)
        g.display.draw_text(fonts.f_wide_normal, "%d" % (dval), x-mw, y, fg=color, bg=Color.black, align=Align.left)

    def show_speed_max(self, data, y):
        if self.cache.changed(6, data.speed_max):
            self.show_float_speed(data.speed_max, g.display.width, y)

    def show_cadence_avg(self, data, y):
        if self.cache.changed(7, data.cadence_avg):
            g.display.draw_text(fonts.f_wide_normal, "%2d" % (data.cadence_avg), g.display.width, y, align=Align.right)

    def show_desc(self, txt, y):
        g.display.draw_text(fonts.f_narrow_small, txt, 3, y + fonts.f_wide_normal.height() - fonts.f_narrow_small.height(), align=Align.left)


    def show_icon(self, icon, y):
        g.display.bitmap_blit(0, y + 14, icon)


    def handle(self, event = 0):
        if event == Event.go_main_menu:
            self.main.gui_show_main_menu()
        elif event == Event.go_prev_view:
            self.main.switch_to_prev_gui()
        elif event == Event.go_next_view:
            self.main.switch_to_next_gui()
        elif event == Event.go_next_meter:
            self.main.gui_show_next_meter()

    def clear(self):
        self.main.clear()