

class MenuItem:
    MENU_ITEM = 0
    INT_ITEM = 1
    FLOAT_ITEM = 2
    def __init__(self, name, action):
        self.name = name
        self.action = action
        self.type = self.MENU_ITEM

class MenuValueItem(MenuItem):
    def __init__(self, name, data, cb = None):
        MenuItem.__init__(self, name, None)
        self.data = data
        self.type = self.FLOAT_ITEM if data.is_float else self.INT_ITEM
        self.callback_changed = cb

    def set_value_changed_callback(self, cb):
        self.callback_changed = cb
