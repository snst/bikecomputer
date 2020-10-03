

class MenuItem:
    MENU_ITEM = 0
    INT_ITEM = 1
    FLOAT_ITEM = 2
    def __init__(self, name, action):
        self.name = name
        self.action = action
        self.type = self.MENU_ITEM

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
    def __init__(self, name, data):
        MenuItem.__init__(self, name, None)
        self.data = data
        self.type = self.FLOAT_ITEM if data.is_float else self.INT_ITEM
