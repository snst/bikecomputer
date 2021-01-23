from gui_edit_value import *
from cycle_gui import *
from gui_menu import *
from nav_gui import *
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
from goal_gui import *
from trip_store import *
from data_cache import *

class GuiMain(GuiBase):
    def __init__(self, settings, nav_data, goal_data, cycling, env_data):
        GuiBase.__init__(self, self)
        self._cache = DataCache()
        self._next_trip_id = 1
        self.callback_repaint = None
        self._cycling = cycling
        self._goal_visible = False
        self._settings = settings
        self._gui_index = 1
        self._gui_index_last = 1
        self._max_views = 5
        self._goal_data = goal_data
        self.nav_data = nav_data
        self.env_data = env_data
        self.active_gui = None
        self.gui_stack = []
        self._meter_list = ItemList()
        self.add_trip()
        self.add_to_gui_stack(self.create_gui())

    @property
    def trip_list(self):
        return self._meter_list._list

    def get_trip(self):
        return self._meter_list.get()

    def set_callback_repaint(self, cb):
        self.callback_repaint = cb

    def clear(self):
        g.display.fill(Color.black)
        #print("clear")

    def cyclic_update(self):
        #print("update")
        #if isinstance(self.active_gui, CycleGui) or isinstance(self.active_gui, NavGui):
        if len(self.gui_stack) == 1:
            self.active_gui.show(False)
        if isinstance(self.active_gui, CycleGui) or isinstance(self.active_gui, NavGui):
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
        val = b''
        itergui = iter(self.gui_stack)
        next(itergui)
        t = b''
        for g in itergui:
            t = g.get_title()
            val = val + b'>'# + t
        return val

    def gui_show_main_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMain(self)))

    def gui_show_meter_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMeter(self, self.get_trip())))

    def gui_show_navi_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuNav(self)))

    def gui_show_altimeter_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuAltimeter(self)))

    def gui_show_csc_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuCSC(self)))

    def gui_show_goal_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuGoal(self, g.bc._goal_data)))

    def go_menu_settings(self):
        m = MenuSettings(self)
        m.led_on.set_value_changed_callback(self.callback_display_brightness_changed)
        m.led_off.set_value_changed_callback(self.callback_display_brightness_changed)
        self.add_to_gui_stack(GuiMenu(self, m))

    def gui_stack_pop_all(self):
        while len(self.gui_stack) > 1:
            self.gui_stack.pop()
        if len(self.gui_stack) > 0:
            self.activate_gui(self.gui_stack[0])

    def action_go_edit_setting_value(self, item):
        self.add_to_gui_stack(GuiEditValue(self, item))

    def create_gui(self):
        i = self._gui_index
        gui = None
        if i == 0:
            gui = NavGui(self)
        elif i == 1:
            gui = CycleGui(self)
        elif i == 2:
            gui = GoalGui(self)
        elif i == 3:
            gui = AltimeterGui(self)
        elif i == 4:
            gui = StatusGui(self)
        g.hal.gc_collect()
        return gui

    def switch_to_next_gui(self):
        index = min(self._gui_index + 1, 4)
        #index = (self._gui_index + 1) % self._max_views
        if index == 0 and self._settings.nav_enabled.value == 0: #skip komoot if not enabled
            index += 1
        if not self._goal_visible and index == 2:
            index += 1
        self.switch_to_gui(index)

    def switch_to_prev_gui(self):
        index = (self._gui_index - 1) 
        if not self._goal_visible and index == 2:
            index -= 1
        if self._settings.nav_enabled.value == 1:
            if index < 0:
                index = 1
        elif index < 1:
            index = 1
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

    def add_trip(self):
        id = self._next_trip_id 
        self._next_trip_id += 1
        trip = TripData(id)
        self._meter_list.add(trip)
        self._meter_list.select_last()
        self.gui_stack_pop_all()

    def del_trip(self):
        meter = self._meter_list.get()
        self._meter_list.prev()
        self._meter_list.remove(meter)
        self.gui_stack_pop_all()

    def reset_meter(self, meter):
        meter.reset()
        meter.enable(True)
        self.gui_stack_pop_all()

    def start_meter(self):
        meter = self._meter_list.get()
        meter.enable(True)
        self.gui_stack_pop_all()

    def stop_meter(self):
        meter = self._meter_list.get()
        meter.enable(False)
        self.gui_stack_pop_all()

    def enable_meter(self, meter, enabled):
        meter.enable(enabled)
        self.gui_stack_pop_all()

    def save_settings(self):
        self.gui_stack_pop_all()
        self._settings.save()

    def ble_reconnect(self):
        g.bt.reconnect_all()
        self.gui_stack_pop_all()

    def save_goal_settings(self):
        self._goal_data.save()

    def load_goal_settings(self):
        self._goal_data.load()

    def gui_toggle_komoot(self):
        if 0 == self._gui_index:
            self.switch_to_gui(self._gui_index_last)
        else:
            self._gui_index_last = self._gui_index
            self.switch_to_gui(0)

    def gui_show_next_meter(self):
        if self._meter_list.count() > 1:
            self._meter_list.next()
            self.gui_stack_pop_all()
        else:
            self.add_trip()

    def gui_show_prev_meter(self):
        self._meter_list.prev()
        self.gui_stack_pop_all()        

    def callback_display_brightness_changed(self, val, closed):
        #print("callback_display_brightness_changed %d" % (val))
        g.hal.set_backlight(val)

    def gui_update_state(self):
        h = 4
        w = 10
        g.display.fill_rect(0, g.display.height-h, w-1, h, Color.yellow if g.bt.is_scanning() else Color.black)
        g.display.fill_rect(w, g.display.height-h, w-1, h, Color.green if g.bt.is_csc_connected() else Color.black)
        g.display.fill_rect(2*w, g.display.height-h, w-1, h, Color.green if g.bt.is_nav_connected() else Color.black)

    def is_kommot_gui_active(self):
        return isinstance(self.active_gui, NavGui)

    def show_goal_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuGoal(self, g.bc._goal_data)))

    def show_cycle_menu(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMeter(self, self.get_trip())))

    def show_goal_meter(self, visible):
        self._goal_visible = visible
        self._goal_data.enable(visible)
        self.switch_to_gui(2 if visible else 1)
        self.gui_stack_pop_all()
        
    def enable_navi(self):
        self._settings.nav_enabled.value = 1
        self.gui_stack_pop_all()

    def save_trip(self, trip):
        ts = TripStore()
        ts.save(trip)
        self.gui_stack_pop_all()

    def load_trip(self, trip):
        ts = TripStore()
        ts.load(trip)
        trip.process(self._cycling)
        self.gui_stack_pop_all()
