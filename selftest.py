"""Tests of the checker.  Writes results/selftest_output.txt; exit status 1 on any failure.

A. Oracle: networkx (exact maximal-clique enumeration, a different algorithm, no shared code) against
   the C solver on 40 random graphs, for both the clique number and the independence number.
B. Planted negatives: a K6 planted in a sparse graph and an independent 12-set planted in a dense one
   must be found; corrupted witnesses (one edge changed) must FAIL.
C. The circulant shortcut (cliques through vertex 0 only) agrees with the full search.
D. Loaders: one small colouring written in every supported format loads back identically.
E. The small witnesses constructed here, rechecked by the networkx oracle.
"""
import os, sys, json, random, tempfile
import numpy as np, networkx as nx
import verify_ramsey as V
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
lines = []; bad = 0
def say(s): lines.append(s); print(s, flush=True)
def check(name, ok):
    global bad
    if not ok: bad += 1
    say('%-58s %s' % (name, 'ok' if ok else 'FAILED'))
def omega(G): return max((len(c) for c in nx.find_cliques(G)), default=0)

# A
rng = random.Random(7); dis = 0
for trial in range(40):
    n = rng.randint(8, 60); p = rng.choice([0.2, 0.5, 0.8])
    G = nx.gnp_random_graph(n, p, seed=rng.randint(0, 10 ** 6))
    C = V.from_adjacency(nx.to_numpy_array(G, dtype=int))
    w, a = omega(G), omega(nx.complement(G))
    ok = V.has_clique(C, 1, w)[0] and not V.has_clique(C, 1, w + 1)[0] and V.has_clique(C, 0, a)[0] and not V.has_clique(C, 0, a + 1)[0]
    if not ok: dis += 1; say('  disagreement n=%d p=%.1f w=%d a=%d' % (n, p, w, a))
check('A. oracle: 40 random graphs, disagreements %d' % dis, dis == 0)

# B
G = nx.gnp_random_graph(80, 0.15, seed=1); S = rng.sample(range(80), 6); G.add_edges_from((x, y) for x in S for y in S if x < y)
check('B. planted K6 in G(80, 0.15) found', V.has_clique(V.from_adjacency(nx.to_numpy_array(G, dtype=int)), 1, 6)[0])
G = nx.gnp_random_graph(80, 0.85, seed=2); S = rng.sample(range(80), 12); G.remove_edges_from([(x, y) for x in S for y in S if x < y])
check('B. planted independent 12-set in G(80, 0.85) found', V.has_clique(V.from_adjacency(nx.to_numpy_array(G, dtype=int)), 0, 12)[0])
C = V.load_g6('constructions/witnesses/paley101_R6_6.g6')
check('B. Paley(101) passes R(6,6)', V.verify(C, [6, 6])['verdict'] == 'PASS')
check('B. Paley(101) fails R(5,6) (its clique number is 5)', V.verify(C, [5, 6])['verdict'] == 'FAIL')
D = C.copy()                      # make vertices 0..5 a clique
S6 = [0, 1, 2, 3, 4, 5]
for x in S6:
    for y in S6:
        if x != y: D[x][y] = 1
check('B. Paley(101) with a planted K6 fails R(6,6)', V.verify(D, [6, 6])['verdict'] == 'FAIL')
E = V.load_colormat('constructions/witnesses/clebsch16_R3_3_3.txt')
check('B. Clebsch colouring passes R(3,3,3)', V.verify(E, [3, 3, 3])['verdict'] == 'PASS')
c = E[0][1]; t = [x for x in range(2, 16) if E[0][x] == c and E[1][x] != c][0]; E2 = E.copy(); E2[1][t] = E2[t][1] = c
check('B. Clebsch colouring with one edge recoloured fails', V.verify(E2, [3, 3, 3])['verdict'] == 'FAIL')
L = V.load_circ3json('third_party/lachy-dauth/circulants.json', 0)
check('B. Lachy-Dauth R(3,3,9) circulant fails as R(3,3,8)', V.verify(L, [3, 3, 8])['verdict'] == 'FAIL')

# C
C = V.circulant_matrix(61, list(range(1, 30, 2)))
check('C. circulant shortcut agrees with full search, k = 4..8', all(V.has_clique(C, 1, k, sym=True)[0] == V.has_clique(C, 1, k)[0] for k in range(4, 9)))
check('C. is_circulant: Paley(101) yes, Clebsch colouring no', V.is_circulant(V.load_g6('constructions/witnesses/paley101_R6_6.g6')) and not V.is_circulant(V.load_colormat('constructions/witnesses/clebsch16_R3_3_3.txt')))

# D
n = 13; Q = {1, 3, 4, 9, 10, 12}; A = np.array([[1 if i != j and (i - j) % n in Q else 0 for j in range(n)] for i in range(n)])
ref = V.from_adjacency(A)
with tempfile.TemporaryDirectory() as d:
    p = lambda f: os.path.join(d, f)
    open(p('a.g6'), 'wb').write(nx.to_graph6_bytes(nx.from_numpy_array(A), header=False))
    open(p('a.m01'), 'w').write('\n'.join(''.join(map(str, r)) for r in A) + '\n')
    open(p('a.col'), 'w').write('\n'.join(''.join(str(int(v)) for v in r) for r in A) + '\n')
    open(p('a.np'), 'w').write(np.array2string(A, threshold=10 ** 6, max_line_width=10 ** 6))
    open(p('a.clq'), 'w').write('p edge %d %d\n' % (n, A.sum() // 2) + ''.join('e %d %d\n' % (i + 1, j + 1) for i in range(n) for j in range(i + 1, n) if A[i][j]))
    open(p('ch.13'), 'w').write('0' + ''.join('1' if min(x, n - x) in Q else '0' for x in range(1, n)) + '\n')
    loaded = dict(g6=V.load_g6(p('a.g6')), matrix01=V.load_matrix01(p('a.m01')), npmatrix=V.load_npmatrix(p('a.np')), dimacs=V.load_dimacs(p('a.clq')),
                  circulant=V.load('circulant', '13:1,3,4'))
    col = V.load_colormat(p('a.col'))
    check('D. g6, matrix01, npmatrix, dimacs, circulant load identically', all((v == ref).all() for v in loaded.values()))
    check('D. colormat loads the same partition', (col == ref).all() or (col == 1 - ref - 2 * np.eye(n, dtype=int)).all())
    # distrow is a distance colouring on a path, not a circulant: compare with its definition
    dr = V.load_distrow(p('ch.13'))
    s = '0' + ''.join('1' if min(x, n - x) in Q else '0' for x in range(1, n))
    exp = np.array([[-1 if i == j else int(s[abs(i - j)]) for j in range(n)] for i in range(n)])
    check('D. distrow: colour of ij is c[|i-j|]', (dr == exp).all() or (dr == 1 - exp - 2 * np.eye(n, dtype=int)).all())

# E
for f, ks in (('c5_R3_3.g6', (3, 3)), ('paley101_R6_6.g6', (6, 6))):
    G = nx.from_graph6_bytes(V.g6_lines('constructions/witnesses/' + f)[0])
    check('E. networkx: %s has clique number < %d and independence number < %d' % (f, ks[0], ks[1]), omega(G) < ks[0] and omega(nx.complement(G)) < ks[1])
E = V.load_colormat('constructions/witnesses/clebsch16_R3_3_3.txt')
check('E. networkx: each colour class of clebsch16 is triangle-free', all(omega(nx.from_numpy_array((E == c).astype(int))) < 3 for c in range(3)))

say('\nALL TESTS PASS' if not bad else '\n%d TESTS FAILED' % bad)
os.makedirs('results', exist_ok=True)
open('results/selftest_output.txt', 'w').write('\n'.join(lines) + '\n')
sys.exit(1 if bad else 0)
