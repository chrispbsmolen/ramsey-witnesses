"""XuR1 Theorem 1 on small primes: build M_p' (3p+6 vertices) and check with both checkers that
no colour has K_{alpha_p + 2}; also that M_p (3p+3) has clique number exactly alpha_p + 1 (Mathon)."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, networkx as nx, lib, constructions as K
V = lib.V
out = []
for p in [int(x) for x in sys.argv[1:]]:
    t0 = time.time()
    beta = K.primitive_root(p)
    H, _ = K.cubic_residue_colouring(p, beta)
    a = max(len(q) for q in nx.find_cliques(nx.from_numpy_array((H == 0).astype(int))))
    C, info = K.xur1(p)
    k = a + 2
    v = V.verify(C, [k, k, k])
    om = {c: max(len(q) for q in nx.find_cliques(nx.from_numpy_array((C == c).astype(int)))) for c in range(3)}
    M = C[:3 * p + 3, :3 * p + 3]
    omM = {c: max(len(q) for q in nx.find_cliques(nx.from_numpy_array((M == c).astype(int)))) for c in range(3)}
    rec = dict(p=p, beta=beta, alpha_p=a, n=len(C), claim='R(%d,%d,%d) > %d' % (k, k, k, len(C)),
               verify_ramsey=v['verdict'], nx_omega=om, nx_ok=all(w < k for w in om.values()),
               omega_Mp_recoloured=omM, seconds=round(time.time() - t0, 1))
    print(json.dumps(rec), flush=True); out.append(rec)
open(os.path.join(lib.OUT, 'logs', 'xur1_small.jsonl'), 'a').write(''.join(json.dumps(r) + '\n' for r in out))
