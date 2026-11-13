"""Sanity tests of the two constructions on small inputs, checked exactly with networkx
(maximal-clique enumeration).  Run: python3 test_small.py"""
import itertools, numpy as np, networkx as nx
import g3lib as L


def omega(A): return max(len(c) for c in nx.find_cliques(nx.from_numpy_array(A)))
def alpha(A): return omega(L.complement(A))


def circ(n, D):
    A = np.zeros((n, n), dtype=np.uint8)
    for i in range(n):
        for d in D: A[i][(i + d) % n] = A[(i + d) % n][i] = 1
    return A

ok = True
# Theorem 9: G a (k, l-1)-graph on m vertices -> (2k-1, l)-graph on 4m vertices
# (C5 with l = 4 is excluded: Theorem 9 needs l >= 5, and the construction indeed fails there)
cases = [('C13(1,5) (3,5)', circ(13, [1, 5]), 3, 6),      # R(5,6) >= 4*14-3 = 53
         ('Paley13 (4,4)', circ(13, [1, 3, 4]), 4, 5),    # R(7,5) >= 4*18-3 = 69
         ('C8(1,4) (3,4)', circ(8, [1, 4]), 3, 5)]        # R(5,5) >= 4*9-3 = 33
for name, A, k, l in cases:
    w, a = omega(A), alpha(A)
    assert w < k and a < l - 1, (name, w, a)
    F = L.t9(A); W, Al = omega(F), alpha(F)
    good = W < 2 * k - 1 and Al < l
    ok &= good
    print('t9 %-16s n=%3d -> n=%3d omega %d (< %d) alpha %d (< %d) %s' % (name, len(A), len(F), W, 2 * k - 1, Al, l, 'ok' if good else 'FAIL'))
    # block permutations are automorphisms
    assert all(L.is_automorphism(F, g) for g in L.t9_block_perms(len(A)))

# XSR2 Corollary 3 special case: H = M = K_{k-1}, W1 of size 2, t = 2 -> (k, s+1)-graph on n(G) + 2k - 2
def cor3(G, k):
    # find a K_{k-1} in G
    Gx = nx.from_numpy_array(G)
    K = next(c for c in nx.find_cliques(Gx) if len(c) >= k - 1)[:k - 1]
    H = np.ones((k - 1, k - 1), dtype=np.uint8); np.fill_diagonal(H, 0)
    return L.xsr2_thm3(G, H, K, list(range(k - 1)), 2)

for name, G, k, s in [('comp C13(1,5) (5,3)', L.complement(circ(13, [1, 5])), 5, 3),     # R(5,4) >= 14+8 = 22
                      ('comp C8(1,4) (5,?)', None, None, None)][:1]:
    F = cor3(G, k); W, Al = omega(F), alpha(F)
    good = W < k and Al < s + 1
    ok &= good
    print('cor3 %-15s n=%3d -> n=%3d omega %d (< %d) alpha %d (< %d) %s' % (name, len(G), len(F), W, k, Al, s + 1, 'ok' if good else 'FAIL'))

# random (5,s)-graphs: take random graphs with omega < 5 containing K4, check Cor3 output
rng = np.random.default_rng(1); cnt = 0
while cnt < 30:
    n = int(rng.integers(12, 26)); A = (rng.random((n, n)) < 0.45).astype(np.uint8); A = np.triu(A, 1); A = A + A.T
    for k in (5, 6):
        if omega(A) >= k or omega(A) < k - 1: continue
        s = alpha(A) + 1
        F = cor3(A, k); W, Al = omega(F), alpha(F)
        good = W < k and Al < s + 1; ok &= good; cnt += 1
        if not good: print('cor3 random FAIL', n, k, s, W, Al)
print('cor3 random graphs: %d tested' % cnt)

# Theorem 3 with a general M: G, H random (k,s),(k,t)-graphs sharing an induced M (plant it)
cnt = 0
while cnt < 30:
    k = 5
    m = int(rng.integers(3, 7)); Mx = (rng.random((m, m)) < 0.5).astype(np.uint8); Mx = np.triu(Mx, 1); Mx = Mx + Mx.T
    if omega(Mx) >= k - 2: continue
    def plant(n):
        A = (rng.random((n, n)) < 0.4).astype(np.uint8); A = np.triu(A, 1); A = A + A.T
        A[:m, :m] = Mx; return A
    G = plant(int(rng.integers(m + 3, 18))); H = plant(int(rng.integers(m + 3, 18)))
    if omega(G) >= k or omega(H) >= k: continue
    s, t = alpha(G) + 1, alpha(H) + 1
    m1 = int(rng.integers(1, m))
    # weaker sufficient condition from XSR2 p. 6: neither M[W1] nor M[W2] contains K_{k-2}
    if omega(Mx[:m1, :m1]) >= k - 2 or omega(Mx[m1:, m1:]) >= k - 2: continue
    F = L.xsr2_thm3(G, H, list(range(m)), list(range(m)), m1)
    W, Al = omega(F), alpha(F); good = W < k and Al < s + t - 1; ok &= good; cnt += 1
    if not good: print('thm3 random FAIL', len(G), len(H), m, m1, W, Al, s, t)
print('thm3 random graphs: %d tested' % cnt)
print('ALL OK' if ok else 'SOME FAILED')
