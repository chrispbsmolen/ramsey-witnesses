"""Structural check of one colour class of XuR1's M_127' (built by g1_constructions.xur1) as a (5,17)-graph.
For colour c, every x in U u W is complete (colour c) to exactly one V-block B_c(x) and anticomplete to the
other two (XuR1 property A and Figure 1).  For a pair x,y in U u W with B_c(x) = B_c(y):
 - if {x,y} has colour c: x, y + a colour-c triangle inside that block give a K5 in colour c;
 - otherwise: x, y + an independent 15-set of the other two blocks give an independent 17-set.
Usage: python3 g387_structure.py [RECOLOUR [COLOUR]].  This script lists such pairs per colour and confirms both facts with clique.c (repo copy)."""
import sys, os, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools')); sys.path.insert(0, HERE)
import verify_ramsey as V, g1_constructions as K
p = 127
RC = int(sys.argv[1]) if len(sys.argv) > 1 else 0   # colour given to the special c-edges (property C)
C, _ = K.xur1(p, c_recolour=RC)
blk = [list(range(3 + i * p, 3 + (i + 1) * p)) for i in range(3)]
YW = [0, 1, 2, 384, 385, 386]; name = {0: 'u0', 1: 'u1', 2: 'u2', 384: 'w0', 385: 'w1', 386: 'w2'}
for c in (range(3) if len(sys.argv) < 3 else [int(sys.argv[2])]):
    B = {}
    for x in YW:
        adj = [i for i in range(3) if all(C[x, v] == c for v in blk[i])]
        non = [i for i in range(3) if all(C[x, v] != c for v in blk[i])]
        assert len(adj) == 1 and len(non) == 2; B[x] = adj[0]
    pairs = [(x, y) for x, y in itertools.combinations(YW, 2) if B[x] == B[y]]
    for x, y in pairs:
        same = C[x, y] == c
        others = [v for i in range(3) if i != B[x] for v in blk[i]]
        S = C[np.ix_(others, others)]; A = (S == c).astype(int); np.fill_diagonal(A, 0)
        a15 = V.has_clique(V.from_adjacency(A), 0, 15)[0]
        In = C[np.ix_(blk[B[x]], blk[B[x]])]; A2 = (In == c).astype(int); np.fill_diagonal(A2, 0)
        tri = V.has_clique(V.from_adjacency(A2), 1, 3)[0]
        print('colour %d: pair %s,%s share block V%d; edge colour %d -> %s' % (c, name[x], name[y], B[x], C[x, y],
              ('K5 (triangle in block: %s)' % tri) if same else ('independent 17 (indep 15 in other blocks: %s)' % a15)))
