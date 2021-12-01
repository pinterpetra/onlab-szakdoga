
import re

entities = [
	"http://asd/cica/kutya/alma",
	"http://asd/cica/nyuszi/alma",
	"http://asd/cica/alma",
	"http://asd/cica/kutya/ananasz",
	"http://asd/krumpli/kutya/ananasz#alma"
]

clustered_entities = [ 0, 1, 2 ]

REPLACE_NONWORD = re.compile(r"[^\w]+", re.MULTILINE)

scores = {}
for x in clustered_entities:
	e = re.sub(REPLACE_NONWORD, '/', entities[x]).split('/')[2:]
	e.reverse()
	l = len(e)
	for idx in range(l):
		y = e[idx]
		if not y in scores:
			scores[y] = 0
		scores[y] += 1 - (idx/l)

minimumScore = len(clustered_entities) * 0.5
print(minimumScore)

relevantNames = [x[0] for x in filter(
	lambda score: score[1] >= minimumScore,
	scores.items()
)]

print("?" + "_".join(relevantNames))
