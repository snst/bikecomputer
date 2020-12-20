

class MenuItem:
    MENU_ITEM = 0
    INT_ITEM = 1
    FLOAT_ITEM = 2
    LAMBDA_ITEM = 3
    def __init__(self, name, action):
        self.name = name
        self.action = action
        self.type = self.MENU_ITEM

class LambdaMenuItem(MenuItem):
    def __init__(self, name, action):
        MenuItem.__init__(self, name, action)
        self.type = self.LAMBDA_ITEM

class IntMenuItem(MenuItem):
    def __init__(self, name, default, min, max):
        MenuItem.__init__(self, name, None)
        self.type = self.INT_ITEM
        self.value = default
        self.min = min
        self.max = max

class FloatMenuItem(IntMenuItem):
    def __init__(self, name, default, min, max):
        IntMenuItem.__init__(self, name, default, min, max)
        self.type = self.FLOAT_ITEM

class MenuValueItem(MenuItem):
    def __init__(self, name, data, cb = None):
        MenuItem.__init__(self, name, None)
        self.data = data
        self.type = self.FLOAT_ITEM if data.is_float else self.INT_ITEM
        self.callback_changed = cb

    def set_value_changed_callback(self, cb):
        self.callback_changed = cb
