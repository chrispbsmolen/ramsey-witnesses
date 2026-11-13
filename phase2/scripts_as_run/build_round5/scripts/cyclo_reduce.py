"""R2: one reduced subproblem of a cyclotomic Cayley graph on Z_p, one checker, one process (Amendment 1 / Amendment 5).

The object is the row's own graph6 file (pinned SHA-256).  Verified on its matrix before anything is searched:
  (1) x -> x + 1 is an automorphism (the matrix is circulant, every entry checked);
  (2) x -> c x with c = g^e (g the least primitive root mod p, e = 3 for the cubic-residue graphs, e = 7 for the R(5,22)
      graph) is an automorphism: A[c x mod p][c y mod p] == A[x][y] for every pair (checked on the whole matrix);
  (3) the orbits of <c> on the neighbours of 0 and on the non-neighbours of 0 are computed on the matrix; the
      representatives are the least element of each orbit.
Then the group {x -> c^i x + b} is transitive on vertices and the stabiliser of 0 has these orbits, so a clique of size
s >= 2 in colour C (C = 'edge' or 'nonedge') can be moved to contain 0 and a representative w of an orbit in colour C;
the rest is a clique of size s - 2 in colour C on the common C-neighbours of 0 and w.  This script builds that subgraph
for one w and asks one checker (clique.c or gen0) for K_(s-2).  The full list of (side, w) subproblems is printed by
`plan`; a half is checked when every representative of that side gives NONE with both checkers.
Usage: python3 cyclo_reduce.py plan  G6 SHA P E
       python3 cyclo_reduce.py solve G6 SHA P E SIDE(edge|nonedge) S W CHECKER TIMEOUT
Appends to logs/cyclo_reduce.jsonl."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L

mode, g6, sha, p, e = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])


def order(a):
    x, k = a, 1
    while x != 1: x = x * a % p; k += 1
    return k


t0 = time.time()
got = L.sha256_file(g6)
A = L.load_g6(g6)
assert len(A) == p
g = next(a for a in range(2, p) if order(a) == p - 1)
c = pow(g, e, p)
chk = dict(sha_match=(got == sha), translation=L.is_circulant(A))
perm = (c * np.arange(p)) % p
chk['multiplier'] = bool((A[np.ix_(perm, perm)] == A).all())
assert all(chk.values()), chk
orbits = {}
for side, mask in (('edge', A[0]), ('nonedge', ~A[0])):
    rest = set(int(x) for x in np.flatnonzero(mask) if x != 0)
    reps = []
    while rest:
        w = min(rest); o, x = set(), w
        while x not in o: o.add(x); x = x * c % p
        assert o <= rest, 'orbit leaves the class'
        rest -= o; reps.append((w, len(o)))
    orbits[side] = reps
base = dict(file=os.path.basename(g6), sha256=got, p=p, primitive_root=g, multiplier='g^%d = %d' % (e, c),
            automorphism_checks=chk, orbit_reps={k: [w for w, _ in v] for k, v in orbits.items()},
            orbit_sizes={k: [n for _, n in v] for k, v in orbits.items()})
if mode == 'plan':
    import json; print(json.dumps(base))
    sys.exit(0)
side, s, w, checker, to = sys.argv[6], int(sys.argv[7]), int(sys.argv[8]), sys.argv[9], int(sys.argv[10])
assert w in base['orbit_reps'][side]
M = A if side == 'edge' else (~A & ~np.eye(p, dtype=bool))
V = np.flatnonzero(M[0] & M[w]); V = V[(V != 0) & (V != w)]
sub = M[np.ix_(V, V)]
f, out, sec = L.solve(checker, sub, s - 2, to)
rec = dict(base, side=side, claim='no K_%d in colour %s through {0,%d}' % (s, side, w), w=w, subgraph_vertices=len(V),
           checker=checker, asked='K_%d' % (s - 2), found=f, out=out, solver_seconds=sec, total_seconds=round(time.time() - t0, 1),
           result='NONE' if f is False else ('FOUND' if f else 'NOT DONE (%s)' % out))
L.log('cyclo_reduce.jsonl', rec)
