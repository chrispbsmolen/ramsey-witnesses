"""Shared helpers for build_round2 (Ramsey phase 2, queued recipe cells), 7 Nov 2026.

Every input is read from a file whose SHA-256 is pinned in INPUTS and checked on every load.
Linear colourings are handled as length vectors c[1..N-1] (c[0] unused): the colour of edge {i,j}
is c[|i-j|] (Rowley's 'linear', AJC 81(2) p.247 Sec.2).  File format '.lengths' (the round-1
convention of hunt_multicolour): line 1 = N, line 2 = c[1] .. c[N-1] separated by spaces.
Colours are 1..r in .lengths files.
"""
import os, sys, json, hashlib, gzip, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
CHECKER = os.path.join(OUT, 'checker')
LOGS = os.path.join(OUT, 'logs')
BUILT = os.path.join(OUT, 'built')
sys.path.insert(0, CHECKER)
P2 = '<cloud>/ramsey-p2'
REPO = P2 + '/repo'
HM = P2 + '/hunt_multicolour'

INPUTS = {
    'cubic3_127': (REPO + '/constructions/witnesses/cubic3_127_R4_4_4.txt',
                   '9fe049f9c244736135b6c476787cb7256fbe8588da7f38991fc4627b3ed10a68',
                   'repo ramsey-witnesses constructions/witnesses (Hill-Irving cyclic cubic-residue (4,4,4;127)), VERIFIED in repo coverage.csv'),
    'paley101': (REPO + '/constructions/witnesses/paley101_R6_6.g6',
                 'ebc60e8269cb2c447fe1ba42c3c8d05c788e130cdd0f63e82ca91e2d00635353',
                 'repo constructions/witnesses/paley101_R6_6.g6 (Paley Q_101 = Kalbfleisch (6,6;101))'),
    'paley281': (REPO + '/constructions/witnesses/paley281_R8_8.g6',
                 '4ab78933e6b619ba7bab6f1d6f1b9c740492a2322bfb2445a168a02d48fc978d',
                 'repo constructions/witnesses/paley281_R8_8.g6 (Paley Q_281)'),
    'paley797': (REPO + '/constructions/witnesses/paley797_R10_10.g6',
                 'b42e63a21acaa5c949d9c31096b509191c4baa410b11895bbd0a03beab135fdd',
                 'repo constructions/witnesses/paley797_R10_10.g6 (Paley Q_797)'),
    'r555_453': (HM + '/converted/julojc_atom_R5_5_5_n453.lengths',
                 '7bcec4b858d02cb77157f8a88d61bb758a95ac69bbe4c28276fe293facd05d5f',
                 'hunt_multicolour converted from Courties github.com/JuloJC/multicolour-ramsey-numbers d9ca62fe ingredients/atom_5_5_5_n453_firstrow.txt (CC0; Exoo (5,5,5;453)); VERIFIED round 1'),
    'r377_673': (HM + '/converted/rowley5_R3_7_7_n673.lengths',
                 '1ce5a5e48b66902893785ec9f5d290eb766373d61d03cf3a03d0e04c708648b4',
                 'hunt_multicolour converted from Rowley arXiv:2203.13476v3 ancillary spreadsheet col 19 (cyclic (3,7,7;673)); VERIFIED round 1'),
    'r388_940': (HM + '/converted/rowley5_R3_8_8_n940.lengths',
                 '7dac9b2152ddd14c62beea1791b3ff9a73b4e3d8b533e8ae73ebf83343418554',
                 'hunt_multicolour converted from Rowley arXiv:2203.13476v3 ancillary spreadsheet col 23 (cyclic (3,8,8;940)); VERIFIED round 1'),
    'exoo_s5': (HM + '/converted/exoo94_R3x5_n161.lengths',
                '67c70db6eeb9c2c3a33999c55e04bd4ae13647482e007a6779b7faa7099b66df',
                'hunt_multicolour converted from Exoo EJC 1 (1994) #R8 p.2 (sum-free 5-partition of [1,160]); VERIFIED round 1'),
    'rowley_cols': (HM + '/downloads/arxiv_2203.13476/cols.json',
                    'f31d27dc9334a047b1299ceae0c304dfdbfc8caa296ab6a2b92420541a44cd32',
                    'round-1 extraction (hunt_multicolour/scripts/rowley_cols.py) of sheet Paper_Sep_2022 of Rowley arXiv:2203.13476v3 ancillary spreadsheet (src tarball sha256 5041096a33d6898c116a35a102e521fb14fe872fb18c20ff7d30822ed4c396b2)'),
    'rowley_sheet': (HM + '/downloads/arxiv_2203.13476/sheets/Paper_Sep_2022.csv',
                     'c9bbd500a17bfd2d6baf5abbcb9ebdbdc69f6c4fe713675d0353d79a32401fe0',
                     'CSV export (round 1) of sheet Paper_Sep_2022, Rowley arXiv:2203.13476v3 ancillary spreadsheet'),
    'rowley_jan2021': (HM + '/downloads/arxiv_2203.13476/sheets/Jan_2021_trg(k,3).csv',
                       '53f2bf9d27f2ed4d4d93cab13b43ebc54d60519aef3b3f717d0224989f466bf9',
                       'CSV export (round 1) of sheet Jan_2021_trg(k,3), Rowley arXiv:2203.13476v3 ancillary spreadsheet'),
    'r3_22_130': (P2 + '/hunt_two_colour/witnesses/R3_22_n130_WSLX2.circ',
                  '73f79090905c8cf1139aa16c24bfc4e090169232784301628af6219edab54225',
                  'hunt_two_colour transcription of Wu-Su-Luo-Xu EJC 17 (2010) #N25 Thm 1 proof part 1) p.7 (PDF sha256 8fad308ee534abe756ab70c5e36ac0d1686d40daf8d0f7e1afe85344cb7d1b68); VERIFIED round 1'),
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def pin(name):
    path, sha, _ = INPUTS[name]
    got = sha256_file(path)
    if got != sha: raise RuntimeError('%s: sha256 %s != pinned %s' % (name, got, sha))
    return path


def input_record(name):
    path, sha, desc = INPUTS[name]
    return dict(name=name, file=path, sha256=sha, source=desc)


# ------------------------------------------------------------------ loaders (to length vectors)
def read_lengths(path):
    op = gzip.open if path.endswith('.gz') else open
    t = op(path, 'rt').read().split()
    N = int(t[0]); c = [None] + [int(x) for x in t[1:]]
    assert len(c) == N, (path, N, len(c))
    return N, c


def lengths_of(name):
    return read_lengths(pin(name))


def g6_adj(path):
    import networkx as nx
    line = open(path, 'rb').read().split()[0]
    G = nx.from_graph6_bytes(line)
    return nx.to_numpy_array(G, nodelist=sorted(G.nodes()), dtype=np.int64)


def circulant_lengths_from_adj(A, ccol_edge=1, ccol_non=2):
    """Length vector of a circulant graph (checked to be circulant): edge -> ccol_edge, non-edge -> ccol_non."""
    n = len(A)
    row = A[0]
    idx = (np.arange(n)[None, :] - np.arange(n)[:, None]) % n
    assert (A == row[idx]).all(), 'graph is not circulant'
    return n, [None] + [ccol_edge if row[d] else ccol_non for d in range(1, n)]


def colormat_lengths(path):
    """Length vector of a linear colour matrix file (repo colormat), checked linear."""
    rows = [l.strip() for l in open(path) if l.strip()]
    n = len(rows); C = np.array([[int(x) for x in r] for r in rows])
    c = [None] + [int(C[0][d]) for d in range(1, n)]
    idx = np.abs(np.arange(n)[:, None] - np.arange(n)[None, :])
    L = np.array([-1] + c[1:])[idx]
    off = idx != 0
    assert (L[off] == C[off]).all(), 'colour matrix not linear'
    return n, c


def paley_lengths(p, edge=1, non=2):
    """Paley Q_p as a length vector on Z_p: d -> edge iff d is a nonzero square mod p (p = 1 mod 4)."""
    assert p % 4 == 1
    Q = {x * x % p for x in range(1, p)}
    return p, [None] + [edge if d in Q else non for d in range(1, p)]


# ------------------------------------------------------------------ properties
def is_cyclic(N, c):
    return all(c[d] == c[N - d] for d in range(1, N))


def colours(c):
    return sorted(set(c[1:]))


def degree(N, c, col, v=0):
    """degree of vertex v in colour col of a linear colouring"""
    return sum(1 for u in range(N) if u != v and c[abs(u - v)] == col)


def write_lengths(N, c, path):
    data = ('%d\n' % N + ' '.join(map(str, c[1:])) + '\n').encode()
    if path.endswith('.gz'):
        with gzip.GzipFile(path, 'wb', mtime=0) as f: f.write(data)
    else:
        open(path, 'wb').write(data)
    return sha256_file(path), hashlib.sha256(data).hexdigest()


def log(name, rec):
    rec = dict(rec); rec.setdefault('time', time.strftime('%Y-%m-%d %H:%M:%S'))
    with open(os.path.join(LOGS, name), 'a') as f: f.write(json.dumps(rec) + '\n')
    print(json.dumps(rec)[:2000], flush=True)
