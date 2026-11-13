"""Second, independent implementation of the constructions, written directly from the papers'
wording with explicit loops (no shared code with g3lib.t9 / g3lib.xsr2_thm3), compared edge by edge
with every built file.  Also records the structural facts the proofs use.
  python3 structure_check.py        -> logs/structure_check.json
"""
import os, sys, json, gzip
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools')); sys.path.insert(0, HERE)
import verify_ramsey as V
from verify_built import load_built
import build as B


def adj_of(cell):
    C, m = load_built(cell); A = (C == 1).astype(np.uint8); np.fill_diagonal(A, 0); return A, m


def thm9_from_text(G):
    """XXER p. 11 (proof of Theorem 7) and p. 15 (Theorem 9): vertices (u_i, v_j), i = 1..4.
    colour inside U_i: 2 if v_j1 v_j2 in E(G) else 3.  i1 in {1,2}, i2 in {3,4}: 1 if j1 = j2, 2 if
    adjacent in G, 3 otherwise.  (i1,i2) in {(1,2),(3,4)}: 3 if j1 = j2, 1 otherwise.
    Theorem 9: H = colours 1 and 2."""
    m = len(G); n = 4 * m
    col = {}
    H = np.zeros((n, n), dtype=np.uint8)
    for i1 in range(1, 5):
        for i2 in range(1, 5):
            for j1 in range(m):
                for j2 in range(m):
                    a = (i1 - 1) * m + j1; b = (i2 - 1) * m + j2
                    if a == b: continue
                    if i1 == i2: c = 2 if G[j1][j2] else 3
                    elif {i1, i2} in ({1, 2}, {3, 4}): c = 3 if j1 == j2 else 1
                    else: c = 1 if j1 == j2 else (2 if G[j1][j2] else 3)
                    H[a][b] = 1 if c in (1, 2) else 0
    return H


def thm3_from_text(G, H, uidx, vidx, m1):
    """XSR2 preprint p. 4-5: V(F) = V(G) u V(H) u W1 u W2; E(F) = E(G) u E(H) u E(M[W1]) u E(M[W2]) u
    {w_i u_j : i != j, u_i u_j in E(G)} u {w_i v_j : i != j, v_i v_j in E(H)} u {u_i v_i}.
    Here u_i = uidx[i], v_i = vidx[i]; the paper's 'i != j' compares vertex labels, i.e. u_j != u_i."""
    p, q, m = len(G), len(H), len(uidx); n = p + q + m
    F = np.zeros((n, n), dtype=np.uint8)
    def e(a, b): F[a][b] = F[b][a] = 1
    for a in range(p):
        for b in range(p):
            if G[a][b]: e(a, b)
    for a in range(q):
        for b in range(q):
            if H[a][b]: e(p + a, p + b)
    w = lambda i: p + q + i
    for i in range(m):
        for j in range(m):
            if i != j and ((i < m1) == (j < m1)) and G[uidx[i]][uidx[j]]: e(w(i), w(j))
        for b in range(p):
            if b != uidx[i] and G[uidx[i]][b]: e(w(i), b)
        for b in range(q):
            if b != vidx[i] and H[vidx[i]][b]: e(w(i), p + b)
        e(uidx[i], p + vidx[i])
    return F


def comp(A):
    B = 1 - A; np.fill_diagonal(B, 0); return B.astype(np.uint8)


def main():
    out = {}
    paley, _ = B.load_input('constructions/paley101_R6_6.g6', 6, 6)
    mat204, _ = B.load_input('constructions/mathon101_R7_7.g6', 7, 7)
    mat564, _ = B.load_input('constructions/mathon281_R9_9.g6', 9, 9, orient=False)
    ins = {'7,11': (paley, True), '8,13': (mat204, True),
           '8,11': (B.load_input('exoo_tatarevic/g67.114', 6, 7)[0], True),
           '8,15': (B.load_input('tatarevic/g78.218', 8, 7)[0], True),
           '8,17': (B.load_input('kuznetsov/table2(7,9)', 9, 7)[0], True),
           '7,16': (B.load_input('tatarevic/g415.157', 4, 15)[0], False),
           '7,17': (B.load_input('kuznetsov/table2(6,9)', 9, 6)[0], True),
           '5,21': (B.load_input('exoo_site/r3.20.110', 3, 20)[0], False)}
    F711, _ = adj_of('7,11')
    ins['8,21'] = (comp(F711), True)
    n89, ds = open(os.path.join(HERE, 'downloads/kuznetsov_lead/R8_9_328_circulant.txt')).read().strip().split(':')
    C89 = V.circulant_matrix(int(n89), [int(d) for d in ds.split(',')])
    ins['10,15'] = ((C89 == 0).astype(np.uint8) * (1 - np.eye(int(n89), dtype=np.uint8)), True)   # non-edges avoid K8
    for cell, (G, c) in ins.items():
        A, m = adj_of(cell)
        H = thm9_from_text(G); H = comp(H) if c else H
        out[cell] = dict(rule='XXER Thm 9' + (' then complement' if c else ''), identical=bool((H == A).all()), n=len(A))
        print(cell, out[cell], flush=True)
    # Corollary 3 cells: the K_{k-1} used is read back from the manifest
    man = json.load(open(os.path.join(HERE, 'built', 'manifest.json')))
    g514 = B.load_input('kuznetsov/table2(5,14)', 5, 14)[0]
    for cell, G, k in (('5,15', g514, 5), ('7,12', F711, 7), ('9,10', mat564, 9), ('aux_7,8', mat204, 7)):
        A, m = adj_of(cell); K = man[cell]['clique_in_G']
        assert G[np.ix_(K, K)].sum() == len(K) * (len(K) - 1)
        Hk = np.ones((k - 1, k - 1), dtype=np.uint8); np.fill_diagonal(Hk, 0)
        F = thm3_from_text(G, Hk, K, list(range(k - 1)), 2)
        out[cell] = dict(rule='XSR2 Thm 3 / Cor 3, H = M = K_%d, |W1| = 2' % (k - 1), identical=bool((F == A).all()), n=len(A),
                         M_is_clique_in_G=True)
        print(cell, out[cell], flush=True)
    # (8,19)
    A813, _ = adj_of('8,13'); Aaux, _ = adj_of('aux_7,8'); A819, _ = adj_of('8,19')
    Mx = comp(mat204)
    F = thm3_from_text(A813, comp(Aaux), list(range(204)), list(range(204)), 102)
    out['8,19'] = dict(rule='XSR2 Thm 3, G = (8,13;816), H = complement of (7,8;216), M = complement of Mathon(204) on vertices 0..203 of both',
                       identical=bool((F == A819).all()), n=len(A819),
                       M_induced_in_G=bool((A813[:204, :204] == Mx).all()), M_induced_in_H=bool((comp(Aaux)[:204, :204] == Mx).all()))
    print('8,19', out['8,19'], flush=True)
    json.dump(out, open(os.path.join(HERE, 'logs', 'structure_check.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
