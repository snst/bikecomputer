import site
import sys
import matplotlib.pyplot as plt 

site.addsitedir('./src')
site.addsitedir('./modules')

from altimeter import *
import random

#import data3 as s1
import data5 as s2
import data0 as s0
import data0_5 as s0_5
import data1 as s1

def search(s, a, b, e):
    alt_kalman = AltSum(Kalman(a,1,b))

    base_alt = s.alt_list[0]
    sum = 0
    for v in s.alt_list:
        alt_kalman.update(v-base_alt) 

    #print("sum %f  (%f, %f)" % (alt_kalman.sum, a, b))
    delta = abs(alt_kalman.sum - s.goal)
    if delta < e:
        #print("a=%f\nb=%f" % (a,b))
        return delta
    else:
        return None

def test(s):
    while True:
        a = random.uniform(0.01, 0.3)
        b = random.uniform(0.5, 2)
        e = 0.3
        d1 = search(s1, a, b, e)
        if d1 != None:
            d2 = search(s2, a, b, e)
            if d2 != None:
                d3 = abs((d1*3.3)-d2)
                if d3 < 0.26:
                    print("a=%f b=%f, d1=%f, d2=%f, d3=%f" % (a, b, d1, d2, d3))
                #break
    
#test(s1)

def calc_avg(s):
    n = len(s.alt_list)
    sum = 0
    for v in s.alt_list:
        sum += v
    sum /= n
    return sum


#v = calc_avg(s0)
#print("avg %f" % (v))


def ab_filter(s, dt=0.5, a = 0.85, b = 0.005):
	
    xk_1 = 0
    vk_1 = 0
    xk = 0
    vk = 0
    rk = 0
    xm = 0
    avg = 0

    for xm in s.alt_list:

        xk = xk_1 + (vk_1 * dt)
        vk = vk_1

        rk = xm - xk

        xk += a * rk
        vk += (b * rk) / dt

        xk_1 = xk
        vk_1 = vk

        #print("%f \t %f" % (xm, xk_1))
        avg += xk_1
    avg = avg / len(s.alt_list)

    diff = abs(avg-s.avg)
    if diff <= 0.00000001:
        print("%f %f %f calc=%f, goal=%f, diff=%f" % (dt, a, b, avg, s.avg, diff))
    return avg


#avg = ab_filter(s0)    




class ABFilter:
    def __init__(self, init = 0, dt = 0.5, a = 0.85, b = 0.005):
        self._dt = dt
        self._a = a
        self._b = b
        self._xk_1 = init
        self._vk_1 = 0
        self._xk = 0
        self._vk = 0
        self._rk = 0
        self._xm = 0

    def add(self, xm):
        self._xk = self._xk_1 + (self._vk_1 * self._dt)
        self._vk = self._vk_1

        self._rk = xm - self._xk

        self._xk += self._a * self._rk
        self._vk += (self._b * self._rk) / self._dt

        self._xk_1 = self._xk
        self._vk_1 = self._vk

        return self._xk_1


class AltSum:
    def __init__(self, last_val = None):
        self.reset(last_val)

    def reset(self, last_val):
        self._sum = 0
        self._last_val = None

    def add(self, val):
        d = 0.1
        if self._last_val == None:
            self._last_val = val
        else:
            diff = val - self._last_val
            if diff > d:
                self._sum += diff
            if abs(diff) > d:
                self._last_val = val
        
    def show(self):
        print("Alt %f" % (self._sum))


def process_all(s, dt, a, b, max_err=0.002):
    filter = ABFilter(init = s.base, dt=dt, a=a, b=b)
    alt = AltSum()
    n = 0
    for v in s.alt_list:
        f = filter.add(v)
        if n == 10:
            alt.add(f)
            n = 0
        n += 1
    #alt.show()
    err = abs(s.goal - alt._sum)
    if err < max_err:
        print("a=%f, b=%f, sum=%f, err=%f" % (a,b, alt._sum, err))
    return err


#a=0.105768, b=0.029250
def try_ab(s):
    
    while True:
        max_err = 0.08
        dt = 1#random.uniform(0.1, 1)
        a = random.uniform(0.01, 1)
        b = random.uniform(0.001, 0.1)
        e1 = process_all(s0_5, dt=dt, a = a, b = b, max_err=max_err)    
        e2 = process_all(s1, dt=dt, a = a, b = b, max_err=max_err)    
        if e1 <= max_err and e2 <= max_err:
            print("a=%f, b=%f" % (a,b))

#try_ab(s1)

#process_all(s0, dt=1, a=0.105768, b=0.029250, max_err=10) 
class CalcAvg:
    def __init__(self, n):
        self._n = n
        self._values = []
        self._avg = 0
    def add(self, val):
        self._values.append(val)
        if len(self._values) > self._n:
            self._values.pop(0)
        sum = 0
        for v in self._values:
            sum += v
        self._avg = sum / len(self._values)
        #print("avg %f" % (self._avg))
        return self._avg


def it_val(arr):
    avg = CalcAvg(10)
    alt = AltSum()
    k = 0
    x = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    n = 0
    for s in arr.alt_list:
        v = avg.add(s)
        alt.add(v)
        y1.append(s)
        y2.append(v)
        y3.append(418.8+alt._sum)
        y4.append(alt._last_val)

        x.append(n)
        n += 1

        
        if k == 5:
            alt.add(v)
            k = 0
        k += 1

        err = abs(arr.base - v)
        #print("val=%f, err=%f" % (v, err))

    alt.show()
    plt.plot(x, y1, label = "raw") 
    plt.plot(x, y2, label = "smooth")
    plt.plot(x, y3, label = "alt")
    plt.plot(x, y4, label = "last_val")
    plt.legend() 
    plt.show() 




#it_val(s0)
it_val(s0)
#it_val(s1)