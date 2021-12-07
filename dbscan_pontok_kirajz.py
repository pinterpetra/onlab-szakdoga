import random
import math
import numpy as np
import matplotlib.pyplot as plt

def RangeQuery(db, distFunc, q, eps):
    n = list()
    for p in db:
        if distFunc(q, p) <= eps:
            n += [p]
    return n

def dbscan(db, distFunc, eps, minPts):
    c = 0
    for p in db:
        if p[1] != None: continue
        n = RangeQuery(db, distFunc, p, eps)
        if len(n) < minPts:
            p[1] = 'NOISE'
            continue
        c = c + 1
        p[1] = 'Cluster#%d' % c
        s = n
        if p in s:
            s.remove(p)
        for q in s:
            if q[1] == 'NOISE':
                q[1] = 'Cluster#%d' % c

            if q[1] != None:
                continue

            q[1] = 'Cluster#%d' % c
            n = RangeQuery(db, distFunc, q, eps)
            if len(n) >= minPts:
                s += n
    return c

def createRandom2dPonit():
    return (random.randint(0, 10000)/1000, random.randint(0, 10000)/1000)

h = 2000

db = [None]*h

x_coords = []
y_coords = []

centers = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

for x in range(h):
    _len = random.random()
    offset = [
        math.cos(2*math.pi*random.random()) * _len,
        math.sin(2*math.pi*random.random()) * _len
    ]

    center = random.choice(centers)
    pos = ( center[0] + offset[0], center[1] + offset[1] )

    x_coords.append(pos[0])
    y_coords.append(pos[1])

    db[x] = [pos, None]

#https://www.calculatorsoup.com/calculators/geometry-plane/distance-two-points.php
def distFunc(p, q):
    return math.sqrt((q[0][0] - p[0][0])*(q[0][0] - p[0][0]) + (q[0][1] - p[0][1])*(q[0][1] - p[0][1]))

c = dbscan(db, distFunc, 0.2, 10)

colors = [1]*h

for x in range(1, c + 1):
    cluster = 'Cluster#%d' % x
    print("%s:" % cluster)
    for idx in range(len(db)):
        y = db[idx]
        if y[1] == cluster:
            colors[idx] = x + 1
            print("  (%f, %f)" % y[0])

plt.scatter(x_coords, y_coords, c=colors)
plt.show()
