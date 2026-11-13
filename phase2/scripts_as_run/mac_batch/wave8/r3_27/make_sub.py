"""R(3,27) > 171 (Li-Li circulant), networkx independence half split over 4 processes.

The circulant G = Cay(Z_171, A) is vertex-transitive (translations; tested on the matrix here with the unchanged
verify_ramsey.is_circulant), so a maximum independent set may be taken through vertex 0:
    alpha(G) = 1 + omega(H),   H = the complement of G restricted to the non-neighbours of 0.
This is exactly the reduction xcheck.py --sym makes (H.subgraph(H.neighbors(0)) of the complement).
This script writes H as a 0/1 colour matrix (colour 1 = edge of H = non-edge of G, diagonal 0) so that
crosscheck_split.py (networkx maximal cliques, split by smallest vertex, --mod 4 R) can share it over 4 processes:
    omega(H) = max over the 4 lanes of omega_max.  PASS for the cell: omega_max <= 25 in all 4 lanes (alpha <= 26).

  python3 make_sub.py CIRC_FILE OUT_FILE      writes OUT_FILE (refuses to overwrite an existing file)
  python3 make_sub.py CIRC_FILE --check FILE  rebuilds H in memory and compares it byte for byte with FILE
Vertex i of H is the i-th non-neighbour of 0 in increasing order (the list is printed)."""
import os, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import numpy as np
import verify_ramsey as V

circ = open(sys.argv[1]).read().strip()
C = V.load('circulant', circ)
n = len(C)
assert n == 171, n
assert V.is_circulant(C), 'not circulant'
G = (C == 1)
assert int(G[0].sum()) == 26, 'degree of 0 should be 26 (|A| = 26)'
nonnb = [u for u in range(1, n) if not G[0, u]]
assert len(nonnb) == 144
Hm = ~G[np.ix_(nonnb, nonnb)]
np.fill_diagonal(Hm, False)
assert (Hm == Hm.T).all()
txt = ''.join(''.join('1' if x else '0' for x in row) + '\n' for row in Hm).encode()
sha = hashlib.sha256(txt).hexdigest()
print('circulant', circ)
print('H: %d vertices (non-neighbours of 0), %d edges, density %.4f, sha256 %s' %
      (len(nonnb), int(Hm.sum()) // 2, Hm.sum() / (len(nonnb) * (len(nonnb) - 1)), sha))
print('vertices of H (labels in Z_171):', ','.join(map(str, nonnb)))
if sys.argv[2] == '--check':
    same = open(sys.argv[3], 'rb').read() == txt
    print('CHECK', 'OK identical' if same else 'MISMATCH', sys.argv[3])
    sys.exit(0 if same else 1)
out = sys.argv[2]
if os.path.exists(out):
    sys.exit('refusing to overwrite %s' % out)
open(out, 'wb').write(txt)
print('wrote', out)
