"""Exact clique number of Paley graphs Q_p.  Q_p is arc transitive (x -> a x + b, a a nonzero
square, maps any edge to any edge), so a clique of size s >= 2 exists iff one contains the edge
{0, 1}, i.e. iff the common neighbourhood N(0) & N(1) has a clique of size s - 2.
Q_p is self-complementary, so its independence number equals its clique number."""
import sys, os, json, time, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paley import residues, is_prime
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import verify_ramsey as V
CLIQUE = V.CLIQUE

def has_clique_through_edge(p, s):
    Q = residues(p)
    if s <= 2: return True
    W = [x for x in range(2, p) if x in Q and (x - 1) % p in Q]   # common neighbours of 0 and 1
    m = len(W); idx = np.array(W)
    D = (idx[:, None] - idx[None, :]) % p
    A = np.isin(D, list(Q)).astype(np.int8); np.fill_diagonal(A, 0)
    buf = '%d\n' % m + '\n'.join(''.join('1' if v else '0' for v in row) for row in A) + '\n'
    V.ensure_solver()
    out = subprocess.run([CLIQUE, str(s - 2)], input=buf, capture_output=True, text=True).stdout
    return out.startswith('FOUND')

def omega(p, start=2):
    s = start
    while has_clique_through_edge(p, s + 1): s += 1
    return s

if __name__ == '__main__':
    res = {}
    for p in [int(x) for x in sys.argv[1:]]:
        assert is_prime(p) and p % 4 == 1
        t0 = time.time()
        # start from a known-safe lower value to save time: omega >= 2 always
        w = omega(p)
        res[p] = w
        print(json.dumps(dict(p=p, omega=w, seconds=round(time.time() - t0, 1),
                              paley_bound='R(%d,%d) >= %d' % (w + 1, w + 1, p + 1),
                              mathon_bound='R(%d,%d) >= %d' % (w + 2, w + 2, 2 * p + 3))), flush=True)
