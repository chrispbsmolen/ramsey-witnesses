"""Step 1 / R1: both checkers on the inputs of the rows moved by Amendment 3 (and g415.157 for R(7,16)).

For each input: load with the repo loader (verify_ramsey.load), check the file SHA-256 (or, for a circulant printed in a
paper, the SHA-256 of its canonical text n:d1,d2,...) against the value pinned in sources/manifest.csv, then for each
colour class c with forbidden size k decide "K_k in colour c?" with clique.c and with gen0.
  circulant inputs: translation x -> x+1 is verified on the matrix (every entry), so a clique can be moved to contain
    vertex 0; both checkers get the same reduced graph N_c(0) and are asked for K_(k-1).
  other inputs: the whole colour class, no reduction.
Usage: python3 confirm_inputs.py NAME FMT PATH ENTRY PINNED_SHA K_COLOUR0 K_COLOUR1 TIMEOUT
With R5_NOSYM=1 every colour class is checked whole (no reduction).  Appends to logs/inputs.jsonl."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L
sys.path.insert(0, L.TOOLS)
import verify_ramsey as V

name, fmt, path, entry, pinned, k0, k1, to = sys.argv[1:9]
k0, k1, to = int(k0), int(k1), int(to)
C = V.load('circulant', open(path).read().strip()) if fmt == 'circfile' else V.load(fmt, path, entry)
n = len(C)
if fmt in ('circcsv',):
    nn, D = V.circcsv_entry(path, entry)
    got = V.sha256_text(V.circulant_key(nn, D))
else:
    got = L.sha256_file(path)
rec = dict(input=name, file=os.path.basename(path), entry=entry, n=n, sha256=got, pinned_sha256=pinned, sha_match=(got == pinned))
A1 = (C == 1); A0 = (C == 0)
circ = L.is_circulant(A1)
if os.environ.get('R5_NOSYM'): circ = False   # full check of the whole colour class even for a circulant
rec['circulant_checked_on_matrix'] = circ
res = {}
for colour, A, k in ((0, A0, k0), (1, A1, k1)):
    if circ:
        nb = np.flatnonzero(A[0]); sub = A[np.ix_(nb, nb)]; kk = k - 1; how = 'N_%d(0), %d vertices, K_%d' % (colour, len(nb), kk)
    else:
        sub = A; kk = k; how = 'whole colour class, %d vertices, K_%d' % (n, kk)
    r = {}
    for chk in ('clique', 'gen0'):
        f, out, sec = L.solve(chk, sub, kk, to)
        r[chk] = dict(found=f, out=out, seconds=sec)
    res['colour%d_no_K%d' % (colour, k)] = dict(reduced_problem=how, **r)
rec['checks'] = res
ok = rec['sha_match'] and all(v[c]['found'] is False for v in res.values() for c in ('clique', 'gen0'))
rec['claim'] = 'colour 0 has no K_%d and colour 1 has no K_%d on %d vertices' % (k0, k1, n)
rec['verdict'] = 'PASS (both checkers)' if ok else 'NOT CONFIRMED'
L.log('inputs.jsonl', rec)
