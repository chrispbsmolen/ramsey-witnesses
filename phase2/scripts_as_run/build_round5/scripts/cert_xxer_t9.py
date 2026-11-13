"""Rebuild certificate for a row built by XXER Theorem 9 (Xu, Xie, Exoo, Radziszowski, EJC 11 (2004) #R35:
statement p.15, proof pp.15-16, which uses the colouring F of the proof of Theorem 7, pp.10-11), written from the text
independently of build_G3/g3lib.py.

Theorem 9: for l >= 5, k >= 2, R(2k-1, l) >= 4R(k, l-1) - 3.  From a (k, l-1; m)-graph G on v_1..v_m, F lives on
U_1..U_4 (U_i = {(u_i, v_j)}): inside each U_i colour 2 on edges of G, 3 on non-edges; between U_i1, U_i2 with
i1 in {1,2}, i2 in {3,4}: 1 if j1 = j2, 2 if v_j1 v_j2 in E(G), else 3; between U_1,U_2 and between U_3,U_4: 3 if j1 = j2,
else 1.  H = colours 1 and 2 of F merged.  The theorem: H has no K_(2k-1) and no independent l-set.
Hypotheses checked: l >= 5, k >= 2; the input file has the pinned SHA-256; its two-checker record (logs/inputs.jsonl)
says no K_k and no independent (l-1)-set.  The rebuilt H (vertex (u_i, v_j) -> (i-1)m + (j-1)) is compared with the row's
built file, directly or as its complement (the row may store the (l, 2k-1) side).
Usage: python3 cert_xxer_t9.py NAME INPUT_FMT INPUT_PATH INPUT_SHA K L BUILT_G6[.gz] BUILT_SHA
Appends to logs/certificates.jsonl."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L
sys.path.insert(0, L.TOOLS)
import verify_ramsey as V

name, fmt, ipath, isha, k, l, bpath, bsha = sys.argv[1:9]
k, l = int(k), int(l)
C = V.load(fmt, ipath, '')
rec = dict(certificate='%s via XXER Thm 9 (EJC 11 (2004) #R35, p.15-16; colouring of Thm 7 pp.10-11)' % name,
           k=k, l=l, hypotheses_k_l=(k >= 2 and l >= 5), input_sha256=L.sha256_file(ipath))
rec['input_sha_match'] = rec['input_sha256'] == isha
# which colour of the input is G (no K_k): take the one whose verify assignment says k
res = V.verify(C, [k, l - 1], timeout=600)
G = (C == [c for c, kk in res['assignment'].items() if kk == k][0]) if res['verdict'] == 'PASS' else None
rec['input_assignment_clique_c'] = {str(a): b for a, b in res.get('assignment', {}).items()}
m = len(C)
E = np.zeros((m, m), dtype=bool) if G is None else G
F = np.zeros((4 * m, 4 * m), dtype=np.int8)
for i1 in range(4):
    for i2 in range(4):
        B = F[i1 * m:(i1 + 1) * m, i2 * m:(i2 + 1) * m]
        for j1 in range(m):
            for j2 in range(m):
                if i1 == i2:
                    if j1 == j2: continue
                    B[j1, j2] = 2 if E[j1, j2] else 3
                elif {i1, i2} in ({0, 1}, {2, 3}):
                    B[j1, j2] = 3 if j1 == j2 else 1
                else:
                    B[j1, j2] = 1 if j1 == j2 else (2 if E[j1, j2] else 3)
H = (F == 1) | (F == 2)
np.fill_diagonal(H, False)
assert (H == H.T).all()
built = L.load_g6(bpath)
rec['built_sha256'] = L.sha256_file(bpath); rec['built_sha_match'] = rec['built_sha256'] == bsha
same = built.shape == H.shape and bool((built == H).all())
comp = built.shape == H.shape and bool((built == (~H & ~np.eye(len(H), dtype=bool))).all())
rec['n'] = 4 * m
rec['rebuilt_equals_built'] = same; rec['rebuilt_complement_equals_built'] = comp
out = H if same else (~H & ~np.eye(len(H), dtype=bool))
rec['rebuilt_graph6_sha256'] = L.sha256_bytes(L.g6_encode(out))
ok = rec['hypotheses_k_l'] and rec['input_sha_match'] and rec['built_sha_match'] and (same or comp)
rec['verdict'] = 'CERTIFIED (rebuild matches the row file; hypotheses of Thm 9 hold)' if ok else 'NOT CERTIFIED'
L.log('certificates.jsonl', rec)
