class DataCache:
    def __init__(self, n):
        self._items = [None] * n
    
    def changed(self, index, value):
        if self._items[index] != value:
            self._items[index] = value
            return True
        else:
            return False
    
    def reset(self):
        for i in range(0, len(self._items)):
            self._items[i] = None