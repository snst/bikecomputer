class MenuIem:
    def __init__(self, name, action):
        self.name = name
        self.action = action


class MenuMain:
    def __init__(self):
        self.title = "Menu"
        self.items = [ MenuIem("Settings", "go_menu_settings"),
                       MenuIem("Reset", "go_menu_reset"),
                       MenuIem("Goal", "go_menu_goal")
        ]
        pass


class MenuReset:
    def __init__(self):
        self.title = "Reset"
        self.items = [ MenuIem("Trip", "do_reset_trip"),
                       MenuIem("Max", "do_reset_max"),
                       MenuIem("Avg", "do_reset_avg"),
        ]
        pass    