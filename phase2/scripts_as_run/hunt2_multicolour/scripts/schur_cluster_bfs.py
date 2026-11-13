"""Light neighbourhood search for XXER's R(3,3,3,5) >= 162 claim (EJC 11 #R35 pp.2-3).
Exoo (EJC 1 #R8, p.2) reports ~10,000 sum-free partitions of [1,160] into 5 sets, 'all close to each other: one
can begin with one of the partitions, move an integer from one set to another, and obtain a new partition'.
This script enumerates (breadth first) the partitions reachable from given seed partitions by single-integer
moves that keep every set sum-free (not necessarily symmetric), up to colour relabelling, and for each one
tests all 10 colour merges for a K5 in the union (colouring of K_161 on [0,160]: colour(u,v) = set of |u-v|).
Prints any partition with a K5-free merge.  Usage: python3 schur_cluster_bfs.py SEED1 [SEED2 ...] --time=S
Seed files: 5 non-comment lines, each a full list of one set (all of [1,160])."""
import sys, time, itertools, json
from collections import deque

N = 161
TL = float(next((a.split('=')[1] for a in sys.argv if a.startswith('--time=')), 500))
seeds = [a for a in sys.argv[1:] if not a.startswith('--')]


def canon(col):
    m = {}; out = []
    for x in col:
        if x not in m: m[x] = len(m)
        out.append(m[x])
    return tuple(out)


def load(path):
    rows = [[int(x) for x in l.split()] for l in open(path) if l.strip() and not l.startswith('#')]
    col = [None] * 160
    for c, r in enumerate(rows):
        for x in r: col[x - 1] = c
    assert None not in col
    return canon(col)


def ok_move(sets, x, c):
    S = sets[c]
    if 2 * x in S or (x % 2 == 0 and x // 2 in S): return False
    for a in S:
        if a != x and (a + x in S or abs(a - x) in S): return False
    return True


def k5_free(col, a, b):
    D = [False] * N
    for d in range(1, N): D[d] = col[d - 1] in (a, b)
    adj = [0] * N
    for i in range(N):
        m = 0
        for j in range(N):
            if j != i and D[abs(i - j)]: m |= 1 << j
        adj[i] = m
    def rec(cand, k):
        if k == 0: return True
        while cand:
            if bin(cand).count('1') < k: return False
            v = cand.bit_length() - 1; cand &= ~(1 << v)
            if rec(cand & adj[v], k - 1): return True
        return False
    return not rec((1 << N) - 1, 5)


t0 = time.time(); Q = deque(); seen = set()
for s in seeds:
    c = load(s); seen.add(c); Q.append(c)
n = 0; found = []; sym = 0
while Q and time.time() - t0 < TL:
    col = Q.popleft(); n += 1
    if all(col[x - 1] == col[N - x - 1] for x in range(1, 161)): sym += 1
    for a, b in itertools.combinations(range(5), 2):
        if k5_free(col, a, b):
            found.append({'partition': [[x for x in range(1, 161) if col[x - 1] == c] for c in range(5)], 'merge': [a + 1, b + 1]})
            print(json.dumps({'FOUND': found[-1]}), flush=True)
    sets = [set(x for x in range(1, 161) if col[x - 1] == c) for c in range(5)]
    for x in range(1, 161):
        for c in range(5):
            if c == col[x - 1] or not ok_move(sets, x, c): continue
            nc = list(col); nc[x - 1] = c; nc = canon(nc)
            if nc not in seen: seen.add(nc); Q.append(nc)
    if n % 500 == 0: print(json.dumps({'tested': n, 'queue': len(Q), 'seen': len(seen), 'symmetric_tested': sym, 's': round(time.time() - t0)}), flush=True)
print(json.dumps({'result': 'EXHAUSTED' if not Q else 'TIMEOUT', 'tested': n, 'seen': len(seen), 'queue_left': len(Q),
                  'symmetric_tested': sym, 'found': len(found), 'seconds': round(time.time() - t0)}))
