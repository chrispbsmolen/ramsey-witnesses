"""Timing of the full (no symmetry) clique.c search, one colour, on the doubling of Q_p for small p, to
extrapolate verify_ramsey.py on the G2 graphs.  Usage: python3 time_G2_full.py P... (k = omega(Q_p) + 2)"""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, constructions as K, build_G2 as B
V = lib.V
for p in map(int, sys.argv[1:]):
    w = B.omega(p)[0]; k = w + 2; C = K.paley_doubling(p)
    for c in (1, 0):
        t0 = time.time()
        try: r = V.has_clique(C, c, k, timeout=280)[0]; st = 'done'
        except subprocess.TimeoutExpired: r, st = None, 'timeout 280 s'
        rec = dict(p=p, n=len(C), omega_Qp=w, k=k, colour=c, has_K_k=r, status=st, seconds=round(time.time() - t0, 1))
        print(json.dumps(rec), flush=True)
        open(os.path.join(lib.OUT, 'logs', 'G2_full_timing.jsonl'), 'a').write(json.dumps(rec) + '\n')
