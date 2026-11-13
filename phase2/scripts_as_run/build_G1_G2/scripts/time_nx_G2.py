"""Time the networkx crosscheck (maximal-clique enumeration, split by smallest vertex) on the largest
reduced subproblem of the doubling of Q_p (r = w3, s = h0, colour 1: Q_p induced on the residues),
to estimate the cost of a networkx check.  Usage: python3 time_nx_G2.py P SECONDS"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, networkx as nx, lib, constructions as K
p, lim = int(sys.argv[1]), float(sys.argv[2])
C = K.paley_doubling(p)
sub = np.nonzero((C[0] == 1) & (C[2] == 1))[0].tolist()
A = (C[np.ix_(sub, sub)] == 1); m = len(sub)
t0 = time.time(); per = []; best = 0
for v in range(m):
    t = time.time()
    nb = [u for u in np.nonzero(A[v])[0].tolist() if u > v]
    if nb:
        H = nx.from_numpy_array(A[np.ix_(nb, nb)].astype(int)); best = max(best, 1 + max(len(q) for q in nx.find_cliques(H)))
    per.append(round(time.time() - t, 2))
    if time.time() - t0 > lim: break
rec = dict(p=p, n_sub=m, vertices_done=len(per), seconds=round(time.time() - t0, 1), first_vertex_seconds=per[:5], omega_so_far=best)
print(json.dumps(rec)); open(os.path.join(lib.OUT, 'logs', 'nx_timing_G2.jsonl'), 'a').write(json.dumps(rec) + '\n')
