"""Timing of the full (no symmetry) clique.c search for one colour of M_p' at growing p, to extrapolate
the cost of verify_ramsey.py on M_1069' (3213 vertices)."""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, lib, constructions as K
V = lib.V
for p in [int(x) for x in sys.argv[1:]]:
    beta = K.primitive_root(p); H, _ = K.cubic_residue_colouring(p, beta)
    a = 2
    while V.has_clique(H, 0, a + 1, sym=True)[0]: a += 1
    C, _ = K.xur1(p); k = a + 2
    t0 = time.time()
    try: r = V.has_clique(C, 0, k, timeout=400)[0]; st = 'done'
    except subprocess.TimeoutExpired: r = None; st = 'timeout 400 s'
    rec = dict(p=p, n=len(C), alpha_p=a, k=k, colour=0, has_K_k=r, status=st, seconds=round(time.time() - t0, 1))
    print(json.dumps(rec), flush=True)
    open(os.path.join(lib.OUT, 'logs', 'xur1_timing.jsonl'), 'a').write(json.dumps(rec) + '\n')
