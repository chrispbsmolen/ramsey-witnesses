#!/usr/bin/env python3
"""split_check.py - exact split of the question "does colour class c of a colouring contain a K_k?" by the smallest
vertex of the clique.  A clique of k vertices whose smallest vertex is v is v together with a clique of k-1 vertices
inside P(v) = {w > v : edge vw has colour c}.  The sets of cliques for v = 0..n-1 are disjoint and cover all cliques,
so colour c has a K_k if and only if for some v the induced graph on P(v) has a K_(k-1).  No symmetry is used.
For each v in the given range the induced graph on P(v) is written out and given unchanged to one checker
(clique.c or gen0.c, compiled binaries in --bin), which is asked for a K_(k-1).  One JSON line per piece is appended
to the log: v, |P(v)|, edges, sha256 of the piece text, checker answer, seconds.  Stops at the time budget; rerun
with the next start vertex.  The coverage check is done by split_summary.py.
usage: split_check.py COLORMAT COLOURDIGIT K CHECKER(clique|gen0) V_FROM V_TO LOG --bin DIR [--budget S]"""
import sys, os, json, time, subprocess, hashlib, argparse
ap = argparse.ArgumentParser()
ap.add_argument('path'); ap.add_argument('digit'); ap.add_argument('k', type=int); ap.add_argument('checker')
ap.add_argument('v_from', type=int); ap.add_argument('v_to', type=int); ap.add_argument('log')
ap.add_argument('--bin', required=True); ap.add_argument('--budget', type=float, default=520)
a = ap.parse_args()
t_start = time.time()
rows = [l.strip() for l in open(a.path) if l.strip()]
n = len(rows); assert all(len(r) == n for r in rows)
sha = hashlib.sha256(open(a.path, 'rb').read()).hexdigest()
adj = [[(i != j and rows[i][j] == a.digit) for j in range(n)] for i in range(n)]
assert all(adj[i][j] == adj[j][i] for i in range(n) for j in range(n))
binary = os.path.join(a.bin, a.checker)
for v in range(a.v_from, a.v_to):
    if time.time() - t_start > a.budget:
        print('budget reached before v=%d' % v); break
    P = [w for w in range(v + 1, n) if adj[v][w]]
    txt = '%d\n' % len(P) + ''.join(''.join('1' if adj[x][y] else '0' for y in P) + '\n' for x in P)
    t = time.time()
    p = subprocess.run([binary, str(a.k - 1)], input=txt, capture_output=True, text=True,
                       timeout=max(5, a.budget + 60 - (time.time() - t_start)))
    ans = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else 'ERROR ' + p.stderr[:200]
    if a.checker == 'gen0': ans = ans.split(' seconds')[0]
    rec = {'file_sha256': sha, 'n': n, 'colour_digit': a.digit, 'k': a.k, 'checker': a.checker, 'v': v,
           'piece_vertices': len(P), 'piece_edges': sum(1 for x in P for y in P if x < y and adj[x][y]),
           'piece_sha256': hashlib.sha256(txt.encode()).hexdigest(), 'asked_for': a.k - 1, 'answer': ans,
           'found': ans.startswith('FOUND'), 'none': ans.startswith('NONE'), 'seconds': round(time.time() - t, 2)}
    open(a.log, 'a').write(json.dumps(rec, sort_keys=True) + '\n')
    if rec['found']:
        print('FOUND at v=%d: %s' % (v, ans)); break
print('done', a.checker, a.v_from, a.v_to, round(time.time() - t_start, 1))
