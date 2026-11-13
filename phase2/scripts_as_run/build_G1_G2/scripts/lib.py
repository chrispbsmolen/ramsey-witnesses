"""Shared helpers for the G1/G2 builds (Ramsey phase 2).

Inputs are read only from files whose SHA-256 is pinned below (repo witnesses, or the phase-1
downloads listed in repo/sources/manifest.csv).  Colourings are n x n integer matrices with
C[i][i] = -1 and colours 0..r-1, the convention of repo/verify_ramsey.py; the checker used is a
byte-identical copy of repo/verify_ramsey.py and repo/clique.c in ../checker (SHA-256 recorded
in REPORT.md), so nothing is written inside ./repo.
"""
import os, sys, hashlib, gzip
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
CHECKER = os.path.join(OUT, 'checker')
sys.path.insert(0, CHECKER)
import verify_ramsey as V            # noqa: E402  (copy of repo/verify_ramsey.py)

REPO = '<cloud>/ramsey-p2/repo'
WORK = '<cloud>/ramsey-work/downloads'
INPUTS = {
    # name: (path, sha256, loader, entry)
    'clebsch16': (REPO + '/constructions/witnesses/clebsch16_R3_3_3.txt',
                  '625befe51b8e7750a108520a68fbce8e980824bac0b0c5a301741702ad6dc1c4', 'colormat', ''),
    'cubic3_127': (REPO + '/constructions/witnesses/cubic3_127_R4_4_4.txt',
                   '9fe049f9c244736135b6c476787cb7256fbe8588da7f38991fc4627b3ed10a68', 'colormat', ''),
    'r4.7.48': (WORK + '/papers/exoo_site/r4.7.48',
                '76a2a63632d6130a68c6316bad0e5813a266120a7a513a4aeda659738dc1bdc4', 'matrix01', ''),
    'g336.60': (WORK + '/papers/exoo_tatarevic/ExT_data/g336.60',
                '67f971a84fa0a85b4a2cb5e9804a61193f7cec0a389f4ce13ee69455dc5801b5', 'colormat', ''),
    'g3310.149': (WORK + '/papers/exoo_tatarevic/ExT_data/g3310.149',
                  'cdd4eed4d7d294fb964e42464f9c8f58c6e02d3800dcf5743f4cbebafbcf27d7', 'colormat', ''),
    'g337.78': (WORK + '/papers/exoo_site/g337.78',
                'f028f8493373eb2b25b8a13a5e8424ab6db783a01e09db1cfdd6926171fd4eac', 'colormat', ''),
    'lachy_r339': (REPO + '/third_party/lachy-dauth/circulants.json',
                   '64dc61a7dbc5524332d25371f4346b9759b2c8bc8cdcc5222e7abe477f2151c9', 'circ3json', '0'),
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def load_input(name):
    path, sha, fmt, entry = INPUTS[name]
    got = sha256_file(path)
    if got != sha: raise RuntimeError('%s: SHA-256 %s does not match pinned %s' % (name, got, sha))
    return V.load(fmt, path, entry)


def colour_with_no_clique(C, size):
    """Colours of C whose class has no K_size (exact, clique.c)."""
    return [c for c in sorted(set(C[C >= 0].tolist())) if not V.has_clique(C, c, size)[0]]


def write_colormat(C, path):
    """One line per vertex, one digit per edge (colour), diagonal written as 0 and ignored by
    verify_ramsey.load_colormat.  Gzipped if path ends in .gz.  Returns SHA-256 of the file."""
    n = len(C)
    assert C.max() <= 9
    D = C.copy(); np.fill_diagonal(D, 0)
    rows = [''.join(map(str, r)) for r in D.tolist()]
    data = ('\n'.join(rows) + '\n').encode()
    if path.endswith('.gz'):
        with gzip.GzipFile(path, 'wb', mtime=0) as f: f.write(data)
    else:
        open(path, 'wb').write(data)
    return sha256_file(path)


def write_g6(C, path):
    """Two-colour matrix: colour 1 = edge.  graph6, gzipped if .gz."""
    import networkx as nx
    A = (C == 1).astype(np.int64)
    data = nx.to_graph6_bytes(nx.from_numpy_array(A), header=False)
    if path.endswith('.gz'):
        with gzip.GzipFile(path, 'wb', mtime=0) as f: f.write(data)
    else:
        open(path, 'wb').write(data)
    return sha256_file(path)


def check_matrix(C, r):
    n = len(C)
    assert C.shape == (n, n)
    assert (C == C.T).all(), 'not symmetric'
    assert (np.diag(C) == -1).all()
    off = C[~np.eye(n, dtype=bool)]
    assert off.min() >= 0 and off.max() <= r - 1, 'colours out of range'
    return True


def induced(C, k):
    """Induced subcolouring on the first k vertices."""
    return C[:k, :k].copy()
