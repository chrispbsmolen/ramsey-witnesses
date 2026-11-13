#!/usr/bin/env python3
"""verify_find.py - check a found colouring with both registered checkers, unreduced, plus negative controls.

Checker 1: clique.c (build_round5/tools, sha256 137a1002...9101), run on the whole graph of each colour class,
           no --sym (no symmetry reduction), and also through verify_ramsey.verify (the repository's entry point).
Checker 2: gen0.c (build_round5/tools, sha256 d82e1855...6614), whole graph of each colour class.
Controls:  (a) lowered k: each colour asked for a K_(k_c - 1) -> both checkers must answer FOUND (shows the bound
           is tight and the checkers see the graph); (b) a corrupted copy in which one edge is recoloured so that a
           forbidden clique appears (built from a K_(k_c - 1)... found in (a) plus one vertex whose missing edges
           are recoloured) -> both checkers must answer FOUND on that colour.
usage: verify_find.py COLORMAT K1,K2,.. LOG [--label L] [--tools DIR]
"""
import sys, os, json, time, subprocess, argparse, hashlib, itertools
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('ks'); ap.add_argument('log')
ap.add_argument('--label', default=''); ap.add_argument('--tools', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
a = ap.parse_args()
T = os.path.abspath(a.tools); sys.path.insert(0, T)
import verify_ramsey as V
V.CLIQUE = os.path.join(T, 'clique')
CLQ, GEN = os.path.join(T, 'clique'), os.path.join(T, 'gen0')
ks = [int(x) for x in a.ks.split(',')]
sha = hashlib.sha256(open(a.path, 'rb').read()).hexdigest()
C = V.load_colormat(a.path); n = len(C)
cols = sorted(set(C[C >= 0].tolist()))


def graph_text(A):
    return '%d\n' % len(A) + '\n'.join(''.join('1' if A[i][j] else '0' for j in range(len(A))) for i in range(len(A))) + '\n'


def run(binary, k, txt, timeout=560):
    t = time.time()
    p = subprocess.run([binary, str(k)], input=txt, capture_output=True, text=True, timeout=timeout)
    out = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else 'ERROR ' + p.stderr[:200]
    return out, round(time.time() - t, 2)


def found(out): return out.startswith('FOUND')


rec = {'label': a.label, 'file': a.path, 'sha256': sha, 'n': n, 'ks': ks, 'colours_used': len(cols),
       'clique_c_sha256': hashlib.sha256(open(os.path.join(T, 'clique.c'), 'rb').read()).hexdigest(),
       'gen0_c_sha256': hashlib.sha256(open(os.path.join(T, 'gen0.c'), 'rb').read()).hexdigest()}
# colours of the file are 0..r-1 in the order of ks (the search writes them so); check that, and also run
# verify_ramsey's own assignment search
rec['verify_ramsey'] = V.verify(C, ks)
per = []; ok = True
for c in range(len(ks)):
    A = (C == c); txt = graph_text(A); k = ks[c]
    o1, t1 = run(CLQ, k, txt); o2, t2 = run(GEN, k, txt)
    l1, u1 = run(CLQ, k - 1, txt); l2, u2 = run(GEN, k - 1, txt)
    d = {'colour': c, 'k': k, 'edges': int(A.sum() // 2), 'clique_c': o1, 'clique_c_s': t1, 'gen0': o2.split(' seconds')[0], 'gen0_s': t2,
         'control_lowered_k': {'clique_c': l1[:12], 'gen0': l2.split(' ')[0]}}
    good = (o1.startswith('NONE') and o2.startswith('NONE'))
    ctl = found(l1) and found(l2)
    # corrupted copy: take the K_(k-1) found by clique.c, add a vertex v outside it, recolour v's edges to it
    corrupt = None
    if found(l1):
        Q = [int(x) for x in l1.split()[2:]]
        v = next(x for x in range(n) if x not in Q)
        A2 = A.copy()
        for q in Q: A2[v][q] = A2[q][v] = True
        t2x = graph_text(A2); c1, _ = run(CLQ, k, t2x); c2, _ = run(GEN, k, t2x)
        corrupt = {'vertex_added': v, 'edges_recoloured': int(sum(1 for q in Q if not A[v][q])), 'clique_c': c1[:12], 'gen0': c2.split(' ')[0],
                   'detected_by_both': found(c1) and found(c2)}
    d['corrupted_copy'] = corrupt
    d['pass'] = good; d['controls_pass'] = ctl and (corrupt is None or corrupt['detected_by_both'])
    ok = ok and good and d['controls_pass']; per.append(d)
rec['per_colour'] = per
rec['verdict'] = 'PASS' if ok and rec['verify_ramsey']['verdict'] == 'PASS' else 'FAIL'
rec['claim'] = 'R(%s) > %d' % (','.join(map(str, ks)), n) if rec['verdict'] == 'PASS' else None
rec['logged_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
open(a.log, 'a').write(json.dumps(rec, sort_keys=True) + '\n'); print(json.dumps(rec, indent=1))
