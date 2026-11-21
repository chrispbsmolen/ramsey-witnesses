#!/usr/bin/env python3
"""verify_colouring.py - check a colouring with both checkers on the whole graph of every colour class (no symmetry,
no reduction), with negative controls.  Same conventions as phase2/check_r3337_249/scripts/verify_find.py.

Checker 1: clique.c (sha256 137a1002...9101), whole colour class, no --sym.
Checker 2: gen0.c  (sha256 d82e1855...6614), whole colour class.
Both read the same text (n, then the 0/1 matrix of the class); its SHA-256 is logged.
Controls per colour c with forbidden size k:
  (a) lowered k: both checkers asked for a K_(k-1) must answer FOUND; the clique printed by clique.c is re-checked
      here edge by edge against the file;
  (b) one-edge corruption: one edge {x,y} not of colour c is recoloured to c so that a K_k appears, when a single edge
      suffices (for k = 3: a path x-z-y of colour c; in general: a K_(k-1) of colour c found in (a) and a vertex with
      exactly one edge to it not of colour c, if the search below finds one); otherwise the vertex with the fewest
      such edges is used and the number of recoloured edges is recorded.  Both checkers must answer FOUND.
A whole-graph run that does not finish within --timeout is recorded as TIMEOUT (not as a pass); see split_check.py.
usage: verify_colouring.py FORMAT(colormat|matrix01) PATH K_for_digit0,K_for_digit1,... LOG --bin DIR [--label L]
       [--timeout S] [--skip-whole CHECKER:DIGIT ...]
For matrix01 the digits are 0 (non-edge) and 1 (edge)."""
import sys, os, json, time, subprocess, argparse, hashlib
ap = argparse.ArgumentParser()
ap.add_argument('fmt'); ap.add_argument('path'); ap.add_argument('ks'); ap.add_argument('log')
ap.add_argument('--bin', required=True); ap.add_argument('--label', default=''); ap.add_argument('--timeout', type=float, default=560)
ap.add_argument('--skip-whole', nargs='*', default=[])
a = ap.parse_args()
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, '..', 'tools')
CLQ, GEN = os.path.join(a.bin, 'clique'), os.path.join(a.bin, 'gen0')
ks = [int(x) for x in a.ks.split(',')]
rows = [l.strip() for l in open(a.path) if l.strip()]
n = len(rows); assert all(len(r) == n for r in rows)
digits = [str(d) for d in range(len(ks))]
for i in range(n):
    for j in range(n):
        if i != j:
            assert rows[i][j] in digits and rows[i][j] == rows[j][i], (i, j)
if a.fmt == 'matrix01': assert all(rows[i][i] == '0' for i in range(n))


def cls(d):
    return [[(i != j and rows[i][j] == d) for j in range(n)] for i in range(n)]


def text(A):
    return '%d\n' % len(A) + ''.join(''.join('1' if x else '0' for x in r) + '\n' for r in A)


def run(binary, k, txt):
    t = time.time()
    try:
        p = subprocess.run([binary, str(k)], input=txt, capture_output=True, text=True, timeout=a.timeout)
        out = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else 'ERROR ' + p.stderr[:200]
    except subprocess.TimeoutExpired:
        out = 'TIMEOUT after %d s' % a.timeout
    return out.split(' seconds')[0], round(time.time() - t, 2)


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


rec = {'label': a.label, 'file': os.path.basename(a.path), 'sha256': sha(a.path), 'n': n, 'ks_by_digit': ks,
       'clique_c_sha256': sha(os.path.join(TOOLS, 'clique.c')), 'gen0_c_sha256': sha(os.path.join(TOOLS, 'gen0.c')),
       'reduction': 'none (whole colour class, no symmetry)'}
per = []; ok = True
for d, k in zip(digits, ks):
    A = cls(d); txt = text(A)
    e = {'digit': d, 'k': k, 'edges': sum(map(sum, A)) // 2, 'class_text_sha256': hashlib.sha256(txt.encode()).hexdigest()}
    for name, binary in (('clique_c', CLQ), ('gen0', GEN)):
        if '%s:%s' % (name, d) in a.skip_whole:
            e[name] = 'NOT RUN HERE (see the separate log for this checker and colour)'; e[name + '_s'] = None
        else:
            e[name], e[name + '_s'] = run(binary, k, txt)
    # (a) lowered k
    l1, _ = run(CLQ, k - 1, txt); l2, _ = run(GEN, k - 1, txt)
    Q = [int(x) for x in l1.split()[2:]] if l1.startswith('FOUND') else []
    q_ok = len(Q) >= k - 1 and len(set(Q)) == len(Q) and all(A[x][y] for x in Q for y in Q if x != y)
    Q = Q[:k - 1]
    e['control_lowered_k'] = {'asked_for': k - 1, 'clique_c': l1, 'gen0': l2, 'clique_rechecked_edge_by_edge': q_ok}
    ctl = l1.startswith('FOUND') and l2.startswith('FOUND') and q_ok
    # (b) corruption
    cor = None
    if q_ok:
        best = None
        if k == 3:
            x, z = Q
            y = next(w for w in range(n) if w not in (x, z) and A[z][w] and not A[x][w])
            best = (1, y, [x])
        else:
            for v in range(n):
                if v in Q: continue
                miss = [q for q in Q if not A[v][q]]
                if best is None or len(miss) < best[0]: best = (len(miss), v, miss)
        cnt, v, miss = best
        A2 = [r[:] for r in A]
        for q in miss: A2[v][q] = A2[q][v] = True
        t2 = text(A2); c1, _ = run(CLQ, k, t2); c2, _ = run(GEN, k, t2)
        cor = {'edges_recoloured': [[v, q, 'from digit %s to digit %s' % (rows[v][q], d)] for q in miss],
               'number_of_edges_recoloured': cnt, 'clique_c': c1, 'gen0': c2,
               'detected_by_both': c1.startswith('FOUND') and c2.startswith('FOUND')}
    e['control_corrupted_copy'] = cor
    e['whole_graph_none_by'] = [nm for nm in ('clique_c', 'gen0') if str(e[nm]).startswith('NONE')]
    e['pass_both_whole'] = len(e['whole_graph_none_by']) == 2
    e['no_checker_found_forbidden_clique'] = not any(str(e[nm]).startswith('FOUND') for nm in ('clique_c', 'gen0'))
    e['controls_pass'] = bool(ctl and cor and cor['detected_by_both'])
    ok = ok and e['pass_both_whole'] and e['controls_pass']; per.append(e)
rec['per_colour'] = per
rec['verdict'] = 'PASS' if ok else 'INCOMPLETE OR FAIL (see per_colour)'
rec['logged_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
open(a.log, 'a').write(json.dumps(rec, sort_keys=True) + '\n'); print(json.dumps(rec, indent=1))
