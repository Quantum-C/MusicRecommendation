from __future__ import division
from collections import defaultdict
from operator import itemgetter
import random

w_us = [0, 0.1, 0.2, 0.3, 0.4]
alpha_u = 0.2
q_us = [5, 6]
alpha_s = 0.15
q_ss = [1, 2, 3]

favSongs = defaultdict(set)
numFavSongs = defaultdict(int)
whoLikes = defaultdict(set)
favSongs_v = defaultdict(set)
numWhoLikes = defaultdict(int)
maxUID = 11000
maxSID = 77997
num2Pred = 100
users = set()

tri_tr = open('striplets.txt', 'r')
tri_val = open('sval.txt', 'r')

for tri in tri_val:
    (u, s) = tri.split()
    u = int(u)
    s = int(s)
    favSongs_v[u].add(s)

for tri in tri_tr:
    (u, s) = tri.split()
    u = int(u)
    s = int(s)
    users.add(u)
    if favSongs_v.has_key(u) and s in favSongs_v[u]:
        continue
    favSongs[u].add(s)
    numFavSongs[u] += 1

tri_tr.close()
tri_val.close()

users = list(users)

# idxs = list(range(maxUID))
# random.shuffle(idxs)
# idxs = idxs[:2*num2Pred]
# val2w = ''
#
# for idx in idxs[:num2Pred]:
#     n = numFavSongs[users[idx]]
#     numFavSongs[users[idx]] //= 2
#     n -= numFavSongs[users[idx]]
#     for j in range(n):
#         s = favSongs[users[idx]].pop()
#         favSongs_v[users[idx]].add(s)
#         val2w += str(users[idx]) + ' ' + str(s) + '\n'
#
# test2w = ''
#
# for idx in idxs[num2Pred:]:
#     n = numFavSongs[users[idx]] - numFavSongs[users[idx]] // 2
#     for j in range(n):
#         test2w += str(users[idx]) + ' ' + str(s) + '\n'
#
# f = open('sval.txt', 'w')
# f.write(val2w)
# f.close()
#
# f = open('stest.txt', 'w')
# f.write(test2w)
# f.close()

for u, ss in favSongs.iteritems():
    for s in ss:
        whoLikes[s].add(u)
        numWhoLikes[s] += 1

tau = 500
stro = ''
f = open('ml111.out', 'w')

for w_u in w_us:
    for q_u in q_us:
        for q_s in q_ss:
            MAP = 0
            for ii, u2pred in enumerate(favSongs_v.keys()):
                predRes = list()
                for s2check in range(maxSID):
                    # If it is a known favorite song (in training set), we skip it
                    if s2check in favSongs[u2pred]:
                        continue
                    # Calculate score_u
                    score_u = 0
                    for u in whoLikes[s2check]:
                        # Cosine similarity
                        # score_u += pow(
                        #     len(favSongs[u].intersection(favSongs[u2pred])) / pow(numFavSongs[u2pred], alpha_u) / pow(
                        #         numFavSongs[u], 1 - alpha_u), q_u)

                        # Tversky index
                        li = len(favSongs[u].intersection(favSongs[u2pred]))
                        score_u += pow(2 * li / (alpha_u * numFavSongs[u] + (2 - alpha_u) * numFavSongs[u2pred]), q_u)

                        # Adjusted Jaccard index
                        li = len(favSongs[u].intersection(favSongs[u2pred]))
                        score_u += pow(li / (alpha_u * numFavSongs[u] + (2 - alpha_u) * numFavSongs[u2pred] - li), q_u)
                    # Calculate score_s
                    score_s = 0
                    for s in favSongs[u2pred]:
                        if numWhoLikes[s2check] == 0:
                            continue
                        # Cosine similarity
                        # score_s += pow(len(whoLikes[s].intersection(whoLikes[s2check])) / (
                        #     pow(numWhoLikes[s2check], alpha_s) * pow(numWhoLikes[s], 1 - alpha_s)), q_s)

                        # Tversky index
                        li = len(whoLikes[s].intersection(whoLikes[s2check]))
                        score_s += pow(2 * li / (alpha_s * numWhoLikes[s] + (2 - alpha_s) * numWhoLikes[s2check]), q_s)

                        # Adjusted index
                        li = len(whoLikes[s].intersection(whoLikes[s2check]))
                        score_s += pow(li / (alpha_s * numWhoLikes[s] + (2 - alpha_s) * numWhoLikes[s2check] - li), q_s)
                    score = w_u * score_u + (1 - w_u) * score_s
                    predRes.append((s2check, score))
                predRes = sorted(predRes, key=itemgetter(1), reverse=True)
                hitCtr = 0
                AP = 0
                l = len(favSongs_v[u2pred])
                for i, (rec_s, score) in enumerate(predRes):
                    if i == min(tau, l):
                        break
                    if rec_s in favSongs_v[u2pred]:
                        hitCtr += 1
                        AP += hitCtr / (i + 1)
                AP /= min(tau, l)
                # print(str(ii) + ': ' + str(hitCtr))
                MAP += AP
            MAP /= len(favSongs_v.keys())
            stro += str(w_u) + ' ' + str(q_u) + ' ' + str(q_s) + ' ' + str(MAP) + '\n'
    print('20% Completed')
    f.write(stro)
    stro = ''

f.close()
