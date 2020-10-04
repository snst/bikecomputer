from gui_edit_value import *
from gui_csc import *
from gui_menu import *
from menu_config import *
import const

class GuiMain:


    def __init__(self, tft, settings, csc_data):
        self.tft = tft
        self.settings = settings
        self.csc_data = csc_data
        self.csc_index = 0
        self.active_gui = None
        self.gui_stack = []
        self.clear()
        self.add_to_gui_stack(GuiCsc(self))

        pass


    def clear(self):
        self.tft.fill(Color.black)


    def cyclic_update(self):
        #print("update")
        if isinstance(self.active_gui, GuiCsc):
            self.active_gui.show(False)
            self.repaint()


    def show(self):
        #print("show")
        self.clear()
        self.active_gui.show(True)
        self.repaint()

    def repaint(self):
        self.tft.update()

    def activate_gui(self, gui):
        self.active_gui = gui
        self.show()

    def handle_click(self, id, long_click):
        self.active_gui.handle(id, long_click)

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

    def go_menu_main(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMain()))

    def go_menu_meter(self):
        self.add_to_gui_stack(GuiMenu(self, MenuMeter()))

    def go_menu_goal(self):
        self.add_to_gui_stack(GuiMenu(self, MenuGoal(self.data.goal)))

    def go_menu_settings(self):
        self.add_to_gui_stack(GuiMenu(self, MenuSettings(self.settings)))


    def action_go_csc(self):
        while len(self.gui_stack) > 1:
            self.gui_stack.pop()
        self.activate_gui(self.gui_stack[0])

    def action_go_edit_setting_value(self, item):
        self.add_to_gui_stack(GuiEditValue(self, item))

    def action_go_back(self):
        self.gui_stack.pop()
        self.activate_gui(self.gui_stack[-1])

    def add_to_gui_stack(self, gui):
        self.gui_stack.append(gui)
        self.activate_gui(gui)

    def do_action(self, action):
        print("do action:" + action)
        getattr(self, action)()

    def do_add_meter(self):
        print("do_add_meter")
        n = len(self.csc_data) + 1
        self.csc_data.append(DataCsc(n))
        self.csc_index = n - 1
        self.action_go_csc()

    def do_reset_meter(self):
        print("do_reset_meter")
        self.get_csc_data().reset()
        self.action_go_csc()

    def do_start_goal(self):
        self.action_go_csc()
        print("START GOAL!")

    def do_save_settings(self):
        self.action_go_csc()
        print("do_save_settings")

    def get_csc_data(self):
        return self.csc_data[self.csc_index]

    def next_csc(self):
        self.csc_index = (self.csc_index + 1) % len(self.csc_data)
        self.action_go_csc()

    def prev_csc(self):
        self.csc_index = (self.csc_index + len(self.csc_data) - 1) % len(self.csc_data)
        self.action_go_csc()        
