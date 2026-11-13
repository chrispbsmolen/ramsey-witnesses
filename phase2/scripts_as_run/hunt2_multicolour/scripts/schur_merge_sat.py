"""Light reconstruction attempt for XXER's R(3,3,3,5) >= 162 claim (EJC 11 (2004) #R35, pp.2-3):
'if, in the resulting (3,3,3,3,3;161)-coloring [Exoo's, EJC 1 #R8], the colors 2 and 3 are merged, then we
obtain a (3,5,3,3;161)-coloring'.  The partition printed in EJC 1 #R8 does not have this property (all 10
merges contain a K5; scripts/merge_k5.py).  Question asked here: does ANY sum-free partition of [1,160]
into 5 sets (symmetric or, with --linear, not necessarily symmetric) have two classes whose union is
K5-free in the induced colouring of K_161?  Lazy SAT (counterexample-guided):
  * variables x[i][c]: element i has colour c (i = 1..80 if symmetric, 1..160 if linear), exactly one colour;
  * sum-free clauses for every colour;
  * colours 0 and 1 are the pair to be merged; every K5 found in the union graph is forbidden by a clause
    'at least one of its 10 differences is not in colours 0/1', plus (symmetric case) all its images under
    multiplication by units mod 161 (automorphisms of the circulant setting).
Stops on SAT-with-K5-free-union (prints the partition) or UNSAT, or at the time limit.
Run with an interpreter that has python-sat (pysat) installed; 1 core."""
import sys, time, itertools, json, threading
from pysat.solvers import Glucose4

N = 161; SYM = '--linear' not in sys.argv
TL = float(next((a.split('=')[1] for a in sys.argv if a.startswith('--time=')), 540))
M = 80 if SYM else 160
fold = (lambda d: d if d <= 80 else N - d) if SYM else (lambda d: d)
var = lambda i, c: (i - 1) * 5 + c + 1
S = Glucose4()
for i in range(1, M + 1):
    S.add_clause([var(i, c) for c in range(5)])
    for a, b in itertools.combinations(range(5), 2): S.add_clause([-var(i, a), -var(i, b)])
seen = set()
for a in range(1, 161):
    for b in range(a, 161 - a):
        t = tuple(sorted({fold(a), fold(b), fold(a + b)}))
        if t in seen: continue
        seen.add(t)
        for c in range(5): S.add_clause([-var(i, c) for i in t])
# light colour symmetry breaking: colours 2,3,4 are interchangeable, as are 0,1 -> order by first occurrence
# (only fixes the colour of element 1 to be in {0, 2}).
S.add_clause([var(1, 0), var(1, 2)])
units = [u for u in range(1, N) if u % 7 and u % 23] if SYM else [1]


def find_k5(col):
    U = [j for j in range(N)]
    inU = lambda d: col[fold(d)] in (0, 1)
    adj = [0] * N
    for i in range(N):
        m = 0
        for j in range(N):
            if j != i and inU(abs(i - j)): m |= 1 << j
        adj[i] = m
    def rec(cand, k, ch):
        if k == 0: return ch
        while cand:
            if bin(cand).count('1') < k: return None
            v = cand.bit_length() - 1; cand &= ~(1 << v)
            r = rec(cand & adj[v], k - 1, ch + [v])
            if r: return r
        return None
    if SYM: return rec(adj[0], 4, [0])
    return rec((1 << N) - 1, 5, [])


# optional phase seeding from a known partition file (5 lines; the first two lines become colours 0 and 1)
seed = next((a.split('=')[1] for a in sys.argv if a.startswith('--seed=')), None)
if seed:
    rows = [[int(x) for x in l.split()] for l in open(seed) if l.strip() and not l.startswith('#')]
    order = [int(x) - 1 for x in next((a.split('=')[1] for a in sys.argv if a.startswith('--order=')), '1,2,3,4,5').split(',')]
    cs = {}
    for newc, oldc in enumerate(order):
        for x in rows[oldc]:
            if x <= M: cs[x] = newc
    S.set_phases([var(i, c) if cs.get(i) == c else -var(i, c) for i in range(1, M + 1) for c in range(5)])
t0 = time.time(); it = 0; ncl = 0
while True:
    if time.time() - t0 > TL: print(json.dumps({'result': 'TIMEOUT', 'iterations': it, 'k5_clauses': ncl, 'seconds': round(time.time() - t0)})); break
    tm = threading.Timer(max(1, TL - (time.time() - t0)), S.interrupt); tm.start()
    r = S.solve_limited(expect_interrupt=True); tm.cancel()
    if r is None: print(json.dumps({'result': 'TIMEOUT_IN_SOLVE', 'iterations': it, 'k5_clauses': ncl, 'seconds': round(time.time() - t0)})); break
    if not r: print(json.dumps({'result': 'UNSAT', 'symmetric': SYM, 'iterations': it, 'k5_clauses': ncl, 'seconds': round(time.time() - t0)})); break
    mdl = set(l for l in S.get_model() if l > 0)
    col = {i: next(c for c in range(5) if var(i, c) in mdl) for i in range(1, M + 1)}
    K = find_k5(col); it += 1
    if K is None:
        parts = [[d for d in range(1, 161) if col[fold(d)] == c] for c in range(5)]
        print(json.dumps({'result': 'FOUND', 'symmetric': SYM, 'merged': [0, 1], 'parts': parts, 'iterations': it, 'seconds': round(time.time() - t0)})); break
    diffs = {abs(a - b) for a, b in itertools.combinations(K, 2)}
    for u in units:
        ds = sorted({fold((u * d) % N) for d in diffs}) if SYM else sorted({fold(d) for d in diffs})
        S.add_clause([var(e, c) for e in ds for c in (2, 3, 4)]); ncl += 1
    if it % 200 == 0: print(json.dumps({'iter': it, 'clauses': ncl, 's': round(time.time() - t0)}), flush=True)
