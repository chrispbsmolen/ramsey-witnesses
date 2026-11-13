"""Rebuild certificate for the doubled-Paley rows, from the text of J. B. Shearer, Lower bounds for small diagonal Ramsey
numbers, J. Combin. Theory Ser. A 42 (1986) 302-304 (local PDF sha256 48eddbfd...):
  p.302: H_p on 0..p-1, lambda, 0'..(p-1)', lambda' with edges (x,lambda), (x',lambda'), (x,x'), (lambda,lambda') for all x;
         (x,y), (x',y') for (x,y) in G_p; (x,y'), (x',y) for (x,y) in the complement of G_p (x != y).
  Lemma 1 (pp.302-303, with proof): c(H_p) = c(G_p) + 1 = k + 1.
  Theorem 1 (p.303): R_2(k+2) > 2p+2 where k = c(G_p).  [Printed "If c(G_p) = p"; the abstract (p.302) and the proof make
         clear that "= k" is meant.]  Proof: the complement of H_p is isomorphic to H_p with the edges (x,x'),
         x in {0..p-1, lambda}, deleted ("H_p^-"); so c(complement of H_p) <= c(H_p) = k+1.
The row files (build_G1_G2 / build_round2, vertex order w3, w1, H, H') store H_p^- with w3 = lambda, w1 = lambda'.
This script: (1) checks p prime, p = 1 mod 4, and the input record c(G_p) = k (passed in, from logs);
(2) builds H_p exactly as on p.302 and H_p^- from it; (3) compares H_p^- with the row file (decompressed graph6 bytes
identical to an independent encoder's output, and the .gz file's SHA-256 equal to the ledger's); (4) checks on the
object the isomorphism used in Theorem 1's proof: x -> n x, x' -> (n x)', lambda <-> lambda' (n a fixed non-residue)
maps the complement of H_p^- onto H_p, edge by edge.  Then: H_p^- is a subgraph of H_p, so c(H_p^-) <= k+1 (Lemma 1),
and its complement is isomorphic to H_p, so alpha(H_p^-) = k+1: no K_(k+2), no independent (k+2)-set on 2p+2 vertices.
Usage: python3 cert_shearer.py P K ROW_FILE ROW_GZ_SHA [SMALLCHECK]   Appends to logs/certificates.jsonl.
SMALLCHECK=1 also computes c(H_p^-) and c(complement) with clique.c and gen0 (small p only)."""
import sys, os, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L

p, k, row, rowsha = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
small = len(sys.argv) > 5 and sys.argv[5] == '1'
rec = dict(certificate='R(%d,%d) > %d via Shearer JCTA 42 (1986) Lemma 1 (pp.302-303) and Theorem 1 (p.303)' % (k + 2, k + 2, 2 * p + 2),
           p=p, k=k, p_prime=all(p % d for d in range(2, int(p ** .5) + 1)), p_1_mod_4=(p % 4 == 1))
QR = np.zeros(p, dtype=bool); QR[[x * x % p for x in range(1, p)]] = True
D = (np.arange(p)[None, :] - np.arange(p)[:, None]) % p
Gp = QR[D]                                   # G_p
Gc = ~Gp & (D != 0)                           # complement of G_p (no loops)
n = 2 * p + 2
LAM, LAMP, X0, XP0 = 0, 1, 2, 2 + p           # order: lambda, lambda', 0..p-1, 0'..(p-1)'
H = np.zeros((n, n), dtype=bool)
H[X0:X0 + p, LAM] = H[LAM, X0:X0 + p] = True                  # (x, lambda)
H[XP0:, LAMP] = H[LAMP, XP0:] = True                          # (x', lambda')
idx = np.arange(p)
H[LAM, LAMP] = H[LAMP, LAM] = True                            # (lambda, lambda')
H[X0:X0 + p, X0:X0 + p] = Gp; H[XP0:, XP0:] = Gp               # (x,y), (x',y') for (x,y) in G_p
H[X0:X0 + p, XP0:] = Gc; H[XP0:, X0:X0 + p] = Gc.T             # (x,y'), (x',y) for (x,y) in complement of G_p
H[X0 + idx, XP0 + idx] = H[XP0 + idx, X0 + idx] = True         # (x, x')  (set after the blocks above)
assert (H == H.T).all() and not H.diagonal().any()
Hm = H.copy()
Hm[X0 + idx, XP0 + idx] = Hm[XP0 + idx, X0 + idx] = False
Hm[LAM, LAMP] = Hm[LAMP, LAM] = False
# (3) compare with the row file
rec['row_gz_sha256'] = L.sha256_file(row); rec['row_gz_sha_match'] = rec['row_gz_sha256'] == rowsha
raw = gzip.open(row).read() if row.endswith('.gz') else open(row, 'rb').read()
enc = L.g6_encode(Hm)
rec['row_graph6_sha256'] = L.sha256_bytes(raw)
rec['rebuilt_graph6_sha256'] = L.sha256_bytes(enc)
rec['rebuilt_equals_row_bytes'] = (enc == raw)
# (4) the isomorphism of Theorem 1's proof, on the object
nr = next(a for a in range(2, p) if not QR[a])
perm = np.empty(n, dtype=np.int64)
perm[LAM], perm[LAMP] = LAMP, LAM
perm[X0 + idx] = X0 + (nr * idx) % p
perm[XP0 + idx] = XP0 + (nr * idx) % p
comp = ~Hm; np.fill_diagonal(comp, False)
# phi maps edge {u,v} of comp to {perm u, perm v}; check comp[u,v] == H[perm u, perm v] for all u, v
img = np.empty_like(H)
img[np.ix_(perm, perm)] = comp
rec['nonresidue_used'] = nr
rec['complement_of_row_isomorphic_to_H_p_via_map'] = bool((img == H).all())
del img, comp
if small:
    for name, A in (('row graph', Hm), ('complement of row graph', ~Hm & ~np.eye(n, dtype=bool))):
        r = {}
        for c in ('clique', 'gen0'):
            f2, o2, _ = L.solve(c, A, k + 2, 300); f1, o1, _ = L.solve(c, A, k + 1, 300)
            r[c] = dict(has_K_k_plus_2=f2, has_K_k_plus_1=f1)
        rec['small_check_%s' % name.replace(' ', '_')] = r
ok = rec['p_prime'] and rec['p_1_mod_4'] and rec['row_gz_sha_match'] and rec['rebuilt_equals_row_bytes'] and rec['complement_of_row_isomorphic_to_H_p_via_map']
rec['verdict'] = 'CERTIFIED (row file = Shearer H_p minus the (x,x\') edges, byte for byte; complement isomorphic to H_p, checked)' if ok else 'NOT CERTIFIED'
L.log('certificates.jsonl', rec)
