#!/usr/bin/env python3
"""extsat.py - exact SAT extension search: keep part of a base colouring fixed and let SAT colour the rest.

Base: a colour matrix on m vertices (colormat text: one row per vertex, colour digits, '-' or any digit on the
diagonal).  The new colouring lives on m - |drop| + add vertices: the base minus the vertices in DROP, plus ADD
new vertices.  Edges between two kept base vertices keep their colour unless one end is in FREE (then they are
free too); all other edges are free variables.  Triangle colours get every triangle clause that touches a free
edge up front; colours with k >= 4 get lazy clique clauses (solve, find monochromatic K_k containing a free edge,
forbid it, repeat).  Restartable: lazy clauses go to STATE (jsonl, keyed by the run signature) and are reloaded.
UNSAT is exact for that extension problem.

usage: extsat.py BASE K1,K2,.. ADD SECONDS STATE OUTPREFIX LOG [--drop i,j,..] [--free i,j,..] [--seed S]
       [--label L] [--per R]
"""
import sys, os, json, time, random, threading, argparse, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import symlib as L
from pysat.solvers import Solver


def load_cm(path):
    rows = [l.strip() for l in open(path) if l.strip()]
    n = len(rows)
    return [[(-1 if i == j else int(rows[i][j])) for j in range(n)] for i in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base'); ap.add_argument('ks'); ap.add_argument('add', type=int); ap.add_argument('seconds', type=float)
    ap.add_argument('state'); ap.add_argument('out'); ap.add_argument('log')
    ap.add_argument('--drop', default=''); ap.add_argument('--free', default=''); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--label', default=''); ap.add_argument('--per', type=int, default=4)
    a = ap.parse_args(); t0 = time.time()
    ks = [int(x) for x in a.ks.split(',')]; r = len(ks)
    B = load_cm(a.base); m = len(B)
    drop = set(int(x) for x in a.drop.split(',') if x); free = set(int(x) for x in a.free.split(',') if x)
    keep = [v for v in range(m) if v not in drop]
    n = len(keep) + a.add
    newv = set(range(len(keep), n)) | {i for i, v in enumerate(keep) if v in free}
    sig = hashlib.sha256(json.dumps([L.sha256_file(a.base), a.ks, a.add, sorted(drop), sorted(free)]).encode()).hexdigest()[:16]
    fixed = {}; fv = {}
    for i in range(n):
        for j in range(i + 1, n):
            if i in newv or j in newv: fv[(i, j)] = len(fv)
            else: fixed[(i, j)] = B[keep[i]][keep[j]]
    var = lambda e, c: fv[e] * r + c + 1
    S = Solver(name='cadical153'); ncl = [0]
    def add(cl): S.add_clause(cl); ncl[0] += 1
    for e in fv:
        add([var(e, c) for c in range(r)])
        for c1 in range(r):
            for c2 in range(c1 + 1, r): add([-var(e, c1), -var(e, c2)])
    E = lambda x, y: (x, y) if x < y else (y, x)
    # triangle clauses touching a free edge
    ntri = 0
    for c in range(r):
        if ks[c] != 3: continue
        for x in range(n):
            for y in range(x + 1, n):
                for z in range(y + 1, n):
                    es = [E(x, y), E(x, z), E(y, z)]
                    fr = [e for e in es if e in fv]
                    if not fr: continue
                    if any(fixed[e] != c for e in es if e not in fv): continue
                    add([-var(e, c) for e in fr]); ntri += 1
    lazy = set()
    if os.path.exists(a.state):
        for line in open(a.state):
            d = json.loads(line)
            if d.get('sig') != sig: continue
            key = (d['c'], tuple(tuple(e) for e in d['edges']))
            if key not in lazy: lazy.add(key); add([-var(tuple(e), d['c']) for e in d['edges']])
    nre = len(lazy); st = open(a.state, 'a')
    L.log_run(a.log, {'event': 'leg_start', 'label': a.label, 'base': a.base, 'add': a.add, 'ks': a.ks, 'seed': a.seed, 'lazy_reloaded': nre,
                      'note': 'a leg_start with no matching end record was stopped by the 590 s process limit inside one solve call'})
    # CaDiCaL in python-sat cannot be interrupted: each process is bounded by the outer `timeout`, and the
    # lazy clauses already found are on disk, so a killed leg loses at most its last solve call.
    result = 'TIME'; iters = 0; found = None
    newlist = sorted(newv)
    while time.time() - t0 < a.seconds:
        res = S.solve()
        if res is None: break
        if res is False: result = 'UNSAT'; break
        iters += 1; pos = set(x for x in S.get_model() if x > 0)
        C = [[-1] * n for _ in range(n)]
        for e, c in fixed.items(): C[e[0]][e[1]] = C[e[1]][e[0]] = c
        for e in fv:
            c = next(c for c in range(r) if var(e, c) in pos); C[e[0]][e[1]] = C[e[1]][e[0]] = c
        newc = 0
        for c in range(r):
            adj = L.colour_adj(C, c)
            for v in newlist:
                for q in L.cliques_through(adj, ks[c], v, limit=a.per):
                    es = tuple(sorted(E(x, y) for i, x in enumerate(q) for y in q[i + 1:] if E(x, y) in fv))
                    key = (c, es)
                    if key in lazy: continue
                    lazy.add(key); add([-var(e, c) for e in es]); newc += 1
                    st.write(json.dumps({'sig': sig, 'c': c, 'edges': [list(e) for e in es]}) + '\n')
        st.flush()
        if newc == 0:
            result = 'FOUND'; found = a.out + '.colormat'; L.write_colormat(C, found); break
    rec = {'method': 'extsat (CaDiCaL 1.5.3 via python-sat, fixed base + free edges, lazy clique clauses)', 'label': a.label,
           'base': a.base, 'base_sha256': L.sha256_file(a.base), 'ks': a.ks, 'n': n, 'add': a.add, 'drop': sorted(drop),
           'free': sorted(free), 'free_edges': len(fv), 'signature': sig, 'seed': a.seed, 'seconds_budget': a.seconds,
           'seconds': round(time.time() - t0, 1), 'triangle_clauses': ntri, 'lazy_clauses_total': len(lazy),
           'lazy_reloaded': nre, 'solve_iterations': iters, 'result': result, 'file': found,
           'sha256': L.sha256_file(found) if found else None}
    L.log_run(a.log, rec); print(json.dumps(rec))
    sys.exit({'FOUND': 0, 'UNSAT': 1}.get(result, 3))


if __name__ == '__main__':
    main()
