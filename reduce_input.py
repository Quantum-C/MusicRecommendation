import random

tri_tr = open('new_triplets.txt', 'r')
small_tr = open('small_triplets.txt', 'w')
maxUID = 109999
numToPred = 11000
idxs = list(range(maxUID + 1))
random.shuffle(idxs)
idxs = set(idxs[:numToPred])
str2w = ''

for i, tri in enumerate(tri_tr):
    if i in idxs:
        str2w += tri

small_tr.write(str2w)
tri_tr.close()
