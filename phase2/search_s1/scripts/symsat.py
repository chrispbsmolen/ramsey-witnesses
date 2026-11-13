#!/usr/bin/env python3
"""symsat.py - exact SAT search (CaDiCaL via python-sat) for a colouring of K_n with no monochromatic K_{k_c}
in colour c, inside a symmetric ansatz (one colour per edge orbit of a group, see symlib.group_perms).

Triangle colours (k = 3) get all their clauses up front (triangles through each vertex-orbit representative).
Colours with k >= 4 get clauses lazily (CEGAR): solve, search the model for monochromatic K_k through each
vertex-orbit representative (enough: every clique can be moved by the group onto one through a representative),
add one clause per clique found (not all its edge orbits in colour c), repeat.  Every added clause is implied
by the problem, so UNSAT is an exact negative for the ansatz, and a model with no clique found is a witness.

Restartable: the lazy clauses are appended to STATE (jsonl) as they are found and reloaded on start.
usage: symsat.py GROUP K1,K2,... SECONDS STATE OUTPREFIX LOG [--seed S] [--per R] [--label L]
       [--fix o:c,...] [--sym-break]
Exit: 0 found (OUTPREFIX.colormat written), 1 UNSAT, 3 time budget used up (resume with the same STATE).
"""
import sys, os, json, time, random, threading, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import symlib as L
from pysat.solvers import Solver


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('group'); ap.add_argument('ks'); ap.add_argument('seconds', type=float)
    ap.add_argument('state'); ap.add_argument('out'); ap.add_argument('log')
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--per', type=int, default=8)
    ap.add_argument('--label', default=''); ap.add_argument('--sym-break', action='store_true')
    ap.add_argument('--maxdeg', default='', help='c:D,... every vertex has at most D neighbours in colour c (a standard '
                    'bound such as D = R(k_others...) - 1; exact, encoded with pysat CardEnc totalizer)')
    ap.add_argument('--no-images', action='store_true', help='do not add images of found cliques under multipliers/block permutations')
    a = ap.parse_args()
    t0 = time.time(); rng = random.Random(a.seed)
    ks = [int(x) for x in a.ks.split(',')]; r = len(ks)
    n, gens, desc = L.group_perms(a.group)
    orb, O = L.edge_orbits(n, gens); reps = L.vertex_orbit_reps(n, gens)
    no = len(O)
    images = [] if a.no_images else L.clique_image_perms(a.group)
    same_k = {c: [d for d in range(r) if ks[d] == ks[c]] for c in range(r)}
    var = lambda o, c: o * r + c + 1 if r > 2 else (o + 1 if c == 1 else -(o + 1))
    S = Solver(name='cadical153')
    nclauses = 0
    def add(cl):
        nonlocal nclauses; S.add_clause(cl); nclauses += 1
    if r > 2:
        for o in range(no):
            add([var(o, c) for c in range(r)])
            for c1 in range(r):
                for c2 in range(c1 + 1, r): add([-var(o, c1), -var(o, c2)])
    # colour symmetry breaking (optional): among colours with equal k, the colour of orbit 0 is the first of its kind
    if a.sym_break and r > 2:
        firsts = {}
        for c in range(r): firsts.setdefault(ks[c], c)
        for c in range(r):
            if firsts[ks[c]] != c: add([-var(0, c)])
    # degree bounds
    from pysat.card import CardEnc, EncType
    top = no * r if r > 2 else no
    ncard = 0
    for item in [x for x in a.maxdeg.split(',') if x]:
        c, D = map(int, item.split(':'))
        for v in reps:
            lits = []
            for u in range(n):
                if u != v: lits.append(var(orb[(min(u, v), max(u, v))], c))
            enc = CardEnc.atmost(lits=lits, bound=D, top_id=top, encoding=EncType.totalizer)
            top = max(top, enc.nv)
            for cl in enc.clauses: add(cl); ncard += 1
    # eager triangle clauses
    tri = set()
    for c in range(r):
        if ks[c] != 3: continue
        for v in reps:
            for x in range(n):
                if x == v: continue
                for y in range(x + 1, n):
                    if y == v: continue
                    s = frozenset((orb[(min(v, x), max(v, x))], orb[(min(v, y), max(v, y))], orb[(x, y)]))
                    tri.add((c, s))
    for c, s in tri: add([-var(o, c) for o in s])
    ntri = len(tri)
    # reload lazy clauses
    lazy = set()
    if os.path.exists(a.state):
        for line in open(a.state):
            d = json.loads(line)
            if d.get('group') != a.group or d.get('ks') != a.ks: continue
            key = (d['c'], frozenset(d['orbits']))
            if key not in lazy:
                lazy.add(key); add([-var(o, d['c']) for o in d['orbits']])
    nreload = len(lazy)
    st = open(a.state, 'a')
    iters = 0; result = 'TIME'; found_path = None; last_nclq = None
    # CaDiCaL in python-sat cannot be interrupted: each process is bounded by the outer `timeout`, and the
    # lazy clauses already found are on disk, so a killed leg loses at most its last solve call.
    while True:
        if time.time() - t0 > a.seconds: break
        res = S.solve()
        if res is None: break
        if res is False: result = 'UNSAT'; break
        iters += 1
        model = S.get_model(); pos = set(x for x in model if x > 0)
        col = []
        for o in range(no):
            if r > 2: col.append(next(c for c in range(r) if var(o, c) in pos))
            else: col.append(1 if (o + 1) in pos else 0)
        C = L.expand(n, orb, col)
        newc = 0
        for c in range(r):
            adj = L.colour_adj(C, c)
            for v in reps:
                qs = L.cliques_through_c(adj, ks[c], v, n) if ks[c] >= 6 else L.cliques_through(adj, ks[c], v, limit=a.per)
                for q in qs:
                    # the clique itself, its images under vertex permutations (each image is again a vertex set of
                    # K_n, so its clause is implied whatever the permutation), and the same set in every colour with
                    # the same forbidden size
                    for qq in [q] + [[g[x] for x in q] for g in images]:
                        s = frozenset(orb[(min(x, y), max(x, y))] for i, x in enumerate(qq) for y in qq[i + 1:])
                        for cc in same_k[c]:
                            key = (cc, s)
                            if key in lazy: continue
                            lazy.add(key); add([-var(o, cc) for o in s]); newc += 1
                            st.write(json.dumps({'group': a.group, 'ks': a.ks, 'c': cc, 'orbits': sorted(s)}) + '\n')
        st.flush(); last_nclq = newc
        if newc == 0:
            result = 'FOUND'; found_path = a.out + '.colormat'
            L.write_colormat(C, found_path)
            with open(a.out + '.orbitcolours.json', 'w') as f:
                json.dump({'group': a.group, 'desc': desc, 'ks': ks, 'n': n, 'orbit_colours': col,
                           'orbit_reps': [O[o][0] for o in range(no)]}, f)
            break
    rec = {'method': 'symsat (CaDiCaL 1.5.3 via python-sat, lazy clique clauses)', 'label': a.label,
           'group': a.group, 'group_desc': desc, 'ks': a.ks, 'n': n, 'edge_orbits': no, 'vertex_orbits': len(reps),
           'seed': a.seed, 'per': a.per, 'image_perms': len(images), 'maxdeg': a.maxdeg, 'card_clauses': ncard, 'seconds_budget': a.seconds, 'seconds': round(time.time() - t0, 1),
           'triangle_clauses': ntri, 'lazy_clauses_total': len(lazy), 'lazy_reloaded': nreload,
           'solve_iterations': iters, 'result': result, 'file': found_path,
           'sha256': L.sha256_file(found_path) if found_path else None,
           'best_score': 0 if result == 'FOUND' else None}
    L.log_run(a.log, rec); print(json.dumps(rec))
    sys.exit({'FOUND': 0, 'UNSAT': 1}.get(result, 3))


if __name__ == '__main__':
    main()
