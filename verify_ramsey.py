"""Exact verification of Ramsey lower-bound witnesses.

A witness for R(k_1, ..., k_r) > n is an r-colouring of the edges of K_n with no monochromatic
K_{k_i} in colour i.  For r = 2 that is a graph G on n vertices with clique number below k_1
and independence number below k_2.

Checks are exact: for every colour class the C program `clique` (clique.c, compiled on first
use) decides whether a clique of the forbidden size exists (bitset branch and bound with
greedy-colouring bounds).  The colour classes may be matched to the k_i in any order; all
matchings are tried.  When the colouring is circulant (invariant under i -> i + 1 mod n, which
is tested, never assumed), only cliques through vertex 0 are searched.

Loaders (the format is always given explicitly, never guessed from content):
  g6         graph6, one graph per line (McKay, our constructions); a chosen line index
  matrix01   n lines of n characters 0/1: adjacency matrix (Exoo site two-colour files)
  colormat   n lines of n digits: colour of edge ij (Exoo-Tatarevic, Tatarevic, Exoo multicolour); diagonal ignored
  npmatrix   numpy-printed 0/1 matrix with brackets (AlphaEvolve files)
  distrow    one line: colour of edge ij is c[|i - j|] (Exoo 'ch' files); n from the file name
  dimacs     DIMACS .clq edge list (Furini et al. certificates)
  circulant  distance set on Z_n: i ~ j iff (i - j) mod n or (j - i) mod n is in D
  circcsv    a labelled row (label, n, distances) of a CSV of circulants (Kuznetsov's Table 2, extracted by fetch_data.py)
  circ3json  three-colour circulant from a JSON list {n, k, A, B} (Lachy-Dauth): red A, blue B, green the rest

Usage: python3 verify_ramsey.py FORMAT PATH K1,K2,... [INDEX]
       python3 verify_ramsey.py circulant N:D1,D2,... K1,K2
"""
import os, re, sys, json, subprocess, hashlib, itertools, time, gzip
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CLIQUE = os.path.join(HERE, 'clique')


def ensure_solver():
    src = os.path.join(HERE, 'clique.c')
    if not os.path.exists(CLIQUE) or os.path.getmtime(CLIQUE) < os.path.getmtime(src):
        subprocess.run(['cc', '-O2', '-o', CLIQUE, src], check=True)


def _open(path, mode='rb'):
    return gzip.open(path, mode) if path.endswith('.gz') else open(path, mode)


def _renumber(C):
    vals = sorted(set(C[C >= 0].tolist())); remap = {v: i for i, v in enumerate(vals)}
    out = np.full(C.shape, -1, dtype=np.int64)
    for v, i in remap.items(): out[C == v] = i
    np.fill_diagonal(out, -1)
    return out


# ---------- loaders: each returns an n x n integer colour matrix C (C[i][j] in 0..r-1, C[i][i] = -1)
def from_adjacency(A):
    A = np.array(A, dtype=np.int64); n = len(A)
    if A.shape != (n, n): raise ValueError('not square')
    if not (A == A.T).all(): raise ValueError('adjacency not symmetric')
    C = np.where(A != 0, 1, 0); np.fill_diagonal(C, -1)
    return C


def g6_lines(path):
    return [l.strip() for l in _open(path) if l.strip()]


def from_g6(line):
    import networkx as nx
    G = nx.from_graph6_bytes(line)
    return from_adjacency(nx.to_numpy_array(G, nodelist=sorted(G.nodes()), dtype=int))


def load_g6(path, index=0):
    return from_g6(g6_lines(path)[index])


def load_matrix01(path):
    rows = [l.strip() for l in open(path) if l.strip()]
    rows = [r for r in rows if set(r) <= set('01 ')]
    return from_adjacency([[int(c) for c in r.replace(' ', '')] for r in rows])


def load_colormat(path):
    rows = [l.strip().replace(' ', '') for l in _open(path, 'rt') if l.strip()]
    n = len(rows)
    if any(len(r) != n for r in rows): raise ValueError('colour matrix not square: %d rows, widths %s' % (n, sorted({len(r) for r in rows})))
    C = np.array([[int(c) for c in r] for r in rows], dtype=np.int64)
    np.fill_diagonal(C, -1)
    if not (C == C.T).all(): raise ValueError('colour matrix not symmetric')
    return _renumber(C)


def load_npmatrix(path):
    txt = open(path).read()
    nums = re.findall(r'[01]', re.sub(r'[^\[\]01\s]', '', txt))
    n = int(round(len(nums) ** 0.5))
    if n * n != len(nums): raise ValueError('matrix has %d entries, not a square' % len(nums))
    return from_adjacency(np.array([int(x) for x in nums]).reshape(n, n))


def circulant_matrix(n, D):
    D = set(int(d) % n for d in D) | set((n - int(d)) % n for d in D)
    if 0 in D: raise ValueError('distance 0')
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for d in D: A[i][(i + d) % n] = 1
    return from_adjacency(A)


def load_distrow(path):
    """Exoo 'chords' files: one line of characters c[..]; colour of edge ij is c[|i-j|]
    (a distance colouring on a path, not a circulant).  Two conventions occur: the string has
    n characters (c[0] is a diagonal marker) or n - 1 (distances 1..n-1); n is read from the
    file name, which ends in .n"""
    row = [l.strip() for l in _open(path, 'rt') if l.strip()][0].replace(' ', '')
    m = re.search(r'\.(\d+)(\.gz)?$', path)
    n = int(m.group(1)) if m else len(row)
    if len(row) == n: c = [int(x) for x in row]
    elif len(row) == n - 1: c = [None] + [int(x) for x in row]
    else: raise ValueError('chord string length %d does not fit n = %d' % (len(row), n))
    C = np.array([[c[abs(i - j)] if i != j else -1 for j in range(n)] for i in range(n)], dtype=np.int64)
    return _renumber(C)


def load_dimacs(path):
    n = None; edges = []
    for l in open(path):
        p = l.split()
        if not p: continue
        if p[0] == 'p': n = int(p[2])
        elif p[0] == 'e': edges.append((int(p[1]) - 1, int(p[2]) - 1))
    A = np.zeros((n, n), dtype=np.int64)
    for a, b in edges: A[a][b] = A[b][a] = 1
    return from_adjacency(A)


def load_circ3json(path, index):
    w = json.load(open(path))['witnesses'][int(index)]
    n, A, B = w['n'], set(w['A']), set(w['B'])
    if A & B: raise ValueError('red and blue distance sets overlap')
    C = np.full((n, n), 2, dtype=np.int64)
    for i in range(n):
        for j in range(n):
            d = min((i - j) % n, (j - i) % n)
            if d in A: C[i][j] = 0
            elif d in B: C[i][j] = 1
    np.fill_diagonal(C, -1)
    return C


def circulant_key(n, D):
    """Canonical text of a circulant (n and the sorted distance set reduced to 1..n/2); its SHA-256
    identifies a circulant witness printed in a paper."""
    D = sorted({min(int(d) % n, (n - int(d)) % n) for d in D})
    return '%d:%s' % (n, ','.join(map(str, D)))


def is_circulant(C):
    """True iff C[i][j] == C[0][(j - i) mod n] for all i != j."""
    n = len(C); row = C[0]
    idx = (np.arange(n)[None, :] - np.arange(n)[:, None]) % n
    return bool((C[idx != 0] == row[idx][idx != 0]).all())


# ---------- exact clique decision through the C solver
def has_clique(C, colour, size, sym=False, timeout=3600):
    """True iff the colour class `colour` of C contains a clique of `size` vertices."""
    ensure_solver()
    n = len(C)
    A = (C == colour)
    buf = '%d\n' % n + '\n'.join(''.join('1' if A[i][j] else '0' for j in range(n)) for i in range(n)) + '\n'
    args = [CLIQUE, str(size)] + (['--sym'] if sym else [])
    p = subprocess.run(args, input=buf, capture_output=True, text=True, timeout=timeout)
    out = p.stdout.strip()
    if out.startswith('FOUND'): return True, out
    if out.startswith('NONE'): return False, out
    raise RuntimeError('clique solver: %s %s' % (out, p.stderr[:200]))


def verify(C, ks, sym=False, timeout=3600):
    """C: colour matrix; ks: forbidden clique sizes (k_1..k_r).  Returns a dict with the verdict
    PASS (no colour class contains its forbidden clique, under some matching of colours to ks)
    or FAIL."""
    t0 = time.time(); n = len(C); r = len(ks)
    colours = sorted(set(C[C >= 0].tolist()))
    res = dict(n=n, ks=list(ks), colours=len(colours))
    if not sym and is_circulant(C):
        sym = True; res['circulant'] = True   # vertex transitive, so cliques through vertex 0 suffice
    if len(colours) > r:
        res['verdict'] = 'FAIL'; res['note'] = '%d colours used, %d allowed' % (len(colours), r); return res
    cache = {}
    def hc(c, k):
        if (c, k) not in cache: cache[(c, k)] = has_clique(C, c, k, sym=sym, timeout=timeout)[0]
        return cache[(c, k)]
    ok_perm = None
    for perm in itertools.permutations(range(r), len(colours)):
        if all(not hc(colours[i], ks[perm[i]]) for i in range(len(colours))):
            ok_perm = perm; break
    res['seconds'] = round(time.time() - t0, 1)
    if ok_perm is not None:
        res['verdict'] = 'PASS'; res['assignment'] = {int(colours[i]): int(ks[ok_perm[i]]) for i in range(len(colours))}
        res['claim'] = 'R(%s) > %d' % (','.join(map(str, ks)), n)
    else:
        res['verdict'] = 'FAIL'; res['note'] = 'some colour class contains a forbidden clique under every assignment'
        res['found'] = {'%d:%d' % (c, k): v for (c, k), v in cache.items()}
    return res


def sha256_file(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode()).hexdigest()


LOADERS = dict(matrix01=load_matrix01, colormat=load_colormat, npmatrix=load_npmatrix, distrow=load_distrow, dimacs=load_dimacs)


def load(fmt, path, entry=''):
    if fmt == 'g6': return load_g6(path, int(entry or 0))
    if fmt == 'circ3json': return load_circ3json(path, entry)
    if fmt == 'circulant':
        n, ds = path.split(':'); return circulant_matrix(int(n), [int(d) for d in re.split(r'[ ,]+', ds.strip()) if d])
    if fmt == 'circcsv':
        n, D = circcsv_entry(path, entry); return circulant_matrix(n, D)
    return LOADERS[fmt](path)


def circcsv_entry(path, label):
    """Row `label` of a CSV with columns label, n, distances (space separated)."""
    import csv
    for row in csv.DictReader(open(path)):
        if row['label'] == label: return int(row['n']), [int(x) for x in row['distances'].split()]
    raise KeyError(label)


if __name__ == '__main__':
    fmt, src, ks = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')]
    entry = sys.argv[4] if len(sys.argv) > 4 else ''
    print(json.dumps(verify(load(fmt, src, entry), ks)))
