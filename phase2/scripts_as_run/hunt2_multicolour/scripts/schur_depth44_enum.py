"""Enumerate symmetric sum-free partitions of [1,160] into 5 sets with depth 44 (Fredricksen-Sweet, EJC 7 (2000)
#R32 p.5: 'all partitions of 160's would be equivalent to the 5840 we found exhaustively for 160 with d = 44',
conditional on their Conjecture 2) and test, for each, all 10 colour merges for a K5 in the union graph of the
circulant colouring of K_161 (colour(u,v) = set containing |u-v|).  Merges are invariant under the
multiplicative equivalence of FreSw (multiplication by a unit mod 161 is a graph isomorphism), so this covers
every symmetric partition equivalent to a depth-44 one.
Encoding (pysat, Glucose4): x[i][c], i = 1..80 (i and 161-i share a colour), c = 0..4; sum-free clauses;
depth 44: elements 1..43 avoid colour 4; colours 0..3 ordered by first occurrence (symmetry breaking);
all solutions enumerated with blocking clauses.  Output: count, merge results, any K5-free merge."""
import sys, time, itertools, json, threading
from pysat.solvers import Glucose4

N = 161; M = 80; TL = float(next((a.split('=')[1] for a in sys.argv if a.startswith('--time=')), 540))
fold = lambda d: d if d <= 80 else N - d
x = lambda i, c: (i - 1) * 5 + c + 1
top = M * 5
u = {}
def U(c, i):
    global top
    if (c, i) not in u: top += 1; u[(c, i)] = top
    return u[(c, i)]
S = Glucose4()
for i in range(1, M + 1):
    S.add_clause([x(i, c) for c in range(5)])
    for a, b in itertools.combinations(range(5), 2): S.add_clause([-x(i, a), -x(i, b)])
seen = set()
for a in range(1, 161):
    for b in range(a, 161 - a):
        t = tuple(sorted({fold(a), fold(b), fold(a + b)}))
        if t not in seen:
            seen.add(t)
            for c in range(5): S.add_clause([-x(i, c) for i in t])
for i in range(1, 44): S.add_clause([-x(i, 4)])
# first-occurrence order for colours 0..3: U(c,i) <-> colour c used among 1..i
for c in range(4):
    for i in range(1, M + 1):
        prev = [U(c, i - 1)] if i > 1 else []
        S.add_clause([-U(c, i), x(i, c)] + prev)
        S.add_clause([U(c, i), -x(i, c)])
        if prev: S.add_clause([U(c, i), -prev[0]])
S.add_clause([x(1, 0)])
for c in range(1, 4):
    for i in range(2, M + 1): S.add_clause([-x(i, c), U(c - 1, i - 1)])
    S.add_clause([-x(1, c)])


def k5(col, a, b):
    D = [False] * N
    for d in range(1, N): D[d] = col[fold(d)] in (a, b)
    adj = [sum(1 << j for j in range(N) if j != i and D[abs(i - j)]) for i in range(N)]
    def rec(cand, k, ch):
        if k == 0: return ch
        while cand:
            if bin(cand).count('1') < k: return None
            v = cand.bit_length() - 1; cand &= ~(1 << v)
            r = rec(cand & adj[v], k - 1, ch + [v])
            if r: return r
        return None
    return rec(adj[0], 4, [0])


t0 = time.time(); n = 0; found = []; status = 'EXHAUSTED'
out = open(sys.argv[1], 'w') if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else None
while True:
    if time.time() - t0 > TL: status = 'TIMEOUT'; break
    tm = threading.Timer(max(1, TL - (time.time() - t0)), S.interrupt); tm.start()
    r = S.solve_limited(expect_interrupt=True); tm.cancel()
    if r is None: status = 'TIMEOUT_IN_SOLVE'; break
    if not r: break
    mdl = set(l for l in S.get_model() if 0 < l <= M * 5)
    col = {i: next(c for c in range(5) if x(i, c) in mdl) for i in range(1, M + 1)}
    n += 1
    if out: out.write(' '.join(str(col[i]) for i in range(1, M + 1)) + '\n')
    for a, b in itertools.combinations(range(5), 2):
        if k5(col, a, b) is None:
            found.append({'colours_1_to_80': [col[i] for i in range(1, M + 1)], 'merge': [a, b]})
            print(json.dumps({'FOUND': found[-1]}), flush=True)
    S.add_clause([-x(i, col[i]) for i in range(1, M + 1)])
    if n % 500 == 0: print(json.dumps({'enumerated': n, 's': round(time.time() - t0)}), flush=True)
print(json.dumps({'result': status, 'partitions_enumerated': n, 'merges_tested': 10 * n, 'k5_free_merges': len(found), 'seconds': round(time.time() - t0)}))
