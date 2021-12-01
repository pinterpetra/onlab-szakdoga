
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

w = 10
h = 4

daaa = [
	[ 1, 1, 0, 0, 0, 0, 0, 0, 0, 0 ],
	[ 0, 0, 1, 1, 1, 0, 0, 0, 0, 0 ],
	[ 0, 0, 0, 0, 1, 0, 0, 0, 0, 0 ],
	[ 0, 0, 0, 1, 0, 0, 0, 0, 0, 0 ]
]

"""db = [
	[daaa[0], None],
	[daaa[1], None],
	[daaa[2], None],
	[daaa[3], None]
]"""

db = [None]*h

for x in range(h):
	db[x] = [daaa[x], None]

def distFunc(p, q):
	c = 0
	for i in range(w):
		if p[0][i] == q[0][i]:
			c += 1
	print(c/w)
	return 1 - c / w


dbscan(db, distFunc, 0.1, 1)

print(db)
