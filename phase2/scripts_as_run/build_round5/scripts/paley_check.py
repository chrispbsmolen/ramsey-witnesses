"""R3 inputs: c(G_p) = k for the Paley graph G_p (p prime, p = 1 mod 4), with both checkers, on a symmetry reduction whose
automorphisms are verified first.

Verified on the object (G_p is the circulant with connection set QR = nonzero squares mod p; its matrix is
A[x][y] = QR[(y - x) mod p], so a check on QR is a check on every entry):
  (a) QR = -QR (the graph is undirected), |QR| = (p-1)/2;
  (b) x -> x + 1 is an automorphism (A is circulant: checked on the matrix);
  (c) x -> g^2 x (g a primitive root) is an automorphism: g^2 * QR = QR, and its powers act transitively on QR, so
      the group {x -> a x + b, a in QR} is transitive on ordered edges (every edge maps to (0,1));
  (d) sigma: x -> 1 - x is an automorphism ((-1) in QR, checked) fixing the edge {0,1} and mapping
      B = N(0) & N(1) onto itself.
So a K_(k+1) exists iff one contains 0, 1 and some a in B, i.e. iff for some orbit representative a of sigma on B,
T_a = B & N(a) holds a K_(k-2).  Every representative's T_a goes to clique.c and to gen0 (same graph, K_(k-2)).
Also (e): a K_k exists: clique.c is asked for K_(k-3) in T_a for the first representatives until FOUND, and the
k vertices {0, 1, a, ...} are checked edge by edge on QR.
Usage: python3 paley_check.py P K TIMEOUT_EACH [START END]   Appends to logs/paley_omega_r5.jsonl."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L

p, k, to = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
assert p % 4 == 1 and all(p % d for d in range(2, int(p ** .5) + 1))
QR = np.zeros(p, dtype=bool); QR[[x * x % p for x in range(1, p)]] = True
def order(a):
    x, e = a, 1
    while x != 1: x = x * a % p; e += 1
    return e
g = next(a for a in range(2, p) if order(a) == p - 1)
S = np.flatnonzero(QR)
chk = {}
chk['a_symmetric'] = bool(all(QR[(-s) % p] for s in S)) and len(S) == (p - 1) // 2
A = QR[(np.arange(p)[None, :] - np.arange(p)[:, None]) % p]
chk['b_translation'] = L.is_circulant(A)
g2 = g * g % p
chk['c_mult_g2_preserves_QR'] = bool(all(QR[g2 * s % p] for s in S))
orb, x = set(), 1
while True:
    orb.add(x); x = x * g2 % p
    if x == 1: break
chk['c_transitive_on_QR'] = orb == set(S.tolist())
B = [x for x in range(2, p) if QR[x] and QR[(x - 1) % p]]
chk['d_sigma_preserves_B'] = all(((1 - a) % p) in set(B) for a in B) and bool(QR[p - 1])
del A
assert all(chk.values()), chk
reps = sorted({min(a, (1 - a) % p) for a in B})
start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
end = int(sys.argv[5]) if len(sys.argv) > 5 else len(reps)
Bn = np.array(B)
def T_of(a):
    T = Bn[QR[(Bn - a) % p]]
    M = QR[(T[:, None] - T[None, :]) % p]; np.fill_diagonal(M, False)
    return T, M
t0 = time.time(); bad = []; secs = {'clique': 0.0, 'gen0': 0.0}; mx = 0
for a in reps[start:end]:
    T, M = T_of(a); mx = max(mx, len(T))
    for c in ('clique', 'gen0'):
        f, o, s = L.solve(c, M, k - 2, to); secs[c] += s
        if f is not False: bad.append((a, c, o))
rec = dict(p=p, k=k, primitive_root=g, automorphism_checks=chk, B=len(B), orbit_reps=len(reps), range=[start, end],
           claim='no K_%d in G_%d' % (k + 1, p), subproblem_max=mx, checker_seconds={c: round(v, 1) for c, v in secs.items()},
           not_none=bad[:20])
if start == 0:
    for a in reps:
        T, M = T_of(a)
        f, o, s = L.solve('clique', M, k - 3, to)
        if f:
            vs = [0, 1, a] + [int(T[int(v)]) for v in o.split()[2:2 + k - 3]]
            rec['K_k_witness'] = dict(vertices=vs, size=len(set(vs)),
                                      all_edges_checked=bool(len(set(vs)) == k and all(QR[(u - v) % p] for u in vs for v in vs if u != v)))
            break
full = (start == 0 and end == len(reps))
rec['verdict'] = ('PASS: c(G_%d) = %d (both checkers, all %d reps)' % (p, k, len(reps))
                  if full and not bad and rec.get('K_k_witness', {}).get('all_edges_checked') else
                  ('PASS (range only)' if not bad else 'FAIL'))
rec['seconds'] = round(time.time() - t0, 1)
L.log('paley_omega_r5.jsonl', rec)
