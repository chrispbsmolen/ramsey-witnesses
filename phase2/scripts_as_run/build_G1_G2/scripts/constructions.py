"""The constructions of groups G1 and G2, each written from the cited text (page references in
REPORT.md).  Every function returns a colour matrix C (n x n, C[i][i] = -1, colours 0..r-1)."""
import numpy as np


# ---------------------------------------------------------------- Robertson / Chung (survey 6.2.b, 6.2.h)
def robertson(T, roles, G, g_roles):
    """Robertson, EJC 6 (1999) #R3, Part Two, 'The Construction' (p. 4): from an (r+2)-colouring
    T = T_{r+2} of K_{M-1} with no triangle in colours x1, x2 and no K_{k_i} in colour x_{i+2}, and a
    colouring G of K_{R(k_1..k_r)-1} in colours 4..r+3, build T_{r+3} on 3(M-1) + |G| vertices:

          A
          D  B
          E  F  C
          1  2  3  G        (rows of the last block: all 1 to V1, all 2 to V2, all 3 to V3)

    A = T(0,2,3,4,..), B = T(0,3,1,4,..), C = T(0,1,2,4,..), D = T(3,2,1,4,..), E = T(2,1,3,4,..),
    F = T(1,3,2,4,..), where T(y0, y1, y2, y3, ..) is T with diagonal entries replaced by y0 and colour
    x_i replaced by y_i.  roles[c] = role (1..r+2) of colour c of T; g_roles[c] = role j (1..r) of colour
    c of G, which becomes colour j+3.  Output colours are 1..r+3 written as 0..r+2."""
    n0 = len(T); g = len(G)
    r2 = max(roles.values()); r = r2 - 2
    def sub(y0, y1, y2):
        lut = {}
        for c, role in roles.items():
            lut[c] = {1: y1, 2: y2}.get(role, role + 1)
        X = np.empty((n0, n0), dtype=np.int64)
        for c, v in lut.items(): X[T == c] = v
        np.fill_diagonal(X, y0)
        return X
    A, B, Cc = sub(0, 2, 3), sub(0, 3, 1), sub(0, 1, 2)
    D, E, F = sub(3, 2, 1), sub(2, 1, 3), sub(1, 3, 2)
    n = 3 * n0 + g
    H = np.zeros((n, n), dtype=np.int64)
    s1, s2, s3, s4 = slice(0, n0), slice(n0, 2 * n0), slice(2 * n0, 3 * n0), slice(3 * n0, n)
    H[s1, s1] = A; H[s2, s2] = B; H[s3, s3] = Cc
    H[s2, s1] = D; H[s1, s2] = D.T
    H[s3, s1] = E; H[s1, s3] = E.T
    H[s3, s2] = F; H[s2, s3] = F.T
    H[s4, s1] = 1; H[s1, s4] = 1
    H[s4, s2] = 2; H[s2, s4] = 2
    H[s4, s3] = 3; H[s3, s4] = 3
    GG = np.zeros((g, g), dtype=np.int64)
    for c, j in g_roles.items(): GG[G == c] = j + 3
    H[s4, s4] = GG
    np.fill_diagonal(H, 0)
    assert H[~np.eye(n, dtype=bool)].min() >= 1
    H = H - 1; np.fill_diagonal(H, -1)
    return H


# ---------------------------------------------------------------- XXER Theorem 7 / Corollaries 3, 5 (survey 6.2.g)
def xxer_quadruple(G, a_colour):
    """XXER, EJC 11 (2004) #R35, Theorem 7 (p. 10-11) in the form of Corollary 3 (p. 11): G is a
    colouring of K_m in which colour a_colour plays the role of 'l-1' (no K_{l-1}, here no K_{k1-1}) and
    every other colour keeps its own forbidden clique.  F lives on U_1..U_4 (4 copies of V(G)):
      inside U_i                      : colour of G (the edges/non-edges of G in Theorem 7);
      U_i1 x U_i2, i1 in {1,2}, i2 in {3,4}: new colour 1 if j1 = j2, else the colour of G(j1, j2);
      U_1 x U_2 and U_3 x U_4          : colour a_colour ('3' in Thm 7) if j1 = j2, else new colour 1.
    The new triangle-free colour 1 is returned as colour index r (one more than G's largest colour).
    In Theorem 7 G is a (k, l-1)-graph, colour 2 = edges of G, colour 3 = non-edges of G."""
    m = len(G); new = int(G.max()) + 1
    n = 4 * m
    F = np.full((n, n), -1, dtype=np.int64)
    I = np.eye(m, dtype=bool)
    def blk(i): return slice(i * m, (i + 1) * m)
    for i in range(4):
        F[blk(i), blk(i)] = G
    cross = G.copy(); cross[I] = new
    for i1 in (0, 1):
        for i2 in (2, 3):
            F[blk(i1), blk(i2)] = cross; F[blk(i2), blk(i1)] = cross.T
    pair = np.full((m, m), new, dtype=np.int64); pair[I] = a_colour
    for i1, i2 in ((0, 1), (2, 3)):
        F[blk(i1), blk(i2)] = pair; F[blk(i2), blk(i1)] = pair.T
    np.fill_diagonal(F, -1)
    return F


def merge(C, c1, c2):
    """Corollary 5 / Theorem 9 of XXER (p. 15): merge colours c1 and c2 (c2 relabelled as c1), then
    renumber the colours to 0..r-2 keeping their order."""
    D = C.copy(); D[D == c2] = c1
    vals = sorted(set(D[D >= 0].tolist()))
    out = np.full(D.shape, -1, dtype=np.int64)
    for i, v in enumerate(vals): out[D == v] = i
    return out


# ---------------------------------------------------------------- Rowley / Giraud linear construction (survey 6.2.j)
def length_colouring(C):
    """Colour as a function of edge length |i-j| for a linear colouring (checked exactly)."""
    n = len(C); c = [None] + [int(C[0][d]) for d in range(1, n)]
    idx = np.abs(np.arange(n)[:, None] - np.arange(n)[None, :])
    L = np.array([-1] + c[1:])[idx]
    assert (L[idx != 0] == C[idx != 0]).all(), 'colouring is not linear'
    return c


def rowley(cU, m, cV, n):
    """Rowley, Australas. J. Combin. 68(3) (2017) 385-395, Section 3 (p. 387), eqs. (3.1), (3.2):
    W has M = 2mn - m - n + 1 vertices; an edge of length l = i + lam(2m-1) with 1 <= i <= m-1 gets
    the U-colour c_U(i) (3.1); a length l = i + (lam-1)(2m-1) with m <= i <= 2m-1 gets the V-colour
    c_V(lam) (3.2).  cU, cV are length colourings (lists indexed 1..m-1, 1..n-1) with disjoint colour
    names.  Returns the colour matrix and the length colouring of W."""
    M = 2 * m * n - m - n + 1
    cW = [None] * M
    for lam in range(n):                      # (3.1)
        for i in range(1, m):
            l = i + lam * (2 * m - 1)
            if 1 <= l <= M - 1: assert cW[l] is None; cW[l] = cU[i]
    for lam in range(1, n):                   # (3.2)
        for i in range(m, 2 * m):
            l = i + (lam - 1) * (2 * m - 1)
            if 1 <= l <= M - 1: assert cW[l] is None; cW[l] = cV[lam]
    assert all(x is not None for x in cW[1:]), 'some length uncoloured'
    idx = np.abs(np.arange(M)[:, None] - np.arange(M)[None, :])
    C = np.array([-1] + cW[1:], dtype=np.int64)[idx]
    return C, cW


# ---------------------------------------------------------------- Mathon cubic scheme + Xu-Radziszowski extension (XuR1)
def primitive_root(p):
    fac = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % s for s in range(2, int(q ** .5) + 1))]
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac): return g


def cubic_residue_colouring(p, beta):
    """H_p^3 of XuR1 p. 2: vertex set Z_p, edge {x,y} has colour i iff x - y = beta^(3s+i)."""
    log = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1): log[x] = e; x = x * beta % p
    D = (np.arange(p)[:, None] - np.arange(p)[None, :]) % p
    C = np.where(D == 0, -1, log[D] % 3)
    return C, log


def xur1(p, c_recolour=0):
    """Xu and Radziszowski, EJC 16 (2009) #N1, p. 2-4.  M_p: vertices U = {(0,1),(0,b),(0,b^2)},
    V_i = {(b^i, a) | a in Z_p}; edge {(x,y),(s,t)} coloured by the cubic character of xt - ys, colour c
    if 0.  M_p': add W = {w0,w1,w2} coloured as in Figure 1 (p. 4); U-U and W edges from Figure 1;
    the c-coloured edges inside V (p disjoint triangles) are recoloured with c_recolour (the paper's
    property C: any recolouring works).  Returns (colour matrix on 3p+6 vertices, info)."""
    assert p % 6 == 1
    beta = primitive_root(p)
    _, log = cubic_residue_colouring(p, beta)
    verts = [(0, 1), (0, beta), (0, beta * beta % p)]
    for i in range(3):
        bi = pow(beta, i, p)
        verts += [(bi, a) for a in range(p)]
    X = np.array([v[0] for v in verts]); Y = np.array([v[1] for v in verts])
    det = (X[:, None] * Y[None, :] - Y[:, None] * X[None, :]) % p
    nM = 3 * p + 3
    CM = np.where(det == 0, 3, log[det] % 3)          # 3 = special colour c
    np.fill_diagonal(CM, -1)
    # property checks from the paper (A and C are used below; checked, not assumed)
    Uidx = [0, 1, 2]
    Vblk = [list(range(3 + i * p, 3 + (i + 1) * p)) for i in range(3)]
    # colour of each u to each V_i must be constant
    pat = {}
    for u in Uidx:
        row = []
        for i in range(3):
            vals = set(CM[u, Vblk[i]].tolist()); assert len(vals) == 1, 'U-V not constant'
            row.append(vals.pop())
        pat[u] = tuple(row)
    c_edges = int((CM == 3).sum() // 2)
    assert c_edges == 3 * (p + 1), 'colour c should be p+1 disjoint triangles'
    # Figure 1 (p. 4): rows u0,u1,u2,w0,w1,w2; columns U (u0 u1 u2), V (V0 V1 V2), W (w0 w1 w2)
    figU = {'u0': {'u1': 0, 'u2': 1}, 'u1': {'u0': 0, 'u2': 2}, 'u2': {'u0': 1, 'u1': 2}}
    figUV = {'u0': (1, 2, 0), 'u1': (2, 0, 1), 'u2': (0, 1, 2)}
    figUW = {'u0': (0, 1, 2), 'u1': (2, 0, 1), 'u2': (1, 2, 0)}
    figWU = {'w0': (0, 2, 1), 'w1': (1, 0, 2), 'w2': (2, 1, 0)}
    figWV = {'w0': (1, 0, 2), 'w1': (0, 2, 1), 'w2': (2, 1, 0)}
    figWW = {'w0': {'w1': 0, 'w2': 1}, 'w1': {'w0': 0, 'w2': 2}, 'w2': {'w0': 1, 'w1': 2}}
    # consistency of Figure 1 with itself (symmetry of the displayed matrix)
    for wi, w in enumerate(('w0', 'w1', 'w2')):
        for ui, u in enumerate(('u0', 'u1', 'u2')):
            assert figWU[w][ui] == figUW[u][wi]
    # identify the figure's u0,u1,u2 with the vertices of U by their colours to V0,V1,V2
    name = {}
    for u in Uidx:
        hits = [f for f, t in figUV.items() if t == pat[u]]
        assert len(hits) == 1, 'U row of Figure 1 not matched'
        name[hits[0]] = u
    n = nM + 3
    C = np.full((n, n), -1, dtype=np.int64)
    C[:nM, :nM] = CM
    # recolour U-U per Figure 1 and the c-triangles inside V
    for a in ('u0', 'u1', 'u2'):
        for b, col in figU[a].items(): C[name[a], name[b]] = col
    C[(C == 3)] = c_recolour
    W = {'w0': nM, 'w1': nM + 1, 'w2': nM + 2}
    for w, wi in W.items():
        for k, u in enumerate(('u0', 'u1', 'u2')):
            C[wi, name[u]] = C[name[u], wi] = figWU[w][k]
        for i in range(3):
            C[wi, Vblk[i]] = figWV[w][i]; C[Vblk[i], wi] = figWV[w][i]
        for w2, col in figWW[w].items(): C[wi, W[w2]] = col
    np.fill_diagonal(C, -1)
    assert (C == C.T).all() and C[~np.eye(n, dtype=bool)].min() >= 0
    return C, dict(p=p, beta=beta, u_names={k: verts[v] for k, v in name.items()})


# ---------------------------------------------------------------- Shearer-Mathon doubling of Q_p (survey 2.2.c)
def quadratic_residues(p):
    return np.array(sorted({x * x % p for x in range(1, p)}))


def paley_doubling(p):
    """2p + 2 vertices: w1, w3, copy H = Z_p, copy H' = Z_p.  As stated in XXER p. 12-13 (proof of
    Theorem 8, restricted to the two colours of the Shearer-Mathon doubling): inside H and H' the
    Paley graph Q_p (x ~ y iff x - y is a quadratic residue); x ~ y' iff x - y is a non-residue
    (F(x,y') = 1 iff H(x,y) = 2), x and x' not adjacent; w1 adjacent to all of H', w3 to all of H,
    w1, w3 not adjacent.  Vertex order: w3, w1, H, H' (so that vertex 0 is joined to H, as in
    repo/constructions/paley.py mathon(p, 'nonres', 0, 0)).  Colour 1 = edge."""
    assert p % 4 == 1
    QR = np.zeros(p, dtype=bool); QR[quadratic_residues(p)] = True
    D = (np.arange(p)[:, None] - np.arange(p)[None, :]) % p
    P = QR[D]
    N = (~QR[D]) & (D != 0)
    n = 2 * p + 2
    A = np.zeros((n, n), dtype=np.int64)
    A[2:2 + p, 2:2 + p] = P; A[2 + p:, 2 + p:] = P
    A[2:2 + p, 2 + p:] = N; A[2 + p:, 2:2 + p] = N.T
    A[0, 2:2 + p] = A[2:2 + p, 0] = 1
    A[1, 2 + p:] = A[2 + p:, 1] = 1
    C = A.copy(); np.fill_diagonal(C, -1)
    return C
