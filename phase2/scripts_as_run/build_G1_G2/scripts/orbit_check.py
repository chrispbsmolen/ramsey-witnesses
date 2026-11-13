"""Exact clique checks reduced by automorphisms that are verified here, never assumed.

Given a colouring C, a list of permutations `gens` of its vertices (each checked to preserve every
colour: C[g(i)][g(j)] == C[i][j] for all i, j) and, per orbit representative r, generators of a
subgroup fixing r (also checked), a K_k in colour c exists iff for some vertex-orbit representative r
and some orbit representative s of Stab(r) on N_c(r), the common neighbourhood N_c(r) & N_c(s) holds a
K_{k-2} in colour c.  (Any K_k can be moved by the group to contain r, then by Stab(r) to contain s.)
Each of these small searches is run twice: clique.c (through verify_ramsey.has_clique) and networkx
maximal-clique enumeration (the crosscheck.py method).  Both must say 'none'.
"""
import sys, os, json, time
import numpy as np, networkx as nx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
V = lib.V


def check_aut(C, g):
    g = np.asarray(g)
    assert sorted(g.tolist()) == list(range(len(C))), 'not a permutation'
    return bool((C[np.ix_(g, g)] == C).all())


def orbits(n, gens, points=None):
    parent = list(range(n))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for g in gens:
        for i in range(n):
            a, b = find(i), find(int(g[i]))
            if a != b: parent[a] = b
    pts = range(n) if points is None else points
    reps = {}
    for i in pts: reps.setdefault(find(i), i)
    return sorted(reps.values())


def nx_omega_split(A):
    """Clique number by networkx maximal-clique enumeration, split by smallest vertex (exact: a clique's
    other vertices are later neighbours of its smallest vertex)."""
    best = 0
    for v in range(len(A)):
        nb = [u for u in np.nonzero(A[v])[0].tolist() if u > v]
        w = 1
        if nb:
            w = 1 + max(len(q) for q in nx.find_cliques(nx.from_numpy_array(A[np.ix_(nb, nb)].astype(int))))
        best = max(best, w)
    return best


NX_MAX = 10 ** 9      # networkx is skipped (recorded as not run) on subproblems with more vertices


def search(C, sub, colour, size, nx_limit=None):
    """clique.c and networkx on the colour-`colour` graph induced on `sub` (list of vertices)."""
    S = C[np.ix_(sub, sub)]
    t0 = time.time()
    found_c = V.has_clique(S, colour, size)[0] if size >= 1 and len(sub) >= size else False
    t1 = time.time()
    if len(sub) > NX_MAX:
        return dict(n_sub=len(sub), size=size, clique_c=bool(found_c), nx_omega=None, nx_found=False,
                    nx='not run (subproblem larger than NX_MAX=%d)' % NX_MAX, sec_c=round(t1 - t0, 1))
    w = nx_omega_split(S == colour)
    t2 = time.time()
    return dict(n_sub=len(sub), size=size, clique_c=bool(found_c), nx_omega=w, nx_found=w >= size,
                sec_c=round(t1 - t0, 1), sec_nx=round(t2 - t1, 1))


def reduced_check(C, k, colours, gens, stab_gens, label, levels=2, log=None):
    n = len(C)
    for g in gens: assert check_aut(C, g), 'generator is not an automorphism'
    reps = orbits(n, gens)
    out = dict(label=label, n=n, k=k, vertex_orbit_reps=reps, searches=[])
    ok = True
    for c in colours:
        for r in reps:
            Nr = np.nonzero(C[r] == c)[0]
            if levels == 1:
                res = search(C, Nr.tolist(), c, k - 1)
                res.update(colour=c, r=int(r)); out['searches'].append(res)
                ok &= not res['clique_c'] and not res['nx_found']
                print(json.dumps(res), flush=True); continue
            sg = stab_gens.get(r, [])
            for g in sg:
                assert g[r] == r and check_aut(C, g), 'bad stabiliser generator'
            sreps = orbits(n, sg, points=Nr.tolist())
            for s in sreps:
                common = np.nonzero((C[r] == c) & (C[s] == c))[0].tolist()
                res = search(C, common, c, k - 2)
                res.update(colour=c, r=int(r), s=int(s))
                out['searches'].append(res)
                ok &= not res['clique_c'] and not res['nx_found']
                print(json.dumps(res), flush=True)
    out['verdict'] = 'PASS' if ok else 'FAIL'
    if log:
        open(log, 'a').write(json.dumps(dict(label=label, n=n, k=k, verdict=out['verdict'],
                                              reps=[int(x) for x in reps], searches=out['searches'],
                                              time=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
    return out
