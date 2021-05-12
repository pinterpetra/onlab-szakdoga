from hdt import HDTDocument
import numpy as np

document = HDTDocument("disgenet.hdt")

#elmentjuk az entitasokat es propertyket egy-egy halmazba, hogy biztos egyediek legyenek
entities_ = set()
properties_ = set()

(triples, cardinality) = document.search_triples("", "", "", limit = 5)
for s, p, o in triples:
    entities_.add(s)
    if (o.find("http", 0, 5) != -1): 
        entities_.add(o)
    properties_.add(p)

h = len(entities_)
w = len(properties_) * 2  #az elso lesz a kifele mutato
w_half = len(properties_)

#a halamzok elemeit ezekbe a tombokbe pakoljuk at, hogy indexelheto lehessen
entities = np.empty(h, dtype = "S200")
properties = np.empty(w_half, dtype = "S200")

for i in range(h):
    entities[i] = entities_.pop()
    print(entities[i])

print("----------")

for i in range(w_half):
    properties[i] = properties_.pop()
    print(properties[i])
    
matrix = np.zeros((h, w), dtype=bool)

i, j = 0, 0
for i in range(h):
    for j in range(w):
        matrix[i][j] = 0

helper = np.empty(1, dtype = "S200")
(triples, cardinality) = document.search_triples("", "", "", limit = 5)
for s, p, o in triples:
    helper[0] = s
    print("s ", end = " ")
    print(s)
    idx_s = np.where(entities == helper[0])
    helper[0] = p
    print("p ", end = " ")
    print(p)
    idx_p = np.where(properties == helper[0])
    helper[0] = o
    print("o ", end = " ")
    print(o)
    idx_o = np.where(entities == helper[0])
    matrix[idx_s[0][0]][idx_p[0][0]] = 1
    if (idx_o[0].size != 0):
        matrix[idx_o[0][0]][idx_p[0][0] + 1] = 1

k, l = 0, 0
for k in range(h):
    for l in range(w):
        print(matrix[k][l], end =" ")
    print("")


