r"""Exact decomposed check of the independence half of the XSR2 Corollary 3 graphs (cells 5,15 7,12 9,10).

F = G + X where X = V(H) u W1 u W2 (2k-2 vertices, H = M = K_{k-1}).  Every independent set I of F
splits as I = T u I_G with T = I n X independent in F[X] and I_G an independent set of G inside
V(G) \ N_F(T).  Hence
        alpha(F) = max over independent T in F[X] of  |T| + alpha(G - N_F(T)).
This script enumerates every independent T of F[X] (from F itself, by brute force over subsets of X
up to size 4; it also checks that none of size 3 exists), and for each T decides exactly, with
both checkers (clique.c via tools/verify_ramsey.has_clique, and networkx find_cliques), whether
G - N_F(T) has an independent set of size s + 1 - |T| (target: alpha(F) <= s, i.e. no independent
(s+1)-set).  T = {} is the input graph G itself (its own check, recorded separately).
  python3 decomp.py CELL TIMEOUT_PER_SUBPROBLEM
"""
import os, sys, json, time, itertools, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools')); sys.path.insert(0, HERE)
import verify_ramsey as V
import g3lib as L
from verify_built import load_built, NXCHILD

INPUT_N = {'5,15': 266, '7,12': 404, '9,10': 564, 'aux_7,8': 204}


def nx_has(X, size, T):
    tmp = os.path.join(HERE, 'logs', 'tmp_decomp.npy'); np.save(tmp, X.astype(np.uint8))
    try:
        p = subprocess.run([sys.executable, '-c', NXCHILD, tmp, str(size), '0'], capture_output=True, text=True, timeout=T)
        r = json.loads(p.stdout.strip().split('\n')[-1]); return ('FOUND' if r['found'] else 'NONE'), r
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', None
    finally:
        os.remove(tmp)


def main():
    cell, T = sys.argv[1], float(sys.argv[2])
    C, m = load_built(cell)
    k, l = [int(x) for x in cell.replace('aux_', '').split(',')]; s = l - 1
    A = (C == 1).astype(np.uint8); np.fill_diagonal(A, 0); n = len(A); p = INPUT_N[cell]
    assert n == p + 2 * k - 2
    X = list(range(p, n))
    indT = [()]
    for r in range(1, 5):
        for c in itertools.combinations(X, r):
            if all(not A[a][b] for a, b in itertools.combinations(c, 2)): indT.append(c)
    sizes = sorted({len(t) for t in indT})
    recs = []; ok = True
    for t in indT:
        if len(t) <= 1: continue
        # T = {}: alpha(G) <= s-1 is the input witness, checked separately.
        # |T| = 1: |T| + alpha(G - N(x)) <= 1 + alpha(G) <= s, implied by the input check.
        rest = [v for v in range(p) if not any(A[v][x] for x in t)]
        target = s + 1 - len(t)
        # implied case: some u in V(G) n N_F(T) whose G-neighbourhood lies inside N_F(T); then any independent
        # set J of G - N_F(T) extends by u, so |J| <= alpha(G) - 1 = s - 2 = target - 1 for |T| = 2
        NT = set(range(p)) - set(rest)
        if len(t) == 2 and any(set(np.nonzero(A[u][:p])[0]) <= NT for u in NT):
            recs.append(dict(T=[int(x) for x in t], order=len(rest), target=target, implied=True)); continue
        sub = A[np.ix_(rest, rest)]
        t0 = time.time()
        try:
            f, out = V.has_clique(V.from_adjacency(sub), 0, target, timeout=T); repo = 'FOUND' if f else 'NONE'
        except subprocess.TimeoutExpired:
            repo = 'TIMEOUT'
        t1 = time.time()
        nxr, info = nx_has(L.complement(sub), target, T)
        t2 = time.time()
        rec = dict(T=[int(x) for x in t], order=len(rest), target=target, repo=repo, repo_s=round(t1 - t0, 1), nx=nxr, nx_s=round(t2 - t1, 1))
        recs.append(rec); print(json.dumps(rec), flush=True)
        if repo != 'NONE' or nxr != 'NONE': ok = False
    if any(len(t) > 2 for t in indT): ok = False; print('independent T of size > 2 in X: not handled')
    out = dict(cell=cell, n=n, input_order=p, independent_T_sizes=sizes, n_subproblems=len(recs), all_none_both=ok,
               implied=sum(1 for r in recs if r.get('implied')), max_order=max([r['order'] for r in recs if not r.get('implied')] or [0]), sha256_file=m['sha256_file'])
    print(json.dumps(out))
    open(os.path.join(HERE, 'logs', 'decomp.jsonl'), 'a').write(json.dumps(dict(summary=out, subproblems=recs)) + '\n')


if __name__ == '__main__':
    main()
