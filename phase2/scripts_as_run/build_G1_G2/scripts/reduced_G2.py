"""Symmetry-reduced exact check of the doubling of Q_p (see orbit_check.py).  Vertex order w3, w1, H, H'.
Automorphisms used, each verified on the built matrix: tau (x -> x + 1 on both copies), mu (x -> g^2 x on
both copies, g a primitive root), swap (x <-> x', w3 <-> w1).
Usage: python3 reduced_G2.py P [NX_MAX] [K_OFFSET] [COLOURS e.g. 0,1]"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, lib, constructions as K, orbit_check as O
p = int(sys.argv[1])
O.NX_MAX = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
off = int(sys.argv[3]) if len(sys.argv) > 3 else 0
cols = [int(c) for c in sys.argv[4].split(',')] if len(sys.argv) > 4 else [0, 1]
k = {797: 11, 1277: 13, 1493: 14, 2741: 15, 2801: 16}.get(p)
t0 = time.time()
C = K.paley_doubling(p); n = len(C)
if k is None:                                   # small test primes: k = omega(Q_p) + 2
    import build_G2 as B; k = B.omega(p)[0] + 2
k += off
g = K.primitive_root(p); g2 = g * g % p
def h(x): return 2 + x % p
def hp(x): return 2 + p + x % p
tau = np.arange(n); mu = np.arange(n); sw = np.arange(n)
for x in range(p):
    tau[h(x)] = h(x + 1); tau[hp(x)] = hp(x + 1)
    mu[h(x)] = h(g2 * x); mu[hp(x)] = hp(g2 * x)
    sw[h(x)] = hp(x); sw[hp(x)] = h(x)
sw[0], sw[1] = 1, 0
stab = {0: [tau, mu], 2: [mu]}
res = O.reduced_check(C, k, cols, [tau, mu, sw], stab, 'Paley doubling p=%d, n=%d, no K_%d' % (p, n, k),
                      log=os.path.join(lib.OUT, 'logs', 'reduced_checks.jsonl'))
print(json.dumps(dict(p=p, n=n, k=k, colours=cols, reps=[int(x) for x in res['vertex_orbit_reps']], searches=len(res['searches']),
                      verdict=res['verdict'], nx_complete=all(s.get('nx_omega') is not None for s in res['searches']),
                      seconds=round(time.time() - t0, 1))))
