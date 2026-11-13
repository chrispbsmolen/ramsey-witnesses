"""Light test: is some union of cyclotomic classes of index d in Z_p (p prime) a (k,l)-graph?
Classes C_i = g^i * <g^d>; d must make -1 lie in <g^d> ((p-1)/d even) so the graph is undirected.
Unions are taken up to multiplication by g (cyclic shift of the index set) and complement is NOT identified
(k != l).  K_k test first (fast), then independence via clique.c --sym with a timeout.
usage: python3 -I cyclo_unions.py p d k l per_check_timeout total_seconds"""
import sys, os, itertools, time, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import verify_ramsey as V
p, d, k, l, tmo, tot = [int(x) for x in sys.argv[1:7]]
assert (p - 1) % d == 0 and ((p - 1) // d) % 2 == 0
def prim(p):
    fs = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, q))]
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs): return g
g = prim(p); H = {pow(g, d * j, p) for j in range((p - 1) // d)}
cls = [sorted({(pow(g, i, p) * h) % p for h in H}) for i in range(d)]
seen = set(); t0 = time.time(); hits = 0
for r in range(1, d):
    for T in itertools.combinations(range(d), r):
        key = min(tuple(sorted((t + s) % d for t in T)) for s in range(d))
        if key in seen: continue
        seen.add(key)
        if time.time() - t0 > tot: print('TIME UP'); sys.exit(0)
        D = sorted(set(x for t in T for x in cls[t]))
        C = V.circulant_matrix(p, [x for x in D if x <= p // 2])
        if V.has_clique(C, 1, k, sym=True, timeout=tmo)[0]: continue
        try:
            ind = V.has_clique(C, 0, l, sym=True, timeout=tmo)[0]
        except subprocess.TimeoutExpired:
            print('timeout alpha', T); continue
        if not ind:
            print('HIT', p, d, T, 'D=', ','.join(map(str, [x for x in D if x <= p // 2]))); hits += 1
print('done, classes tried', len(seen), 'hits', hits, 'g', g)
