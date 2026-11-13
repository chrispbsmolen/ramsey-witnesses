"""Constructions for build_round2, each written from the cited text (page references below and in
results.csv).  All work on length vectors c[1..N-1] of linear colourings (see lib2.py)."""


def giraud(cG, n, k):
    """XXER (EJC 11 (2004) #R35) Theorem 1 [Giraud 1968], p.5: from a cyclic (k1..kr; n)-colouring with
    distance partition C_i of {1..n-1}, a cyclic (k1..kr, k; m)-colouring, m = (2k-3)n - k + 2:
        D_i     = { j + lam(2n-1) : j in C_i, 0 <= lam < k-1 }            (1 <= i <= r)
        D_{r+1} = { j + lam(2n-1) : n <= j <= 2n-1, 0 <= lam < k-2 }.
    The new colour is max(colours)+1."""
    m = (2 * k - 3) * n - k + 2
    new = max(cG[1:]) + 1
    cH = [None] * m
    for lam in range(k - 1):
        for j in range(1, n):
            l = j + lam * (2 * n - 1)
            if 1 <= l <= m - 1: assert cH[l] is None; cH[l] = cG[j]
    for lam in range(k - 2):
        for j in range(n, 2 * n):
            l = j + lam * (2 * n - 1)
            if 1 <= l <= m - 1: assert cH[l] is None; cH[l] = new
    assert all(x is not None for x in cH[1:]), 'Giraud: lengths not partitioned'
    return m, cH


def rowley31(cU, m, cV, n):
    """Rowley, Australas. J. Combin. 68(3) (2017) 385-395, Sec.3 eqs (3.1)-(3.2), p.387 (same equations
    as build_G1_G2/scripts/constructions.py rowley(), here without the matrix): M = 2mn - m - n + 1;
    l = i + lam(2m-1), 1 <= i <= m-1, 0 <= lam <= n-1 gets c_U(i);  l = i + (lam-1)(2m-1), m <= i <= 2m-1,
    1 <= lam <= n-1 gets c_V(lam).  U and V must use disjoint colour names."""
    assert not (set(cU[1:]) & set(cV[1:]))
    M = 2 * m * n - m - n + 1
    cW = [None] * M
    for lam in range(n):
        for i in range(1, m):
            l = i + lam * (2 * m - 1)
            if 1 <= l <= M - 1: assert cW[l] is None; cW[l] = cU[i]
    for lam in range(1, n):
        for i in range(m, 2 * m):
            l = i + (lam - 1) * (2 * m - 1)
            if 1 <= l <= M - 1: assert cW[l] is None; cW[l] = cV[lam]
    assert all(x is not None for x in cW[1:]), 'Rowley 3.1: some length uncoloured'
    return M, cW


def rowley32(cU, m, cV, n):
    """Rowley, Australas. J. Combin. 81(2) (2021) 245-256, Theorem 3.2 and its proof, pp.248-249.
    U = U(k1..k_{q-1}, 3; m) linear with tf-template Theta = colour q = c_U(m-1) (Def. 3.1, p.248).
    V = V(...; n) linear.  phi = largest integer < min L_q.  W has order (m-1)(n-1) + 1 + phi:
      L'_s  = { l + (mu-1)(m-1) : l in L_s, 1 <= mu <= n-1 }                         (s != q)
      L''_s = L'_s u { l + (n-1)(m-1) : l in L_s, 1 <= l <= phi }
      L''_{q+s} = { l + (mu-1)(m-1) : l in L_q, 1 <= mu <= n-1, c(mu, V) = q+s }.
    Colour names of W: U's colours except q keep their names; V colour v becomes ('V', v), and the
    caller relabels.  Returns (N, cW, phi, q)."""
    q = cU[m - 1]
    Lq = [l for l in range(1, m) if cU[l] == q]
    phi = min(Lq) - 1
    N = (m - 1) * (n - 1) + 1 + phi
    cW = [None] * N
    for lam in range(1, N):
        mu = (lam - 1) // (m - 1) + 1
        l = lam - (mu - 1) * (m - 1)
        assert 1 <= l <= m - 1
        if mu <= n - 1:
            cW[lam] = cU[l] if cU[l] != q else ('V', cV[mu])
        else:
            assert mu == n and l <= phi and cU[l] != q
            cW[lam] = cU[l]
    return N, cW, phi, q


def relabel(c):
    """Map colour names to 1..r in order of first appearance of U-colours (ints, sorted) then V colours."""
    names = sorted({x for x in c[1:] if not isinstance(x, tuple)}) + sorted({x for x in c[1:] if isinstance(x, tuple)})
    lut = {v: i + 1 for i, v in enumerate(names)}
    return [None] + [lut[x] for x in c[1:]], lut


def schur_template(f, q, g, p):
    """Ageron, Casteras, Pellerin, Portella, Rimmel, Tomasik, arXiv:2112.03175v2, Theorem 2.3 and its
    proof, pp.3-5: f an S-template of width q with n+1 colours (special colour s = f(q), Def. 2.1 p.3),
    g a sum-free k-partition of [1,p].  m = min f^{-1}(s).  h on [1, pq + m - 1]:
       x = (alpha-1) q + u, u in [1,q]:  h(x) = f(u) if f(u) != s,  else  ('g', g(alpha)).
    Returns the length vector of the linear colouring of K_{pq+m} (colour of {i,j} = h(|i-j|))."""
    s = f[q]
    m = min(u for u in range(1, q + 1) if f[u] == s)
    top = p * q + m - 1
    h = [None] * (top + 1)
    for x in range(1, top + 1):
        alpha = (x - 1) // q + 1; u = x - (alpha - 1) * q
        h[x] = f[u] if f[u] != s else ('g', g[alpha])
    return top + 1, h, m, s


def check_template(cU, m):
    """Def. 3.1 (AJC 81(2) p.248): the colour of length m-1 is triangle-free (in the linear sense:
    no a, b, a+b all of that colour within 1..m-1)."""
    q = cU[m - 1]
    L = [l for l in range(1, m) if cU[l] == q]
    S = set(L)
    tf = not any((a + b) in S for a in L for b in L if a <= b and a + b <= m - 1)
    return dict(template_colour=q, size=len(L), min=min(L), triangle_free=tf)


def check_s_template(f, q):
    """Def. 2.1 of arXiv:2112.03175: partition of [1,q] into sum-free sets; for the non-special colours
    also x, y in A_i, x+y > q  =>  x+y-q not in A_i."""
    s = f[q]; ok = True
    for x in range(1, q + 1):
        for y in range(x, q + 1):
            if f[x] != f[y]: continue
            if x + y <= q and f[x + y] == f[x]: ok = False
            if f[x] != s and x + y > q and f[x + y - q] == f[x]: ok = False
    return ok
