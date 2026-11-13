"""Second implementation of the two gluing constructions, written for build_round4 directly from the
papers' wording.  Pure Python, edge sets of vertex pairs; shares no code with g3lib.py (numpy blocks).

  thm9_edges(m, E)       XXER, EJC 11 (2004) #R35.  Theorem 7 colouring F (proof, p. 11): vertices
                         (u_i, v_j), i = 1..4, j = 1..m, of a (k, l-1; m)-graph G with edge set E.
                           inside U_i:            colour 2 if v_j1 v_j2 in E(G), else 3
                           U_i1 - U_i2, i1 in {1,2}, i2 in {3,4}:
                                                  1 if j1 = j2; 2 if v_j1 v_j2 in E(G); else 3
                           (i1, i2) in {(1,2), (3,4)}:  3 if j1 = j2; else 1
                         Theorem 9 (p. 15): H = edges of colour 1 or 2.  Vertex (u_i, v_j) has label (i-1)*m + (j-1).
  xsr2_thm3_edges(p, EG, q, EH, u, v, m1)
                         XSR2, SIAM J. Discrete Math. 25 (2011) 394-400, preprint p. 4-5 (proof of Theorem 3):
                         V(F) = V(G) u V(H) u W, W = {w_1..w_m}; u_i = u[i-1] in V(G), v_i = v[i-1] in V(H) span
                         copies of M under u_i -> v_i -> w_i; W1 = {w_1..w_m1}, W2 = the rest.
                         E(F) = E(G) u E(H) u E(M[W1]) u E(M[W2])
                                u {w_i u_j : u_j != u_i, u_i u_j in E(G)} u {w_i v_j : v_j != v_i, v_i v_j in E(H)}
                                u {u_i v_i : i = 1..m}.
                         Labels: V(G) = 0..p-1, V(H) = p..p+q-1, w_i = p+q+i-1.
"""


def thm9_edges(m, E):
    adj = set()
    for a, b in E:
        adj.add((a, b)); adj.add((b, a))
    out = set()
    lab = lambda i, j: (i - 1) * m + j
    for i1 in range(1, 5):
        for i2 in range(i1, 5):
            for j1 in range(m):
                for j2 in range(m):
                    x, y = lab(i1, j1), lab(i2, j2)
                    if x >= y:
                        continue
                    if i1 == i2:
                        colour = 2 if (j1, j2) in adj else 3
                    elif (i1, i2) in ((1, 2), (3, 4)):
                        colour = 3 if j1 == j2 else 1
                    else:  # i1 in {1,2}, i2 in {3,4}
                        colour = 1 if j1 == j2 else (2 if (j1, j2) in adj else 3)
                    if colour in (1, 2):
                        out.add((x, y))
    return 4 * m, out


def xsr2_thm3_edges(p, EG, q, EH, u, v, m1):
    m = len(u)
    assert len(v) == m and 0 < m1 < m
    aG = set(); aH = set()
    for a, b in EG: aG.add((a, b)); aG.add((b, a))
    for a, b in EH: aH.add((a, b)); aH.add((b, a))
    # M must be induced identically on u and on v
    for i in range(m):
        for j in range(m):
            if i != j: assert ((u[i], u[j]) in aG) == ((v[i], v[j]) in aH), 'M not common'
    out = set()
    def add(x, y):
        if x != y: out.add((min(x, y), max(x, y)))
    for a, b in EG: add(a, b)
    for a, b in EH: add(p + a, p + b)
    w = lambda i: p + q + i
    for i in range(m):
        for j in range(m):
            same_part = (i < m1) == (j < m1)
            if i != j and same_part and (u[i], u[j]) in aG:   # M[W1], M[W2] (M as induced on u)
                add(w(i), w(j))
        for x in range(p):
            if x != u[i] and (u[i], x) in aG: add(w(i), x)
        for y in range(q):
            if y != v[i] and (v[i], y) in aH: add(w(i), p + y)
        add(u[i], p + v[i])
    return p + q + m, out


def complement_edges(n, E):
    return n, {(a, b) for a in range(n) for b in range(a + 1, n)} - set(E)


def adjacency_key(n, E):
    """canonical text of a labelled graph: n, then the upper triangle row by row as 0/1"""
    rows = [bytearray(b'0' * (n - a - 1)) for a in range(n)]
    for a, b in E:
        a, b = min(a, b), max(a, b)
        rows[a][b - a - 1] = ord('1')
    return b'%d\n' % n + b'\n'.join(bytes(r) for r in rows) + b'\n'
