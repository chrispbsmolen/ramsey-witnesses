"""(1) every built file loads back (verify_ramsey loaders) to exactly the matrix its construction gives;
(2) negative controls: in each small G1 colouring, recolour one edge so that a forbidden clique appears
    (an edge inside a maximum clique of another colour is moved to that colour's... see code) and check
    verify_ramsey reports FAIL."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, lib, constructions as K
V = lib.V; B = os.path.join(lib.OUT, 'built'); out = []
pairs = [('R7_7_7_n3213.txt.gz', 'colormat', lambda: K.xur1(1069)[0])]
for p, k in ((797, 11), (1277, 13), (1493, 14), (2741, 15), (2801, 16)):
    pairs.append(('mathon%d_R%d_%d.g6.gz' % (p, k, k), 'g6', (lambda p=p: K.paley_doubling(p))))
for f, fmt, mk in pairs:
    L = V.load(fmt, os.path.join(B, f), '0' if fmt == 'g6' else ''); M = mk()
    if fmt == 'colormat':   # loader renumbers colours in sorted order; ours are already 0..r-1
        pass
    out.append(dict(file=f, sha256=lib.sha256_file(os.path.join(B, f)), reloads_identical=bool((L == M).all())))
    print(json.dumps(out[-1]), flush=True)
# negative controls: take a maximum clique Q of the triangle-free colour c (an edge {x,y}) and a vertex z with
# C[x][z] == c; recolour {y,z} to c -> a triangle in colour c.  verify must FAIL.
for f, ks in (('R3_3_3_3_n50.txt', [3, 3, 3, 3]), ('R3_4_8_n192.txt', [3, 4, 8]), ('R3_5_7_n240.txt', [3, 5, 7]),
              ('R3_4_4_4_n380.txt', [4, 4, 4, 3]), ('R3_3_3_7_n240_demo.txt', [3, 3, 3, 7])):
    C = V.load('colormat', os.path.join(B, f))
    tri = [c for c in sorted(set(C[C >= 0].tolist())) if not V.has_clique(C, c, 3)[0]][0]
    x, y = [int(t) for t in np.argwhere(C == tri)[0]]
    z = [int(t) for t in np.nonzero(C[x] == tri)[0] if t != y and C[y][t] != tri][0]
    D = C.copy(); D[y][z] = D[z][y] = tri
    v = V.verify(D, ks)['verdict']
    out.append(dict(file=f, control='edge {%d,%d} recoloured to triangle-free colour %d' % (y, z, tri), verdict=v, expected='FAIL'))
    print(json.dumps(out[-1]), flush=True)
open(os.path.join(lib.OUT, 'logs', 'consistency.jsonl'), 'a').write(''.join(json.dumps(r) + '\n' for r in out))
