from hdt import HDTDocument

document = HDTDocument("disgenet.hdt")

(triples, cardinality) = document.search_triples("", "", "", limit = 20)
for s, p, o in triples:
    print("S:")
    print(s)
    print("P:")
    print(p)
    print("O:")
    print(o)


#ha a matrix [3][0] = 1, akkor entities[3] entitasbol van el a properties[0]-ba

#calculate similarity for first and second entity:
#entities[0]
#entities[1]
elso = set()
for i in range(w)
    elso.add(matrix[0][i])

masodik = set()
for i in range(w)
    masodik.add(matrix[1][i])

inter = elso.intersection(masodik)
similarity = len(inter) #ahany kozos property volt


