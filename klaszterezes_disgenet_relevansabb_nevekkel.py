from hdt import HDTDocument
import numpy as np
import re

LIMIT = 10000
document = HDTDocument("disgenet.hdt")

#elmentjuk az entitasokat es propertyket egy-egy halmazba, hogy biztos egyediek legyenek
entities_ = set()
properties_ = set()

(triples, cardinality) = document.search_triples("", "", "", limit = LIMIT)
for s, p, o in triples:
    #print(s, o, p)
    entities_.add(s)
    if (o.find("http", 0, 5) != -1): 
        entities_.add(o)
    properties_.add(p)

#print(properties_)
#print(entities_)
#exit()

h = len(entities_)
w = len(properties_) * 2  #az elso lesz a kifele mutato
w_half = len(properties_)

#a halamzok elemeit ezekbe a tombokbe pakoljuk at, hogy indexelheto lehessen
entities = np.empty(h, dtype = "S200")
properties = np.empty(w_half, dtype = "S200")

for i in range(h):
    entities[i] = entities_.pop()
for i in range(w_half):
    properties[i] = properties_.pop()
    
matrix = np.zeros((h, w), dtype=bool)

i, j = 0, 0
for i in range(h):
    for j in range(w):
        matrix[i][j] = 0

helper = np.empty(1, dtype = "S200")
(triples, cardinality) = document.search_triples("", "", "", limit = LIMIT)
for s, p, o in triples:
    helper[0] = s
    idx_s = np.where(entities == helper[0])
    helper[0] = p
    idx_p = np.where(properties == helper[0])
    helper[0] = o
    idx_o = np.where(entities == helper[0])
    matrix[idx_s[0][0]][idx_p[0][0]] = 1
    if (idx_o[0].size != 0):
        matrix[idx_o[0][0]][idx_p[0][0] + 1] = 1

"""
k, l = 0, 0
for k in range(h):
    for l in range(w):
        print(1 if matrix[k][l] else 0, end =" ")
    print("")
"""

simMatrix = np.zeros((h, h), dtype=float)

for k1 in range(h):
    for k2 in range(h):
        if k1 == k2: continue    
        intersect = 0
        for l in range(w):
            if matrix[k1][l] == matrix[k2][l]:
                intersect += 1
        similarity = intersect/w
        simMatrix[k1][k2] = similarity
        #print(k1, k2, similarity)

"""
for k in range(h):
    for l in range(h):
        print("%.2f" % simMatrix[k][l], end =" ")
    print("")
"""

sortedEntities = list()
for k in range(h):
    _max = np.amax(simMatrix[k])
    sortedEntities.append((k, _max))

sortedEntities.sort(key=lambda x: x[1], reverse=True)
#print(sortedEntities)

max_diff = 0
for k in range(1, len(sortedEntities)):
    e1 = sortedEntities[k-1]
    e2 = sortedEntities[k]
    diff = e1[1] - e2[1]
    if diff > max_diff: 
        max_diff = diff
        diff_entity = e2

print(max_diff, diff_entity)

"""
typeProfile = np.zeros(w, dtype=float)
for j in range(w):
    count = 0
    for i in range(h):
        count += 1 if matrix[i][j] else 0
    print(count, h, count/h)
    typeProfile[j] = count/h
print(typeProfile)
"""

"""
MinPts = 1
setOfTypeProfile = set()
classOfType = 0
for j in range(w):
    setOfNeighbor = set() #todo
    if len(setOfNeighbor) >= MinPts:
        classOfType += 1
        #setOfTypeProfile 
        """


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
            p[1] = -1
            continue
        c = c + 1
        p[1] = c
        s = n
        if p in s:
            s.remove(p)
        for q in s:
            if q[1] == -1:
                q[1] = c

            if q[1] != None:
                continue

            q[1] = c
            n = RangeQuery(db, distFunc, q, eps)
            if len(n) >= minPts:
                s += n
    return c

db = [None]*h

for x in range(h):
    db[x] = [matrix[x], None]

def distFunc(p, q):
    c = 0
    for i in range(w):
        if p[0][i] == q[0][i]:
            c += 1
    """print(c/w)"""
    return 1 - c / w

numClusters = dbscan(db, distFunc, max_diff, 1)

REPLACE_NONWORD = re.compile(r"[^\w]+", re.MULTILINE)

def printCluster(cluster):
    scores = {}
    print("%s:" % cluster)

    for x in range(len(db)):
        if db[x][1] != cluster:
            continue

        name = entities[x].decode('utf-8')
        print("  %s" % name)
        e = re.sub(REPLACE_NONWORD, '/', name).lower().split('/')

        if e[0].startswith('http'):
            e = e[2:]

        for y in e:
            if len(y) < 4: continue
            if not y in scores:
                scores[y] = 0
            scores[y] += 1

    relevantNames = []
    maxCount = 0

    for name, count in scores.items():
        if count == maxCount:
            relevantNames.append(name)
        elif count > maxCount:
            relevantNames = [name]
            maxCount = count

    #print(scores)

    print("  -> fancy name: %d?%s" % (idx, "_".join(relevantNames)))

for idx in range(1, numClusters):
    printCluster(idx)

#for i in range(h):
#    print("entity %d, %s: %s" %(i, entities[i], db[i][1]))

