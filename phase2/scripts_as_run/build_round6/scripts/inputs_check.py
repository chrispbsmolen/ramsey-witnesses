"""Input checks for the six Rowley rows (Amendments 3/4: the theorem's inputs must be VERIFIED with both checkers).
Each input is a linear colouring of K_n given by its length vector c[1..n-1]:
  U inputs (first prototypes with tf-template): sheet Paper_Sep_2022 columns 15 (6,6,3;235), 19 (7,7,3;472),
    21 (8,8,3;650), 25 (9,9,3;1282), 27 (5,5,5,3;977); Rowley AJC 81(2) Figure 1 (6,3;12).
  V inputs (second prototypes): circulant (7,7;202) and (9,9;562) from the doubling of Q_101 / Q_281 (pair definition,
    see cert_rowley_r6.py), Paley Q_281, (5,5,5;453) (julojc_atom_R5_5_5_n453.lengths).
For every colour s with bound k_s (k for the non-template colours, 3 for the template colour):
  'full'    : the whole graph of colour s on n vertices, clique of k_s vertices, clique.c and gen0, no reduction;
  'reduced' : the neighbourhood of vertex 0 in colour s, clique of k_s - 1 vertices, both checkers.  Valid for any linear
              colouring: a monochromatic clique {a_0 < ... < a_t} shifts to {0, a_1-a_0, ...} (Giraud's lemma, as used
              in Rowley AJC 81(2) p.248); for cyclic V it is also the translation automorphism of Z_n, verified on c.
  control   : the same reduced graph asked for a clique of k_s - 2 vertices (a K_{k_s - 1} through 0); FOUND is expected
              for the non-template colours (the colour reaches clique number k_s - 1).
A colour PASSES if both checkers return NONE on the full graph, or on the reduced graph when the full run is not
finished within the cap.  Usage: python3 inputs_check.py WHICH SHEET R555 TIMEOUT [COLOUR]   (COLOUR: check only that colour; WHICH = U6,U7,U8,U9,U5,U6b,V7,V8,V9,V5)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L
import r6common as C

which, sheet, r555, to = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
SPEC = {'U6': (15, 235, 6), 'U7': (19, 472, 7), 'U8': (21, 650, 8), 'U9': (25, 1282, 9), 'U5': (27, 977, 5)}
rec = dict(input=which)
if which in SPEC:
    col, m, k = SPEC[which]
    rec['sheet_sha_match'] = L.sha256_file(sheet) == C.SHEET_SHA
    U, hdr = C.sheet_column(sheet, col, m)
    c = np.array([0] + U[1:], dtype=np.int8); n = m
    q = U[m - 1]
    bounds = {s: (3 if s == q else k) for s in sorted(set(U[1:]))}
    rec.update(name='(%s;%d) sheet Paper_Sep_2022 column %d' % (hdr['PARAMETERS'], m, col), template_colour=int(q))
elif which == 'U6b':
    c = np.array([0] + C.FIG1, dtype=np.int8); n = 12; bounds = {1: 6, 2: 3}
    rec.update(name='(6,3;12) Rowley AJC 81(2) Figure 1 p.251', template_colour=2)
elif which in ('V7', 'V9'):
    p = 101 if which == 'V7' else 281
    n, c, circ = C.doubled_circulant(p); k = 7 if which == 'V7' else 9
    bounds = {1: k, 2: k}; rec.update(name='circulant (%d,%d;%d) from the doubling of Q_%d' % (k, k, n, p), pair_graph_circulant=circ)
elif which == 'V8':
    n, c = C.paley(281); bounds = {1: 8, 2: 8}; rec['name'] = 'Paley Q_281 (8,8;281)'
elif which == 'V5':
    rec['sha_match'] = L.sha256_file(r555) == C.R555_SHA
    n, c = C.read_lengths(r555); bounds = {1: 5, 2: 5, 3: 5}; rec['name'] = '(5,5,5;453) julojc_atom_R5_5_5_n453.lengths'
c = np.asarray(c, dtype=np.int8)
rec['n'] = int(n); rec['cyclic'] = bool(all(c[d] == c[n - d] for d in range(1, n)))
rec['canonical_text_sha256'] = L.sha256_bytes(('%d\n' % n).encode() + b' '.join(b'%d' % x for x in c[1:].tolist()) + b'\n')
d = np.abs(np.arange(n)[:, None] - np.arange(n)[None, :])
res = {}
only = int(sys.argv[5]) if len(sys.argv) > 5 else None
if only is not None: rec['only_colour'] = only
for s, ks in bounds.items():
    if only is not None and s != only: continue
    A = (c[d] == s) & (d > 0)
    r = dict(bound=ks, degree0=int(A[0].sum()))
    for chk in ('clique', 'gen0'):
        f, o, sec = L.solve(chk, A, ks, to); r['full_' + chk] = dict(found=f, out=o[:120], seconds=sec)
    S = np.flatnonzero(A[0]); B = A[np.ix_(S, S)]
    r['reduced_graph_sha256'] = L.sha256_bytes(L.graph_text(B))
    for chk in ('clique', 'gen0'):
        f, o, sec = L.solve(chk, B, ks - 1, to); r['reduced_' + chk] = dict(found=f, out=o[:120], seconds=sec)
    if ks > 3:
        for chk in ('clique', 'gen0'):
            f, o, sec = L.solve(chk, B, ks - 2, to); r['control_K%d_%s' % (ks - 1, chk)] = dict(found=f, out=o[:120], seconds=sec)
    full = all(r['full_' + x]['found'] is False for x in ('clique', 'gen0'))
    red = all(r['reduced_' + x]['found'] is False for x in ('clique', 'gen0'))
    anyfound = any(r[x + y]['found'] is True for x in ('full_', 'reduced_') for y in ('clique', 'gen0'))
    r['verdict'] = 'FAIL (clique found)' if anyfound else ('PASS (full, both checkers)' if full else ('PASS (reduced, both checkers)' if red else 'NOT DONE'))
    res[str(s)] = r
rec['colours'] = res
rec['verdict'] = 'PASS' if all(v['verdict'].startswith('PASS') for v in res.values()) else 'NOT PASS'
L.log('inputs.jsonl', rec)
