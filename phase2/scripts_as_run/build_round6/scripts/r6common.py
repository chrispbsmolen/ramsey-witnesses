"""build_round6 helpers on top of build_round5's r5lib.py (unchanged copy, sha256 82bd650c...).
Reading a row's length file: line 1 N, then the colours c[1..N-1] of the edge-lengths (colour of {i,j} = c[|i-j|]);
.gz files are read through gzip.  Pinned SHA-256 values of the row files are those of build_round2/built/MANIFEST.json."""
import os, sys, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L

ROW = {  # cell: (row file name, pinned sha256 of the file as stored, U column of sheet Paper_Sep_2022 or 'fig1', m, k)
    'R(7,7,7,7)': ('R7^4_n94873.lengths', '3133b7b00eaf8b7b5c18c7fca70795c5c73e4aa701b5e7628d803675d992f6da', 19, 472, 7),
    'R(8,8,8,8)': ('R8^4_n182001.lengths', 'b5653bc4d1e978baefdaeee8cec17d5df50ee49f447e53a3a4a1072727f93510', 21, 650, 8),
    'R(9,9,9,9)': ('R9^4_n719203.lengths.gz', 'b4fdde975a813606812af7b51bf4ba1482a9c6bc0109be10bd9d72bab3638829', 25, 1282, 9),
    'R(5,5,5,5,5,5)': ('R5^6_n441605.lengths.gz', '9f21737f29b5c08708f77f0ce3f10629f0e34c19baca50d9a22fad73be57b9b9', 27, 977, 5),
    'R(6,6,6,6,6)': ('R6^5_n258505.lengths.gz', '29ae816508ae6f0ec76c49c8e95f148d30bffa827314c84034020bc33efe9577', 'fig1', 12, 6),
    'R(6,6,6,6,6,6)': ('R6^6_n5499101.lengths.gz', 'c5645d4c19da18d03d111bc884d5431ccbcf03b763bdadd8d947521d8e82a7e2', 15, 235, 6),
}
R64 = ('R6^4_n23501.lengths', 'a43c939da7dc68381b1674e417c003129295b07ce1189a475389b4786c18730a')
SHEET_SHA = 'c9bbd500a17bfd2d6baf5abbcb9ebdbdc69f6c4fe713675d0353d79a32401fe0'
R555_SHA = '7bcec4b858d02cb77157f8a88d61bb758a95ac69bbe4c28276fe293facd05d5f'
FIG1 = [1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2]   # Rowley AJC 81(2) Figure 1 p.251, (6,3;12)-graph, lengths 1..11


def raw_bytes(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rb') as f: return f.read()


def read_lengths(path, upto=None):
    """Return (N, c) with c[0] = 0 and c[d] the colour of length d, as a numpy int8 array.  upto: read only c[1..upto]."""
    b = raw_bytes(path)
    nl = b.index(b'\n'); N = int(b[:nl])
    body = b[nl + 1:]
    if upto is not None:
        body = body[:2 * upto + 8]   # one-digit colours separated by single spaces
        a = np.array(body.split()[:upto], dtype=np.int8)
    else:
        a = np.array(body.split(), dtype=np.int8)
        assert len(a) == N - 1, 'file holds %d lengths, expected %d' % (len(a), N - 1)
    return N, np.concatenate([[0], a]).astype(np.int8)


def sheet_column(sheet, col, m):
    import csv
    rows = list(csv.reader(open(sheet)))
    v = {int(r[1]): int(r[col]) for r in rows if len(r) > col and r[1].strip().isdigit() and r[col].strip()}
    hdr = {r[2]: r[col] for r in rows[:12] if len(r) > col and len(r) > 2 and r[2]}
    return [None] + [v[l] for l in range(1, m)], hdr


def qr_set(p):
    return {x * x % p for x in range(1, p)}


def paley(p):
    Q = qr_set(p)
    return p, np.array([0] + [1 if mu in Q else 2 for mu in range(1, p)], dtype=np.int8)


def doubled_circulant(p):
    """Pair rule recorded for V in build_round2 (H u H' of the doubling; build_linear.py cites XXER pp.12-13): vertex (x, a), a in {0,1}.
    (x,a) ~ (y,b): a == b: x-y in QR; a != b: x != y and x-y not in QR.  Map z in Z_2p -> (z mod p, z mod 2)."""
    Q = qr_set(p); n = 2 * p
    def edge(z1, z2):
        x, a = z1 % p, z1 % 2; y, b = z2 % p, z2 % 2
        return ((x - y) % p in Q) if a == b else (x != y and (x - y) % p not in Q)
    c = np.zeros(n, dtype=np.int8)
    for d in range(1, n): c[d] = 1 if edge(0, d) else 2
    circ = all(edge(z1, z2) == (c[(z2 - z1) % n] == 1) for z1 in range(n) for z2 in range(n) if z1 != z2)
    return n, c, circ
