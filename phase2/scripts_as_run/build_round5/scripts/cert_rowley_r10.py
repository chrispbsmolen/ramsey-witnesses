"""Rebuild certificate for R(10,10,10) (W on 23093 vertices), written from the text of Rowley, AJC 81(2) (2021) 245-256,
Theorem 3.2 (statement p.248; construction in the proof, p.249), independently of build_round2/scripts/build_linear.py.

Inputs (hashed): U = column "10,3" of sheet Jan_2021_trg(k,3) of the ancillary spreadsheet of Rowley arXiv:2203.13476v3
(CSV export, sha256 53f2bf9d...), m = 30; V = Paley graph Q_797 (colour of length mu: quadratic residue or not; the
repo file paley797_R10_10.g6 is compared with it).
Hypotheses checked: U is a linear 2-colouring of K_30 (lengths 1..29); the template colour q = 2 contains length m-1 = 29
and is triangle-free as a set of lengths (no a, b, a+b all in it) -- the tf-template of Def. 3.1 p.248; phi = min(L_q)-1
and phi < m-1; V is a linear colouring of K_797 (Q_797 is cyclic); n_W = (m-1)(n-1)+1+phi.
Construction (p.249): for s != q, L''_s = {l + (mu-1)(m-1) : l in L_s, 1 <= mu <= n-1} u {l + (n-1)(m-1) : l in L_s, l <= phi};
for each colour t of V, L''_t = {l + (mu-1)(m-1) : l in L_q, 1 <= mu <= n-1, c_V(mu) = t}.
The rebuilt length vector is compared with built/R10^3_n23093.lengths (SHA-256 pinned) up to renaming the colours of V,
and the canonical text of the rebuilt file is hashed.
Usage: python3 cert_rowley_r10.py SHEET_CSV LENGTHS_FILE [PALEY797_G6]   Appends to logs/certificates.jsonl."""
import sys, os, csv, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L

sheet, lengths = sys.argv[1], sys.argv[2]
g6 = sys.argv[3] if len(sys.argv) > 3 else None
SHEET_SHA = '53f2bf9d27f2ed4d4d93cab13b43ebc54d60519aef3b3f717d0224989f466bf9'
W_SHA = '7c26d1205680411161a5f0ff010d738bd1d838509e396672fd1cafd1635462a2'
P797_SHA = 'b42e63a21acaa5c949d9c31096b509191c4baa410b11895bbd0a03beab135fdd'
rec = dict(certificate='R(10,10,10) > 23093 via Rowley AJC 81(2) Thm 3.2', sheet_sha256=L.sha256_file(sheet))
rec['sheet_sha_match'] = rec['sheet_sha256'] == SHEET_SHA
rows = list(csv.reader(open(sheet)))
hdr = next(r for r in rows if len(r) > 2 and r[2] == 'PARAMETERS')
col = hdr.index('10,3')
order = int(next(r for r in rows if len(r) > 2 and r[2] == 'ORDER =')[col])
phi_sheet = int(next(r for r in rows if len(r) > 2 and r[2] == 'PHI =')[col])
U = {}
for r in rows:
    if len(r) > col and r[1].strip().isdigit() and r[col].strip():
        U[int(r[1])] = int(r[col])
m = order
assert sorted(U) == list(range(1, m)), 'U must give lengths 1..m-1'
q = 2
Lq = {l for l in U if U[l] == q}
tf = not any((a + b) in Lq for a in Lq for b in Lq if a <= b)
phi = min(Lq) - 1
p = 797
QR = np.zeros(p, dtype=bool); QR[[x * x % p for x in range(1, p)]] = True
cV = {mu: (1 if QR[mu] else 2) for mu in range(1, p)}   # V's two colours, named 1 (residue) and 2 (non-residue)
n = p
NW = (m - 1) * (n - 1) + 1 + phi
c = [None] * NW
for mu in range(1, n):
    for l in range(1, m):
        h = l + (mu - 1) * (m - 1)
        assert c[h] is None
        c[h] = ('U', U[l]) if U[l] != q else ('V', cV[mu])
for l in range(1, phi + 1):
    h = l + (n - 1) * (m - 1)
    assert c[h] is None and U[l] != q
    c[h] = ('U', U[l])
assert all(x is not None for x in c[1:])
rec.update(m=m, U_colours=sorted(set(U.values())), template_colour=q, template_contains_m_minus_1=(m - 1) in Lq,
           template_triangle_free=tf, phi=phi, phi_sheet=phi_sheet, phi_ok=(phi == phi_sheet and phi < m - 1),
           U_order_sheet=order, V='Q_797', N_formula='(m-1)(n-1)+1+phi = %d' % NW, N=NW)
if g6:
    A = L.load_g6(g6)
    rec['paley797_g6_sha_match'] = L.sha256_file(g6) == P797_SHA
    rec['paley797_g6_equals_QR_rule'] = bool(L.is_circulant(A) and all(A[0][mu] == QR[mu] for mu in range(1, p)))
# compare with the row's file, up to renaming colours
rec['file_sha256'] = L.sha256_file(lengths)
rec['file_sha_match'] = rec['file_sha256'] == W_SHA
tok = open(lengths).read().split()
Nf = int(tok[0]); f = [int(x) for x in tok[1:Nf]]
rec['file_N'] = Nf
best = None
labels = sorted(set(c[1:]))
for perm in itertools.permutations(sorted(set(f)), len(labels)):
    mp = dict(zip(labels, perm))
    if Nf == NW and all(mp[c[h]] == f[h - 1] for h in range(1, NW)):
        best = {'%s%d' % k: v for k, v in mp.items()}; break
rec['matches_file'] = best is not None
rec['colour_map_rebuilt_to_file'] = best
if best:
    mp = {k: best['%s%d' % k] for k in labels}
    txt = ('%d\n' % NW + ' '.join(str(mp[c[h]]) for h in range(1, NW)) + '\n').encode()
    rec['rebuilt_canonical_text_sha256'] = L.sha256_bytes(txt)
    rec['rebuilt_text_equals_file_bytes'] = (txt == open(lengths, 'rb').read())
ok = rec['sheet_sha_match'] and rec['file_sha_match'] and tf and rec['template_contains_m_minus_1'] and rec['phi_ok'] and rec['matches_file'] and NW == 23093
rec['verdict'] = 'CERTIFIED (rebuild matches the row file; hypotheses of Thm 3.2 hold)' if ok else 'NOT CERTIFIED'
L.log('certificates.jsonl', rec)
