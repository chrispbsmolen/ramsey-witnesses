"""R(6,21) independence half: exact reduction alpha(F) <= alpha(G) + 1, checked on the built file.

F = G + X, X = V(H) u W = vertices 877..886 (H = M = K5).  Every independent set I of F is T u J with
T = I n X independent in F[X] and J independent in G - N_F(T).  This script, on the loaded matrix:
  1. checks F[0..876] equals the input G (file R6_20_n877_SLLLcubic.g6, SHA-256 checked);
  2. lists every independent T in F[X] (all subsets of X), and checks none has 3 or more vertices;
  3. for every T with |T| = 2 finds a vertex u of G in N_F(T) whose whole G-neighbourhood lies in N_F(T)
     ("implied": then J + u is independent in G, so |J| <= alpha(G) - 1 and |I| <= alpha(G) + 1).
|T| = 0 gives |I| <= alpha(G) and |T| = 1 gives |I| <= 1 + alpha(G).  So alpha(F) <= alpha(G) + 1, and
alpha(G) <= 19 (input check) gives no independent 21-set.  This is the argument of XSR2 Theorem 3 (preprint
p. 5, |I| <= s + t - 2 = 20) made concrete for this object.  Appends one JSON line to logs/reduce_6_21.jsonl.
"""
import os, sys, json, itertools
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import verify_ramsey as V

man = json.load(open(os.path.join(HERE, 'built', 'MANIFEST.json')))['6,21']
path = os.path.join(HERE, man['file']); assert V.sha256_file(path) == man['sha256_file']
C = V.load_g6(path); A = (C == 1).astype(np.uint8); np.fill_diagonal(A, 0)
gp = os.path.join(HERE, 'inputs', 'R6_20_n877_SLLLcubic.g6')
assert V.sha256_file(gp) == 'ef50e6ab42e3814f4abd9118d26724df25c3a4ccd819774d7add6964a8ed20be'
G = (V.load_g6(gp) == 1).astype(np.uint8); np.fill_diagonal(G, 0)
p = 877; n = len(A); X = list(range(p, n))
rec = dict(cell='6,21', sha256_file=man['sha256_file'], n=n, G_induced_on_0_876=bool((A[:p, :p] == G).all()))
indT = [c for r in range(0, len(X) + 1) for c in itertools.combinations(X, r)
        if all(not A[a][b] for a, b in itertools.combinations(c, 2))]
rec['independent_T_count_by_size'] = {str(s): sum(1 for t in indT if len(t) == s) for s in range(0, 11) if any(len(t) == s for t in indT)}
pairs = []
for t in indT:
    if len(t) != 2: continue
    NT = set(int(v) for v in range(p) if any(A[v][x] for x in t))
    u = next((u for u in sorted(NT) if set(np.nonzero(G[u])[0].tolist()) <= NT), None)
    pairs.append(dict(T=[int(x) for x in t], witness_u=u, implied=u is not None))
rec['pairs'] = pairs
rec['max_T'] = max(len(t) for t in indT)
rec['all_pairs_implied'] = all(q['implied'] for q in pairs)
rec['conclusion'] = 'alpha(F) <= alpha(G) + 1' if rec['G_induced_on_0_876'] and rec['max_T'] <= 2 and rec['all_pairs_implied'] else 'NOT ESTABLISHED'
print(json.dumps(rec))
open(os.path.join(HERE, 'logs', 'reduce_6_21.jsonl'), 'a').write(json.dumps(rec) + '\n')
