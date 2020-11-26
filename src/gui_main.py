from gui_edit_value import *
from cycle_gui import *
from gui_csc_stat import *
from gui_menu import *
from komoot_gui import *
from goal_data import *
from menu_config import *
from goal_data import *
from const import *
import fonts 
import math
import data_global as g
from altimeter_gui import *
from status_gui import *
from item_list import *

class GuiMain(GuiBase):
    def __init__(self, settings, list_csc_data, komoot_data):
        self.callback_repaint = None
        self._settings = settings
        self._cycle_data_list = ItemList(list_csc_data)
        self.komoot_data = komoot_data
        self.active_gui = None
        self.gui_stack = []
        self._gui_list = ItemList()
        self.clear()
        self._gui_index = 1
        self._gui_index_last = 1
        self.add_to_gui_stack(self.create_gui())

    def add_gui_list(self, gui):
        self._gui_list.append(gui)

    def get_csc_data(self):
        return self._cycle_data_list.get()

    def set_callback_repaint(self, cb):
        self.callback_repaint = cb

    def clear(self):
        g.display.fill(Color.black)
        #print("clear")

    def cyclic_update(self):
        #print("update")
        #if isinstance(self.active_gui, CycleGui) or isinstance(self.active_gui, KomootGui):
        if len(self.gui_stack) == 1:
            self.active_gui.show(False)
        self.gui_update_state()
        self.repaint()

    def show(self):
        #print("show")
        self.clear()
        self.active_gui.show(True)
        self.repaint()

    def repaint(self):
        if self.callback_repaint:
            self.callback_repaint()

    def activate_gui(self, gui):
        self.active_gui = gui
        self.show()

    def handle_click(self, btn_id, ev_type):
        event = btn_id | ev_type
        self.active_gui.handle(event)

    def get_breadcrum(self):
        val = ""
        itergui = iter(self.gui_stack)
        next(itergui)
        for g in itergui:
            val = val + ">" + g.get_title()
        return val

    def gui_show_main_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMain()))

    def gui_show_meter_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMeter()))

    def gui_show_komoot_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuKomoot(self._settings)))

    def gui_show_csc_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuCSC(self._settings)))

    def gui_show_goal_menu(self):
        data = self.cycle_data
        if data.goal == None:
            data.goal = GoalData()
            data.goal.load()
        self.add_to_gui_stack(GuiMenu(self, MenuGoal(data.goal)))

    def go_menu_settings(self):
        m = MenuSettings(self._settings)
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
            return KomootGui(self)
        elif i == 1:
            return CycleGui(self)
        elif i == 2:
            return GuiCscStat(self)
        elif i == 3:
            return AltimeterGui(self)
        elif i == 4:
            return StatusGui(self)

    def switch_to_next_gui(self):
        index = (self._gui_index + 1) % 5
        if index == 0:
            index += 1
        self.switch_to_gui(index)

    def switch_to_gui(self, index):
        self._gui_index = index
        gui = self.create_gui()
        self.gui_stack[0] = gui
        self.activate_gui(gui)


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
        n = self._cycle_data_list.count() + 1
        self._cycle_data_list.add(CycleData(n, self._settings))
        self._cycle_data_list.select_last()
        self.gui_stack_pop_all()

    def reset_meter(self):
        #print("reset_meter")
        self.cycle_data.reset()
        self.gui_stack_pop_all()

    def start_goal(self):
        data = self.cycle_data
        data.goal.is_started = True
        data.goal.calculate_progress(data)
        self.gui_stack_pop_all()

    def stop_goal(self):
        self.cycle_data.goal.is_started = False
        self.gui_stack_pop_all()

    def save_settings(self):
        self.gui_stack_pop_all()
        #print("save_settings")
        self._settings.save()

    def ble_reconnect(self):
        g.bt.reconnect_all()
        self.gui_stack_pop_all()

    def save_goal_settings(self):
        self.cycle_data.goal.save()

    def load_goal_settings(self):
        self.cycle_data.goal.load()

    def gui_toggle_komoot(self):
        if 0 == self._gui_index:
            self.switch_to_gui(self._gui_index_last)
        else:
            self._gui_index_last = self._gui_index
            self.switch_to_gui(0)

    @property
    def cycle_data(self):
        return self._cycle_data_list.get()

    def gui_show_next_meter(self):
        self._cycle_data_list.next()
        self.gui_stack_pop_all()

    def gui_show_prev_meter(self):
        self._cycle_data_list.prev()
        self.gui_stack_pop_all()        

    def callback_display_brightness_changed(self, val, closed):
        #print("callback_display_brightness_changed %d" % (val))
        g.hal.set_backlight(val)

    def gui_update_state(self):
        txt = ""
        txt += "S" if g.bt.is_scanning() else " "
        txt += "R" if self.cycle_data.is_riding else "  "
        txt += "C" if g.bt.is_csc_connected() else " "
        txt += "K" if g.bt.is_komoot_connected() else " "

        g.display.draw_text(fonts.pf_small, txt, 50, Display.height - fonts.pf_small.height())
        g.display.draw_text(fonts.pf_small, "%.2f" % (g.hal.read_bat()), 0, Display.height - fonts.pf_small.height())
