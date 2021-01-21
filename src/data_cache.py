class DataCache:
    def __init__(self):
        self._items = []
        pass
    
    def changed(self, index, value):
        while len(self._items) <= index:
            self._items.append(None)

        if self._items[index] != value:
            self._items[index] = value
            return True
        else:
            return False
    
    def reset(self):
        for i in range(0, len(self._items)):
            self._items[i] = None

    def reset_val(self, index):
        self._items[index] = None