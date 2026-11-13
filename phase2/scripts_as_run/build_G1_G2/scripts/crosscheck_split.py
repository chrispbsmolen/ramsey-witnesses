"""crosscheck.py's method (networkx maximal-clique enumeration, no code shared with clique.c) for ONE
colour class, split by smallest vertex so it can be timed, resumed and spread over processes:
every clique has a smallest vertex v and the rest of it lies in N(v) restricted to vertices > v, so
omega = 1 + max over v of omega(G[N+(v)]).  Exact; nothing is skipped.

Usage: python3 crosscheck_split.py FORMAT PATH COLOUR LO HI [--stop K] [--limit SECONDS] [--mod K R]
  --mod K R: only vertices v with v % K == R (to spread one colour over K processes).
  checks v = LO .. HI-1 and prints one JSON line {colour, lo, hi_done, omega_max, seconds}.
  --stop K: stop early (verdict FOUND) as soon as a clique of K vertices is seen.
"""
import sys, os, json, time
import numpy as np, networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'checker'))
import verify_ramsey as V

a = sys.argv[1:]
stop = None; limit = None; mod = None
if '--mod' in a: i = a.index('--mod'); mod = (int(a[i + 1]), int(a[i + 2])); del a[i:i + 3]
if '--stop' in a: i = a.index('--stop'); stop = int(a[i + 1]); del a[i:i + 2]
if '--limit' in a: i = a.index('--limit'); limit = float(a[i + 1]); del a[i:i + 2]
fmt, path, colour, lo, hi = a[0], a[1], int(a[2]), int(a[3]), int(a[4])
C = V.load(fmt, path, '0' if fmt == 'g6' else '')
A = (C == colour)
t0 = time.time(); best = 0; done = lo; status = 'done'
for v in range(lo, min(hi, len(C))):
    if mod and v % mod[0] != mod[1]: continue
    nb = [u for u in np.nonzero(A[v])[0].tolist() if u > v]
    w = 1
    if nb:
        H = nx.from_numpy_array(A[np.ix_(nb, nb)].astype(int))
        w = 1 + max(len(q) for q in nx.find_cliques(H))
    best = max(best, w); done = v + 1
    if stop and best >= stop: status = 'FOUND'; break
    if limit and time.time() - t0 > limit: status = 'stopped at limit'; break
print(json.dumps(dict(file=os.path.basename(path), colour=colour, lo=lo, mod=mod, hi_requested=hi, hi_done=done,
                      omega_max=best, status=status, seconds=round(time.time() - t0, 1))), flush=True)
