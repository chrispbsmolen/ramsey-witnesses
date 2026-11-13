"""Check one colour class of a circulant two-colouring with verify_ramsey.has_clique (clique.c, --sym).
Usage: python3 onecolour.py N D1,D2,... COLOUR SIZE TIMEOUT
COLOUR 1 = the listed distances, 0 = the complement."""
import sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import verify_ramsey as V
n = int(sys.argv[1]); D = [int(x) for x in sys.argv[2].split(',')]
col, size, to = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
C = V.circulant_matrix(n, D)
assert V.is_circulant(C)
t = time.time()
try:
    r = V.has_clique(C, col, size, sym=True, timeout=to)
    print('n=%d colour=%d K%d: %s (%s) %.1fs' % (n, col, size, 'FOUND' if r[0] else 'NONE', r[1][:80], time.time() - t))
except Exception as e:
    print('n=%d colour=%d K%d: not completed (%s) %.1fs' % (n, col, size, type(e).__name__, time.time() - t))
