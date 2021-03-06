class ItemList:
    def __init__(self, init_list = []):
        self._list = init_list
        self._index = 0

    def add(self, item):
        self._list.append(item)

    def get(self):
        return self._list[self._index]

    def next(self):
        self._index = (self._index + 1) % self.count()
        return self.get()

    def prev(self):
        cnt = self.count()
        self._index = (self._index + cnt - 1) % cnt
        return self.get()

    def count(self):
        return len(self._list)

    def select_last(self):
        self._index = self.count() - 1
        return self.get()

    def remove(self, item):
        self._list.remove(item)