"""Checks that the reduced subproblem built by cyclo_reduce.py (from the row's graph6 file) is the same graph, byte for
byte, as the input cube_alpha.py (hunt2_two_colour, used in Mac wave 8 J2) gives clique.c for the same p and w.
cube_alpha.py builds Cay(Z_p, cubes) from p alone and passes the complement induced on the common non-neighbours of
0 and w, in increasing vertex order.  Usage: python3 subproblem_identity.py G6 P W   Appends to logs/subproblem_identity.jsonl."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L
g6, p, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
A = L.load_g6(g6)
M = ~A & ~np.eye(p, dtype=bool)
V = np.flatnonzero(M[0] & M[w]); V = V[(V != 0) & (V != w)]
mine = L.graph_text(M[np.ix_(V, V)])
H = {pow(x, 3, p) for x in range(1, p)}
nonadj = lambda x, y: x != y and ((x - y) % p) not in H
VV = [v for v in range(p) if nonadj(v, 0) and nonadj(v, w)]
theirs = ('%d\n' % len(VV) + '\n'.join(''.join('1' if nonadj(a, b) else '0' for b in VV) for a in VV) + '\n').encode()
L.log('subproblem_identity.jsonl', dict(file=os.path.basename(g6), sha256=L.sha256_file(g6), p=p, w=w, vertices=len(V),
      cyclo_reduce_input_sha256=L.sha256_bytes(mine), cube_alpha_input_sha256=L.sha256_bytes(theirs), identical=(mine == theirs)))
