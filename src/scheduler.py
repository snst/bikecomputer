import time

class Scheduler:
    def __init__(self, hal):
        self._hal = hal
        self._tasks = []
        pass

    def insert(self, ms, cb):
        now = self._hal.ticks_ms()
        then = now + ms
        self._tasks.append((then, cb))
        self._tasks.sort(key=lambda tup: tup[0])

    def run(self):
        if len(self._tasks) > 0:
            first = self._tasks[0]
            t = first[0]
            cb = first[1]
            now = self._hal.ticks_ms()
            delta = t - now
            if delta <= 0:
                self._tasks.pop(0)
                cb()
            else:
                if delta > 10:
                    delta = 10
                self._hal.sleep_ms(delta)

        else:
            self._hal.sleep_ms(10)



"""

class Hal:
    def __init__(self):
        pass
    def ticks_ms(self):
        return int(round(time.time() * 1000))      
    def sleep_ms(self, delta):
        time.sleep(delta/1000)

h = Hal()
s = Scheduler(h)

def task1():
    print("task1")
    s.insert(1000, task1)

def task2():
    print("task2")
    s.insert(2000, task2)

s.insert(1, task1)
s.insert(1, task2)
#s.insert(4000, 4000)
#s.insert(2000, 2000)
#s.insert(8000, 8000)
while True:
    s.run()

"""
