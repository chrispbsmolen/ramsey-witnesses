"""Symmetry-reduced exact check of XuR1's M_p' (see orbit_check.py).  Automorphisms used (each verified):
tau: (x, y) -> (x, y + x)  [matrix (1 1; 0 1), det 1], which fixes U and W and shifts every V_i;
sigma: (x, y) -> (x, l*y) with l = beta^3 a cube [det l, a cube], which fixes U, W and every (b^i, 0).
Usage: python3 reduced_777.py P [LEVELS]"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, lib, constructions as K, orbit_check as O
p = int(sys.argv[1]); levels = int(sys.argv[2]) if len(sys.argv) > 2 else 2
t0 = time.time()
C, info = K.xur1(p); beta = info['beta']; n = len(C)
beta_ = K.primitive_root(p); H, _ = K.cubic_residue_colouring(p, beta_)
a = 2
while lib.V.has_clique(H, 0, a + 1, sym=True)[0]: a += 1
k = a + 2 + (int(sys.argv[3]) if len(sys.argv) > 3 else 0)   # optional offset, -1 = negative control
def vidx(i, aa): return 3 + i * p + aa % p
tau = list(range(n)); sig = list(range(n)); lam = pow(beta, 3, p)
for i in range(3):
    bi = pow(beta, i, p)
    for aa in range(p):
        tau[vidx(i, aa)] = vidx(i, aa + bi)
        sig[vidx(i, aa)] = vidx(i, aa * lam)
tau, sig = np.array(tau), np.array(sig)
reps = O.orbits(n, [tau])
stab = {r: ([sig] if r >= 3 + 3 * p or r < 3 or (r - 3) % p == 0 else []) for r in reps}
for r in reps:
    if r < 3 or r >= 3 + 3 * p: stab[r] = [tau, sig]
log = os.path.join(lib.OUT, 'logs', 'reduced_checks.jsonl')
res = O.reduced_check(C, k, [0, 1, 2], [tau], stab, 'XuR1 M_%d prime, n=%d, no K_%d' % (p, n, k), levels=levels, log=log)
print(json.dumps(dict(p=p, n=n, alpha_p=a, k=k, reps=[int(x) for x in res['vertex_orbit_reps']],
                      searches=len(res['searches']), verdict=res['verdict'], seconds=round(time.time() - t0, 1))))
