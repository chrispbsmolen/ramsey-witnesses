"""R(7,7,7) >= 3214 (XuR1): build M_1069' on 3(1069+2) = 3213 vertices; check alpha_1069 < 6 (the
paper's hypothesis, quoted from Mathon) exactly with clique.c on the cyclic colouring H_1069^3."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, lib, constructions as K
V = lib.V
p = 1069
t0 = time.time()
beta = K.primitive_root(p)
H, _ = K.cubic_residue_colouring(p, beta)
assert V.is_circulant(H)
alpha = {}
for c in range(3):
    has6 = V.has_clique(H, c, 6, sym=True)[0]
    has5 = V.has_clique(H, c, 5, sym=True)[0]
    alpha[c] = 5 if (has5 and not has6) else ('>=6' if has6 else '<5')
C, info = K.xur1(p)
assert len(C) == 3213
path = os.path.join(lib.OUT, 'built', 'R7_7_7_n3213.txt.gz')
sha = lib.write_colormat(C, path)
rec = dict(cell='7,7,7', file='built/R7_7_7_n3213.txt.gz', n=len(C), ks=[7, 7, 7], sha256=sha, p=p, beta=beta,
           alpha_H1069_per_colour=alpha, construction='XuR1 Theorem 1 (Mathon M_p + 3 vertices, Fig. 1)',
           u_names={k: list(v) for k, v in info['u_names'].items()}, seconds=round(time.time() - t0, 1),
           time=time.strftime('%Y-%m-%d %H:%M:%S'))
open(os.path.join(lib.OUT, 'logs', 'builds.jsonl'), 'a').write(json.dumps(rec) + '\n')
print(json.dumps(rec))
