"""Rebuild certificate for the doubled-Paley rows, row by row.  Same checks and same record fields as cert_shearer.py
(see its header for the text of Shearer, J. Combin. Theory Ser. A 42 (1986) 302-304, that is used); the only
difference is that no n x n matrix is held in memory, so that p = 8941 and p = 10861 fit in a few hundred MB.
  H_p (p.302), vertex order lambda, lambda', 0..p-1, 0'..(p-1)':  row(u) is computed from the definition.
  H_p^- = H_p minus the edges (x,x') and (lambda,lambda').
  (3) graph6 of H_p^- (upper triangle, column by column) is compared byte for byte with the decompressed row file.
  (4) phi: x -> n x, x' -> (n x)', lambda <-> lambda' (n the least non-residue).  For every vertex u the row of u in
      the complement of H_p^- , read through phi, equals the row of phi(u) in H_p.
Usage: python3 cert_shearer_rows.py P K ROW_FILE ROW_GZ_SHA    Appends to logs/certificates.jsonl."""
import sys, os, gzip, hashlib, json, time
import numpy as np

p, k, row, rowsha = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
sha = lambda b: hashlib.sha256(b).hexdigest()
rec = dict(certificate='R(%d,%d) > %d via Shearer JCTA 42 (1986) Lemma 1 (pp.302-303) and Theorem 1 (p.303)' % (k + 2, k + 2, 2 * p + 2),
           p=p, k=k, p_prime=all(p % d for d in range(2, int(p ** .5) + 1)), p_1_mod_4=(p % 4 == 1), method='row by row (cert_shearer_rows.py)')
QR = np.zeros(p, dtype=bool); QR[[x * x % p for x in range(1, p)]] = True
n = 2 * p + 2
LAM, LAMP, X0, XP0 = 0, 1, 2, 2 + p
ar = np.arange(p)

def H_row(u, minus=False):
    """row u of H_p (minus=False) or of H_p^- (minus=True)"""
    r = np.zeros(n, dtype=bool)
    if u == LAM:
        r[X0:X0 + p] = True; r[LAMP] = not minus
    elif u == LAMP:
        r[XP0:] = True; r[LAM] = not minus
    elif u < XP0:
        x = u - X0; d = (ar - x) % p
        r[LAM] = True
        r[X0:X0 + p] = QR[d]                       # (x,y) in G_p
        r[XP0:] = ~QR[d] & (d != 0)                # (x,y') for (x,y) in the complement of G_p
        r[XP0 + x] = not minus                     # (x,x')
    else:
        x = u - XP0; d = (ar - x) % p
        r[LAMP] = True
        r[XP0:] = QR[d]
        r[X0:X0 + p] = ~QR[d] & (d != 0)
        r[X0 + x] = not minus
    return r

# symmetry of the row function on a sample (the definition is symmetric because QR = -QR)
assert (QR[1:] == QR[1:][::-1]).all()
# (3)
rec['row_gz_sha256'] = sha(open(row, 'rb').read()); rec['row_gz_sha_match'] = rec['row_gz_sha256'] == rowsha
raw = gzip.open(row).read() if row.endswith('.gz') else open(row, 'rb').read()
bits = np.zeros(n * (n - 1) // 2 + 5, dtype=bool); pos = 0
for j in range(1, n):
    bits[pos:pos + j] = H_row(j, True)[:j]; pos += j
m = -(-pos // 6)
vals = (bits[:m * 6].reshape(-1, 6) * np.array([32, 16, 8, 4, 2, 1], dtype=np.uint8)).sum(axis=1).astype(np.uint8) + 63
assert 63 <= n < 258048
enc = bytes([126, 63 + (n >> 12 & 63), 63 + (n >> 6 & 63), 63 + (n & 63)]) + vals.tobytes() + b'\n'
del bits, vals
rec['row_graph6_sha256'] = sha(raw); rec['rebuilt_graph6_sha256'] = sha(enc); rec['rebuilt_equals_row_bytes'] = (enc == raw)
# (4)
nr = next(a for a in range(2, p) if not QR[a])
perm = np.empty(n, dtype=np.int64)
perm[LAM], perm[LAMP] = LAMP, LAM
perm[X0 + ar] = X0 + (nr * ar) % p
perm[XP0 + ar] = XP0 + (nr * ar) % p
assert sorted(perm.tolist()) == list(range(n))
ok4 = True; rows_checked = 0
for u in range(n):
    c = ~H_row(u, True); c[u] = False            # row u of the complement of H_p^-
    if not (c == H_row(int(perm[u]))[perm]).all(): ok4 = False; break
    rows_checked += 1
rec['nonresidue_used'] = nr
rec['complement_of_row_isomorphic_to_H_p_via_map'] = bool(ok4); rec['rows_checked'] = rows_checked
ok = rec['p_prime'] and rec['p_1_mod_4'] and rec['row_gz_sha_match'] and rec['rebuilt_equals_row_bytes'] and ok4
rec['verdict'] = 'CERTIFIED (row file = Shearer H_p minus the (x,x\') edges, byte for byte; complement isomorphic to H_p, checked)' if ok else 'NOT CERTIFIED'
rec['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
os.makedirs('logs', exist_ok=True)
open('logs/certificates.jsonl', 'a').write(json.dumps(rec) + '\n'); print(json.dumps(rec))
