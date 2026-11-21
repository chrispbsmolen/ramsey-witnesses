#!/usr/bin/env python3
"""xxer7_indep.py - second, independent implementation of the colouring F in the proof of Theorem 7 of
X. Xu, Z. Xie, G. Exoo, S. P. Radziszowski, Constructive lower bounds on classical multicolor Ramsey numbers,
Electron. J. Combin. 11 (2004) #R35, page 11.  Written from the text of the paper.  Pure Python: no numpy,
no verify_ramsey, no constructions.py; the input file is parsed here.

Paper (p.11): G is a (k, l-1; m)-graph on v_1..v_m.  V(F) = U_1 + U_2 + U_3 + U_4, U_i = {(u_i, v_j) : 1 <= j <= m}.
  (a) inside U_i:  F((u_i,v_j1),(u_i,v_j2)) = 2 if v_j1 v_j2 is an edge of G, otherwise 3;
  (b) between U_i1 and U_i2 with i1 in {1,2}, i2 in {3,4}:
          1 if j1 = j2;  2 if v_j1 v_j2 is an edge of G;  3 if it is not an edge and j1 != j2;
  (c) for (i1,i2) in {(1,2),(3,4)}:  3 if j1 = j2;  1 if j1 != j2.
Claim of the theorem: F has no triangle in colour 1, no K_k in colour 2, no K_l in colour 3 (for k >= 3, l >= 5).

Input: n lines of n characters 0/1, '1' = edge of G.  Output: 4m lines of 4m digits; vertex (u_i, v_j) has index
(i-1)m + (j-1); the digit is the paper's colour minus 1; the diagonal is written '0' (same file format as
build_xxer7.py, so the two outputs can be compared byte for byte).
usage: xxer7_indep.py G.matrix01 OUT.colormat"""
import sys, hashlib

src, out = sys.argv[1], sys.argv[2]
rows = [line.strip() for line in open(src) if line.strip()]
m = len(rows)
assert all(len(r) == m and set(r) <= {'0', '1'} for r in rows)
edge = [[r[j] == '1' for j in range(m)] for r in rows]
for a in range(m):
    assert not edge[a][a]
    for b in range(m):
        assert edge[a][b] == edge[b][a]


def colour(i1, j1, i2, j2):
    """Paper colour (1, 2 or 3) of the edge {(u_i1, v_j1), (u_i2, v_j2)}; i in 1..4, j in 1..m."""
    if i1 > i2:
        i1, j1, i2, j2 = i2, j2, i1, j1
    if i1 == i2:                                   # (a)
        return 2 if edge[j1 - 1][j2 - 1] else 3
    if (i1, i2) in ((1, 2), (3, 4)):               # (c)
        return 3 if j1 == j2 else 1
    assert i1 in (1, 2) and i2 in (3, 4)           # (b)
    if j1 == j2:
        return 1
    return 2 if edge[j1 - 1][j2 - 1] else 3


n = 4 * m
lines = []
for x in range(n):
    i1, j1 = x // m + 1, x % m + 1
    row = []
    for y in range(n):
        if x == y:
            row.append('0'); continue
        i2, j2 = y // m + 1, y % m + 1
        c = colour(i1, j1, i2, j2)
        assert c == colour(i2, j2, i1, j1)
        row.append(str(c - 1))
    lines.append(''.join(row))
with open(out, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('n=%d input_sha256=%s out_sha256=%s' % (n, hashlib.sha256(open(src, 'rb').read()).hexdigest(),
                                              hashlib.sha256(open(out, 'rb').read()).hexdigest()))
