"""Time one reduced subproblem (r = w3, s = h0, colour 1: Q_p on the residues, search K_{k-2}) of the
doubling of Q_p, with a hard time cap.  Usage: python3 time_G2_sub.py P K SECONDS"""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, lib, constructions as K
p, k, lim = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
C = K.paley_doubling(p)
sub = np.nonzero((C[0] == 1) & (C[2] == 1))[0].tolist()
t0 = time.time()
try: r = lib.V.has_clique(C[np.ix_(sub, sub)], 1, k - 2, timeout=lim)[0]; st = 'done'
except subprocess.TimeoutExpired: r, st = None, 'timeout %d s' % lim
rec = dict(p=p, n_sub=len(sub), search='K_%d' % (k - 2), found=r, status=st, seconds=round(time.time() - t0, 1))
print(json.dumps(rec)); open(os.path.join(lib.OUT, 'logs', 'G2_sub_timing.jsonl'), 'a').write(json.dumps(rec) + '\n')
