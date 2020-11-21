from gui_edit_value import *
from gui_csc import *
from gui_csc_stat import *
from gui_menu import *
from gui_komoot import *
from data_goal import *
from menu_config import *
from data_goal import *
from const import *
import fonts 
import math
import data_global as g
from gui_altitude import *
from item_list import *

class GuiMain(GuiBase):
    def __init__(self, settings, list_csc_data, komoot_data):
        self.callback_repaint = None
        self.settings = settings
        self._list_csc_data = list_csc_data
        self._komoot_data = komoot_data
        self.active_gui = None
        self.gui_stack = []
        self._gui_list = ItemList()
        self.clear()
        #self._gui_komoot = GuiKomoot(self)
        #self._gui_csc = GuiCsc(self)
        #self._gui_csc_stat = GuiCscStat(self)
        #self._gui_alt = GuiAltitude(self)
        #self.add_to_gui_stack(self._gui_csc)

        #self._gui_list.add(self._gui_csc)
        #self._gui_list.add(self._gui_csc_stat)
        #self._gui_list.add(self._gui_alt)
        self._gui_index = 0
        self.add_to_gui_stack(self.create_gui())
        pass

    def add_gui_list(self, gui):
        self._gui_list.append(gui)

    def get_csc_data(self):
        return self._list_csc_data.get()

    def set_callback_repaint(self, cb):
        self.callback_repaint = cb

    def clear(self):
        g.display.fill(Color.black)
        #print("clear")

    def cyclic_update(self):
        #print("update")
        #if isinstance(self.active_gui, GuiCsc) or isinstance(self.active_gui, GuiKomoot):
        if len(self.gui_stack) == 1:
            self.active_gui.show(False)
            self.repaint()
        self.gui_update_state()

    def show(self):
        #print("show")
        self.clear()
        self.active_gui.show(True)
        self.repaint()

    def repaint(self):
        if self.callback_repaint:
            self.callback_repaint()
        #self.tft.update()
        #self.gui_update_state()
        pass

    def activate_gui(self, gui):
        self.active_gui = gui
        self.show()

    def handle_click(self, id, long_click):
        event = id | (Button.long if long_click else Button.short)
        self.active_gui.handle(event)

    def get_breadcrum(self):
        val = ""
        itergui = iter(self.gui_stack)
        next(itergui)
        for g in itergui:
            val = val + ">" + g.get_title()
        #if len(self.gui_stack) > 1:
         #   gui = self.gui_stack[-1]
          #  val = gui.breadcrum + ">" + gui.title
        return val

    def gui_show_main_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMain()))

    def gui_show_meter_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMeter()))

    def gui_show_goal_menu(self):
        csc_data = self.get_csc_data()
        if csc_data.goal == None:
            csc_data.goal = DataGoal()
            csc_data.goal.load()
        self.add_to_gui_stack(GuiMenu(self, MenuGoal(csc_data.goal)))

    def go_menu_settings(self):
        m = MenuSettings(self.settings)
        m.led_on.set_value_changed_callback(self.callback_display_brightness_changed)
        m.led_off.set_value_changed_callback(self.callback_display_brightness_changed)
        self.add_to_gui_stack(GuiMenu(self, m))

    def gui_stack_pop_all(self):
        while len(self.gui_stack) > 1:
            self.gui_stack.pop()
        self.activate_gui(self.gui_stack[0])

    def action_go_edit_setting_value(self, item):
        self.add_to_gui_stack(GuiEditValue(self, item))

    def gui_next_old(self):
        gui = self._gui_list.next()
        self.gui_stack[0] = gui
        self.activate_gui(gui)

    def create_gui(self):
        i = self._gui_index
        if i == 0:
            return GuiCsc(self)
        elif i == 1:
            return GuiCscStat(self)
        elif i == 2:
            return GuiAltitude(self)

    def gui_next(self):
        self._gui_index = (self._gui_index + 1) % 3
        gui = self.create_gui()
        self.gui_stack[0] = gui
        self.activate_gui(gui)
        pass


    def gui_stack_pop(self):
        self.gui_stack.pop()
        self.activate_gui(self.gui_stack[-1])

    def add_to_gui_stack(self, gui):
        self.gui_stack.append(gui)
        self.activate_gui(gui)

    def do_action(self, action):
        #print("do action:" + action)
        getattr(self, action)()

    def add_meter(self):
        #print("add_meter")
        n = self._list_csc_data.count() + 1
        self._list_csc_data.add(DataCsc(n))
        self._list_csc_data.select_last()
        self.gui_stack_pop_all()

    def reset_meter(self):
        #print("reset_meter")
        self.get_csc_data().reset()
        self.gui_stack_pop_all()

    def start_goal(self):
        csc_data = self.get_csc_data()
        csc_data.goal.is_started = True
        csc_data.goal.calculate_progress(csc_data)
        self.gui_stack_pop_all()

    def stop_goal(self):
        csc_data = self.get_csc_data()
        csc_data.goal.is_started = False
        self.gui_stack_pop_all()

    def save_settings(self):
        self.gui_stack_pop_all()
        #print("save_settings")
        self.settings.save()

    def ble_reconnect(self):
        g.bt.reconnect_all()
        self.gui_stack_pop_all()

    def save_goal_settings(self):
        self.get_csc_data().goal.save()

    def load_goal_settings(self):
        self.get_csc_data().goal.load()

    def gui_show_komoot(self):
        self.add_to_gui_stack(GuiKomoot(self))

    def get_csc_data(self):
        return self._list_csc_data.get()

    def gui_show_next_meter(self):
        self._list_csc_data.next()
        self.gui_stack_pop_all()

    def gui_show_prev_meter(self):
        self._list_csc_data.prev()
        self.gui_stack_pop_all()        

    def callback_display_brightness_changed(self, val, closed):
        #print("callback_display_brightness_changed %d" % (val))
        g.hal.set_backlight(val)

    def gui_update_state(self):
        txt = ""
        txt += "S" if g.bt.is_scanning() else " "
        txt += "R" if self.get_csc_data().is_riding else "  "
        txt += "C" if g.bt.is_csc_connected() else " "
        txt += "K" if g.bt.is_komoot_connected() else " "

        g.display.draw_text(fonts.pf_small, txt, 50, Display.height - fonts.pf_small.height())
        g.display.draw_text(fonts.pf_small, "%.2f" % (g.hal.read_bat()), 0, Display.height - fonts.pf_small.height())

    def get_komoot_data(self):
        return self._komoot_data