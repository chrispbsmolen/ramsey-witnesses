"""symlib.py - search S1 shared code: symmetric colouring ansatzes, exact clique search, logging.

A colouring of K_n is searched inside an ansatz given by a permutation group G on the vertices:
every edge orbit of G gets one colour.  Ansatzes ("group specs"):
  cyc:N                 Z_N acting by x -> x+1 (circulant colourings)
  bcyc:M:C              Z_M acting on C blocks of M vertices (vertex a*M+i), i -> i+1 in every block
  bcycmul:P:C:W         as bcyc with P prime, plus i -> W*i in every block (W a unit mod P)
  cycmul:N:W            Z_N plus x -> W*x (W a unit mod N)
  dih:N                 Cayley graphs of the dihedral group of order 2N (left regular action)
  dprod:A:B             Cayley graphs of D_A x Z_B (order 2AB), D_A dihedral of order 2A
  zxd:A:B               Cayley graphs of Z_A x D_B (order 2AB)
Everything is exact; no randomness except where a seed is passed.
"""
import json, os, sys, time, hashlib, itertools, random


# ------------------------------------------------------------------ groups
def _dihedral_elems(a):
    # (i, e): r^i s^e ; (i,e)*(j,f) = (i + (-1)^e j, e+f)
    return [(i, e) for e in (0, 1) for i in range(a)]


def _dmul(x, y, a):
    i, e = x; j, f = y
    return ((i + (j if e == 0 else -j)) % a, (e + f) % 2)


def group_perms(spec):
    """Return (n, generator permutations as lists, description)."""
    p = spec.split(':'); kind = p[0]
    if kind == 'cyc':
        n = int(p[1]); return n, [[(x + 1) % n for x in range(n)]], f'Z_{n}'
    if kind == 'cycmul':
        n, w = int(p[1]), int(p[2])
        return n, [[(x + 1) % n for x in range(n)], [(w * x) % n for x in range(n)]], f'Z_{n} with x->{w}x'
    if kind == 'bcyc':
        m, c = int(p[1]), int(p[2]); n = m * c
        return n, [[(v // m) * m + (v % m + 1) % m for v in range(n)]], f'Z_{m} on {c} blocks'
    if kind == 'bcycmul':
        q, c, w = int(p[1]), int(p[2]), int(p[3]); n = q * c
        g1 = [(v // q) * q + (v % q + 1) % q for v in range(n)]
        g2 = [(v // q) * q + (w * (v % q)) % q for v in range(n)]
        return n, [g1, g2], f'AGL-type: Z_{q} on {c} blocks with x->{w}x'
    if kind in ('dih', 'dprod', 'zxd'):
        if kind == 'dih':
            a = int(p[1]); els = _dihedral_elems(a)
            mul = lambda x, y: _dmul(x, y, a)
            gens = [(1 % a, 0), (0, 1)]
            desc = f'D_{a} (order {2*a})'
        elif kind == 'dprod':
            a, b = int(p[1]), int(p[2])
            els = [(d, z) for d in _dihedral_elems(a) for z in range(b)]
            mul = lambda x, y: (_dmul(x[0], y[0], a), (x[1] + y[1]) % b)
            gens = [((1 % a, 0), 0), ((0, 1), 0), ((0, 0), 1 % b)]
            desc = f'D_{a} x Z_{b} (order {2*a*b})'
        else:
            a, b = int(p[1]), int(p[2])
            els = [(z, d) for z in range(a) for d in _dihedral_elems(b)]
            mul = lambda x, y: ((x[0] + y[0]) % a, _dmul(x[1], y[1], b))
            gens = [(1 % a, (0, 0)), (0, (1 % b, 0)), (0, (0, 1))]
            desc = f'Z_{a} x D_{b} (order {2*a*b})'
        idx = {g: i for i, g in enumerate(els)}; n = len(els)
        # left regular action g: h -> g*h ; edge orbits {h, h'} <-> h^{-1}h' up to inverse
        perms = [[idx[mul(g, h)] for h in els] for g in gens]
        return n, perms, desc
    raise ValueError(spec)


def clique_image_perms(spec):
    """Vertex permutations used to copy a found clique (unit multipliers, block permutations).  Any permutation
    is sound for this purpose; these are chosen because they normalise the ansatz group."""
    from math import gcd
    p = spec.split(':'); kind = p[0]; out = []
    if kind in ('cyc', 'cycmul'):
        n = int(p[1])
        for u in range(2, n):
            if gcd(u, n) == 1: out.append([(u * x) % n for x in range(n)])
    elif kind in ('bcyc', 'bcycmul'):
        m, c = int(p[1]), int(p[2])
        units = [u for u in range(1, m) if gcd(u, m) == 1]
        for u in units:
            for bp in itertools.permutations(range(c)):
                if u == 1 and list(bp) == list(range(c)): continue
                out.append([bp[v // m] * m + (u * (v % m)) % m for v in range(m * c)])
    return out


def edge_orbits(n, gens):
    """Union-find over edges; returns (orbit id per edge index, list of orbits as edge lists)."""
    eid = lambda a, b: (a * n + b) if a < b else (b * n + a)
    parent = {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a in range(n):
        for b in range(a + 1, n):
            parent[a * n + b] = a * n + b
    for g in gens:
        for a in range(n):
            ga = g[a]
            for b in range(a + 1, n):
                x, y = find(a * n + b), find(eid(ga, g[b]))
                if x != y: parent[x] = y
    roots = {}; orb = {}
    for a in range(n):
        for b in range(a + 1, n):
            r = find(a * n + b)
            if r not in roots: roots[r] = len(roots)
            orb[(a, b)] = roots[r]
    O = [[] for _ in roots]
    for e, o in orb.items(): O[o].append(e)
    return orb, O


def vertex_orbit_reps(n, gens):
    seen = [False] * n; reps = []
    for v in range(n):
        if seen[v]: continue
        reps.append(v); st = [v]; seen[v] = True
        while st:
            x = st.pop()
            for g in gens:
                y = g[x]
                if not seen[y]: seen[y] = True; st.append(y)
    return reps


def check_perm_automorphism(C, g):
    n = len(C)
    for a in range(n):
        for b in range(a + 1, n):
            if C[a][b] != C[g[a]][g[b]]: return False
    return True


# ------------------------------------------------------------------ cliques (exact, bitsets as ints)
def colour_adj(C, c):
    n = len(C); adj = [0] * n
    for a in range(n):
        row = C[a]; m = 0
        for b in range(n):
            if b != a and row[b] == c: m |= 1 << b
        adj[a] = m
    return adj


def _greedy_bound(P, adj):
    # number of colour classes of a greedy colouring of P (upper bound on clique size in P)
    k = 0; U = P
    while U:
        k += 1; Q = U
        while Q:
            v = (Q & -Q).bit_length() - 1
            Q &= ~(1 << v); U &= ~(1 << v); Q &= ~adj[v]
    return k


def find_clique(adj, k, P, limit=1, out=None, cur=None):
    """Find up to `limit` k-cliques inside vertex set P (bitmask). Returns list of vertex lists."""
    if out is None: out = []
    if cur is None: cur = []
    if k == 0:
        out.append(list(cur)); return out
    if bin(P).count('1') < k: return out
    if k >= 3 and _greedy_bound(P, adj) < k: return out
    while P and len(out) < limit:
        v = (P & -P).bit_length() - 1
        P &= ~(1 << v)
        cur.append(v)
        find_clique(adj, k - 1, P & adj[v], limit, out, cur)
        cur.pop()
        if bin(P).count('1') < k: break
    return out


def cliques_through(adj, k, v, limit=1):
    return [[v] + c for c in find_clique(adj, k - 1, adj[v], limit)]


# ------------------------------------------------------------------ colourings
def expand(n, orb, colour_of_orbit):
    C = [[-1] * n for _ in range(n)]
    for (a, b), o in orb.items():
        C[a][b] = C[b][a] = colour_of_orbit[o]
    return C


def write_colormat(C, path):
    with open(path, 'w') as f:
        f.write('\n'.join(''.join('0' if x < 0 else str(x) for x in row) for row in C) + '\n')


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''): h.update(blk)
    return h.hexdigest()


def log_run(logfile, rec):
    rec = dict(rec); rec.setdefault('logged_at', time.strftime('%Y-%m-%dT%H:%M:%S%z'))
    with open(logfile, 'a') as f:
        f.write(json.dumps(rec, sort_keys=True) + '\n')


CLIQUE_BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'clique')


def cliques_through_c(adj, k, v, n):
    """One K_k containing v (as a list), via clique.c on the subgraph induced by v and its neighbours; [] if none.
    Used for large k where the Python search is slow.  The subgraph is relabelled, so the answer is mapped back."""
    import subprocess
    nb = [v] + [u for u in range(n) if (adj[v] >> u) & 1]
    m = len(nb)
    rows = []
    for x in nb:
        ax = adj[x]; rows.append(''.join('1' if (y != x and (ax >> y) & 1) else '0' for y in nb))
    p = subprocess.run([CLIQUE_BIN, str(k)], input='%d\n' % m + '\n'.join(rows) + '\n', capture_output=True, text=True)
    out = p.stdout.split()
    if not out or out[0] != 'FOUND': return []
    q = [nb[int(x)] for x in out[2:]][:k]
    return [q]
