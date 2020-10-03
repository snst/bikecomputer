import bike_data
import gui_edit_value
import gui_csc
import gui_menu
import menu_config

class BikeGUI:

    color_val = (0xFFFF)
    color_black = (0x0000)
    rh = 40

    def __init__(self, tft, csc, data):
        self.csc = csc
        self.tft = tft
        self.data = data
        self.active_gui = None
        self.gui_stack = []
        self.clear()
        self.add_to_gui_stack(gui_csc.GuiCsc(self))
        pass


    def clear(self):
        self.tft.fill(self.color_black)


    def cyclic_update(self):
        #print("update")
        if isinstance(self.active_gui, gui_csc.GuiCsc):
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
        self.add_to_gui_stack(gui_menu.GuiMenu(self, menu_config.MenuMain()))

    def go_menu_reset(self):
        self.add_to_gui_stack(gui_menu.GuiMenu(self, menu_config.MenuReset()))

    def go_menu_goal(self):
        self.add_to_gui_stack(gui_menu.GuiMenu(self, menu_config.MenuGoal(self.data.goal)))

    def go_menu_settings(self):
        self.add_to_gui_stack(gui_menu.GuiMenu(self, menu_config.MenuSettings(self.data.settings)))


    def action_go_csc(self):
        while len(self.gui_stack) > 1:
            self.gui_stack.pop()
        self.activate_gui(self.gui_stack[0])
        self.clear()

    def action_go_edit_setting_value(self, item):
        self.add_to_gui_stack(gui_edit_value.GuiEditValue(self, item))

    def action_go_back(self):
        self.gui_stack.pop()
        self.activate_gui(self.gui_stack[-1])

    def add_to_gui_stack(self, gui):
        self.gui_stack.append(gui)
        self.activate_gui(gui)

    def do_action(self, action):
        print("do action:" + action)
        getattr(self, action)()

    def do_reset_trip(self):
        print("do_reset_trip")
        self.csc.reset_trip()
        self.csc.reset_avg_cadence()
        self.csc.reset_avg_speed()
        self.csc.reset_max_speed()
        self.action_go_csc()

    def do_reset_max(self):
        print("do_reset_max")
        self.csc.reset_max_speed()
        self.action_go_csc()

    def do_reset_avg(self):
        print("do_reset_avg")
        self.csc.reset_avg_cadence()
        self.csc.reset_avg_speed()
        self.action_go_csc()

    def do_start_goal(self):
        self.action_go_csc()
        print("START GOAL!")

    def do_save_settings(self):
        self.action_go_csc()
        print("do_save_settings")