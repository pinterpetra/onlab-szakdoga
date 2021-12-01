import random

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

h = 20

db = [None]*h

for x in range(h):
    db[x] = [random.randint(0, 10000)/1000, None]

def distFunc(p, q):
    return abs(p[0] - q[0])

c = dbscan(db, distFunc, 0.5, 1)

for x in range(1, c):
    cluster = 'Cluster#%d' % x
    print("%s:" % cluster)
    for y in db:
        if y[1] == cluster:
            print("  %f" % y[0])
    
#print(db)
