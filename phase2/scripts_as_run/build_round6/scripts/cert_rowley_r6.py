"""Rebuild certificates for the six Rowley rows, written from the text of Rowley, AJC 81(2) (2021) 245-256, Theorem 3.2
(statement p.248; construction in the proof, p.249), independently of build_round2/scripts/build_linear.py.

For each cell: U = first m-1 entries of the cell's column of sheet Paper_Sep_2022 (Rowley arXiv:2203.13476v3 ancillary,
CSV export sha256 c9bbd500...), or Figure 1 p.251 for (6,3;12); V as recorded in build_round2/built/MANIFEST.json:
  R(7^4): V = circulant on Z_202 obtained from the Shearer-Mathon doubling of Q_101 (vertices H u H' only);
  R(8^4): V = Paley Q_281;  R(9^4): V = the same circulant on Z_562 from Q_281;
  R(5^6): V = (5,5,5;453) (hunt_multicolour/converted/julojc_atom_R5_5_5_n453.lengths, sha256 7bcec4b8..., VERIFIED);
  R(6^5), R(6^6): V = the R(6,6,6,6) object R6^4_n23501.lengths (sha256 a43c939d..., VERIFIED 12 Nov).
The doubled circulants are computed from the pair definition (x ~ y iff x-y in QR, x ~ y' iff x-y in NQR, x !~ x';
z -> (z mod p, z mod 2)), and the pair graph is checked to be circulant on Z_2p edge by edge.
Hypotheses checked: U is a linear colouring of K_m (lengths 1..m-1); the template colour q = c(m-1) is triangle-free
as a set of lengths (no a <= b with a, b, a+b all in L_q; Def. 3.1) and contains m-1; phi = min(L_q)-1 < m-1 and equals
the sheet's PHI; V is linear (n-1 lengths); N = (m-1)(n-1)+1+phi.
Construction (p.249): for s != q, L''_s = {l+(mu-1)(m-1) : l in L_s, 1<=mu<=n-1} u {l+(n-1)(m-1) : l in L_s, l<=phi};
for each colour t of V, L''_t = {l+(mu-1)(m-1) : l in L_q, 1<=mu<=n-1, c_V(mu) = t}.
The rebuilt length vector is compared with the row file byte for byte (decompressed), after one renaming of colours
determined from the first occurrence of each colour and then checked on every length.
Usage: python3 cert_rowley_r6.py BUILT_DIR SHEET_CSV R555_LENGTHS [CELL ...]   Appends to logs/certificates.jsonl."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L
import r6common as C
from r6common import paley, doubled_circulant

built, sheet, r555 = sys.argv[1], sys.argv[2], sys.argv[3]
cells = sys.argv[4:] or list(C.ROW)


def compound(U, m, q, phi, cV, n):
    """W of Thm 3.2: returns c (int16 tags) with tag s for U colour s (s != q) and 100+t for V colour t."""
    N = (m - 1) * (n - 1) + 1 + phi
    c = np.zeros(N, dtype=np.int16)
    Uarr = np.array(U[1:], dtype=np.int16)            # colours of lengths 1..m-1
    h = np.arange(1, N)
    mu = (h - 1) // (m - 1) + 1                        # block 1..n (block n = the partial copy)
    l = h - (mu - 1) * (m - 1)
    cu = Uarr[l - 1]
    full = mu <= n - 1
    tag = np.where(cu != q, cu, 0).astype(np.int16)
    vt = np.zeros_like(tag)
    vt[full] = 100 + cV[mu[full]]
    tag = np.where((cu == q) & full, vt, tag)
    assert not ((~full) & (cu == q)).any(), 'partial copy reaches the template'
    assert (l[~full] <= phi).all()
    c[1:] = tag
    assert (c[1:] != 0).all()
    return N, c


for cell in cells:
    fname, pin, col, m, k = C.ROW[cell]
    rec = dict(certificate='%s via Rowley AJC 81(2) Thm 3.2' % cell, row_file=fname)
    path = os.path.join(built, fname)
    rec['row_file_sha256'] = L.sha256_file(path); rec['row_file_sha_match'] = rec['row_file_sha256'] == pin
    if col == 'fig1':
        U = [None] + C.FIG1; hdr = {'PHI =': '4', 'ORDER =': '12'}; rec['U_source'] = 'Rowley AJC 81(2) Figure 1 p.251, (6,3;12)'
    else:
        rec['sheet_sha256'] = L.sha256_file(sheet); rec['sheet_sha_match'] = rec['sheet_sha256'] == C.SHEET_SHA
        U, hdr = C.sheet_column(sheet, col, m)
        rec['U_source'] = 'sheet Paper_Sep_2022 column %d (%s), first %d lengths' % (col, hdr.get('PARAMETERS'), m - 1)
    q = U[m - 1]
    Lq = {l for l in range(1, m) if U[l] == q}
    tf = not any((a + b) in Lq for a in Lq for b in Lq if a <= b)
    phi = min(Lq) - 1
    rec.update(m=m, U_order_sheet=int(hdr['ORDER =']), U_colours=sorted(set(U[1:])), template_colour=q,
               template_contains_m_minus_1=True, template_triangle_free=tf, template_size=len(Lq), phi=phi,
               phi_sheet=int(hdr['PHI =']), phi_ok=(phi == int(hdr['PHI =']) and phi < m - 1))
    # V
    if cell in ('R(7,7,7,7)', 'R(9,9,9,9)'):
        p = 101 if cell == 'R(7,7,7,7)' else 281
        n, cV, circ = doubled_circulant(p)
        rec.update(V='circulant on Z_%d from the doubling of Q_%d (H u H\')' % (n, p), V_pair_graph_is_circulant=circ,
                   V_is_cyclic=bool(all(cV[d] == cV[n - d] for d in range(1, n))))
    elif cell == 'R(8,8,8,8)':
        n, cV = paley(281); rec['V'] = 'Paley Q_281 (quadratic-residue rule)'
    elif cell == 'R(5,5,5,5,5,5)':
        rec['V_sha256'] = L.sha256_file(r555); rec['V_sha_match'] = rec['V_sha256'] == C.R555_SHA
        n, cV = C.read_lengths(r555); rec['V'] = '(5,5,5;453) julojc_atom_R5_5_5_n453.lengths'
    else:
        vp = os.path.join(built, C.R64[0])
        rec['V_sha256'] = L.sha256_file(vp); rec['V_sha_match'] = rec['V_sha256'] == C.R64[1]
        n, cV = C.read_lengths(vp); rec['V'] = 'R(6,6,6,6) object %s' % C.R64[0]
    rec['V_order'] = int(n); rec['V_colours'] = sorted(set(int(x) for x in cV[1:]))
    N, cW = compound(U, m, q, phi, cV, n)
    rec['N_formula'] = '(m-1)(n-1)+1+phi = %d*%d+1+%d = %d' % (m - 1, n - 1, phi, N)
    # compare with the row file
    Nf, f = C.read_lengths(path)
    rec['file_N'] = int(Nf)
    mp = {}
    ok = Nf == N
    if ok:
        for tag in sorted(set(int(x) for x in cW[1:])):
            idx = int(np.argmax(cW == tag)); mp[tag] = int(f[idx])
        ok = len(set(mp.values())) == len(mp)
        if ok:
            lut = np.zeros(200, dtype=np.int8)
            for t, v in mp.items(): lut[t] = v
            mapped = lut[cW]
            ok = bool((mapped[1:] == f[1:]).all())
    rec['matches_file_every_length'] = bool(ok)
    rec['colour_map_rebuilt_to_file'] = {('U%d' % t if t < 100 else 'V%d' % (t - 100)): v for t, v in mp.items()}
    if ok:
        txt = ('%d\n' % N).encode() + b' '.join(b'%d' % x for x in mapped[1:].tolist()) + b'\n'
        rec['rebuilt_canonical_text_sha256'] = L.sha256_bytes(txt)
        rec['rebuilt_text_equals_file_bytes'] = (txt == C.raw_bytes(path))
        del txt
    goods = [rec['row_file_sha_match'], tf, rec['phi_ok'], ok, rec.get('rebuilt_text_equals_file_bytes', False),
             rec.get('sheet_sha_match', True), rec.get('V_sha_match', True), rec.get('V_pair_graph_is_circulant', True)]
    rec['verdict'] = 'CERTIFIED (rebuild equals the row file byte for byte; hypotheses of Thm 3.2 hold)' if all(goods) else 'NOT CERTIFIED'
    L.log('certificates.jsonl', rec)
