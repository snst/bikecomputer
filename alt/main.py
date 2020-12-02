import site
import sys
site.addsitedir('./src')
site.addsitedir('./modules')

from altimeter import *
import random

import data3 as s1
import data5 as s2


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
    
test(s1)