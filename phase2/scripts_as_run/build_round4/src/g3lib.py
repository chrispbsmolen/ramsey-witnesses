"""Constructions for the G3 cells (two-colour graphs glued from smaller witnesses).

Conventions: a "(a,b)-graph" is a graph with no K_a and no independent set of size b.
All graphs are 0/1 numpy adjacency matrices (symmetric, zero diagonal).

  t9(A)       XXER Theorem 9 (EJC 11 (2004) #R35, pp. 15-16, construction of Theorem 7 p. 11 with
              colours 1 and 2 merged).  A: a (k, l-1)-graph on m vertices.  Returns a graph on 4m
              vertices, claimed to be a (2k-1, l)-graph (so R(2k-1, l) >= 4R(k, l-1) - 3).
              Vertex (i, j), i = 0..3 (the paper's U_1..U_4), j = 0..m-1, has index i*m + j.
              Edges: inside U_i a copy of A; between U_i1 (i1 in {1,2}) and U_i2 (i2 in {3,4}):
              j1 = j2 or j1 ~ j2 in A (colours 1, 2); between U_1,U_2 and between U_3,U_4:
              j1 != j2 (colour 1).  Everything else (colour 3) is a non-edge.

  xsr2_thm3(G, H, phiG, phiH, m1)
              XSR2 Theorem 3 (SIAM J. Discrete Math. 25 (2011) 394-400; preprint p. 4-6,
              https://www.cs.rit.edu/~spr/PUBL/paper68.pdf).  G a (k,s)-graph, H a (k,t)-graph,
              M the graph induced by G on the vertex list phiG, which must equal (with the same
              order) the graph induced by H on phiH.  W1 = the first m1 vertices of M, W2 = the rest.
              Vertex order of the result: V(G) (p), V(H) (q), W (m).  Edges: those of G, H,
              M[W1], M[W2]; w_i ~ u_j iff u_i ~ u_j in G (u_i = phiG[i], u_j != u_i); w_i ~ v_j iff
              v_i ~ v_j in H; the matching u_i ~ v_i.  Claimed (k, s+t-1)-graph on p+q+m vertices
              under the theorem's condition on (W1, W2).
"""
import numpy as np, hashlib, gzip, io


def t9(A):
    A = np.asarray(A, dtype=np.uint8); m = len(A)
    I = np.eye(m, dtype=np.uint8)
    J = np.ones((m, m), dtype=np.uint8)
    cross = np.where((A + I) > 0, 1, 0).astype(np.uint8)   # j1 = j2 or adjacent
    pair = (J - I).astype(np.uint8)                          # j1 != j2
    Z = None
    blocks = [[A, pair, cross, cross],
              [pair, A, cross, cross],
              [cross, cross, A, pair],
              [cross, cross, pair, A]]
    F = np.block(blocks).astype(np.uint8)
    np.fill_diagonal(F, 0)
    assert (F == F.T).all()
    return F


def t9_lift_perm(perm_m, m):
    """an automorphism of A acting on every block U_i simultaneously"""
    perm_m = np.asarray(perm_m)
    return np.concatenate([i * m + perm_m for i in range(4)])


def t9_block_perms(m):
    """the block permutations (U1 U2), (U3 U4), (U1 U3)(U2 U4); as vertex permutations"""
    out = []
    for bp in ([1, 0, 2, 3], [0, 1, 3, 2], [2, 3, 0, 1]):
        out.append(np.concatenate([bp[i] * m + np.arange(m) for i in range(4)]))
    return out


def xsr2_thm3(G, H, phiG, phiH, m1):
    G = np.asarray(G, dtype=np.uint8); H = np.asarray(H, dtype=np.uint8)
    p, q, m = len(G), len(H), len(phiG)
    phiG = list(phiG); phiH = list(phiH)
    assert len(phiH) == m and 0 < m1 < m
    assert len(set(phiG)) == m and len(set(phiH)) == m
    MG = G[np.ix_(phiG, phiG)]; MH = H[np.ix_(phiH, phiH)]
    if not (MG == MH).all(): raise ValueError('phiG and phiH do not induce the same labelled graph M')
    n = p + q + m
    F = np.zeros((n, n), dtype=np.uint8)
    F[:p, :p] = G
    F[p:p + q, p:p + q] = H
    W = p + q
    # M[W1] and M[W2] only, no edges between W1 and W2
    for a in range(m):
        for b in range(m):
            if a != b and MG[a][b] and ((a < m1) == (b < m1)):
                F[W + a][W + b] = 1
    for i in range(m):
        ui, vi = phiG[i], phiH[i]
        for j in range(p):
            if j != ui and G[ui][j]: F[W + i][j] = F[j][W + i] = 1
        for j in range(q):
            if j != vi and H[vi][j]: F[W + i][p + j] = F[p + j][W + i] = 1
        F[ui][p + vi] = F[p + vi][ui] = 1          # matching u_i - v_i
    np.fill_diagonal(F, 0)
    assert (F == F.T).all()
    return F


def complement(A):
    A = np.asarray(A, dtype=np.uint8)
    B = (1 - A).astype(np.uint8); np.fill_diagonal(B, 0); return B


def g6_bytes(A):
    import networkx as nx
    return nx.to_graph6_bytes(nx.from_numpy_array(np.asarray(A, dtype=np.int64)), header=False)


def is_automorphism(A, perm):
    perm = np.asarray(perm)
    return bool((A[np.ix_(perm, perm)] == A).all())


def orbit_of_0(n, gens):
    seen = {0}; stack = [0]
    while stack:
        x = stack.pop()
        for g in gens:
            y = int(g[x])
            if y not in seen: seen.add(y); stack.append(y)
    return len(seen)


def sha256(b): return hashlib.sha256(b).hexdigest()
