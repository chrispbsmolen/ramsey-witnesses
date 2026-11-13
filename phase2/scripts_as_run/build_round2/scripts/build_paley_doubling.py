"""R(17,17) .. R(23,23): Shearer/Mathon doubling of the Paley graph Q_p (survey 2.2.c; LuSL AJC 25 (2002)
Lemma 1 p.103 and Theorem 2 pp.112-115; Exoo https://cs.indstate.edu/ge/Paley/ramsey.html).
The doubling as stated in XXER EJC 11 (2004) #R35 pp.12-13 and implemented in round 1
(build_G1_G2/scripts/constructions.py paley_doubling, matrix-identical to the repo's verified mathon101 and
mathon281 files): vertices w3, w1, H = Z_p, H' = Z_p (in this order); x ~ y and x' ~ y' iff x-y is a nonzero
square; x ~ y' iff x-y is a non-square (x !~ x'); w3 ~ all of H; w1 ~ all of H'; w3 !~ w1.  n = 2p + 2.

Usage: python3 build_paley_doubling.py selftest | P [write]
  For n <= 40000 with 'write': graph6 (gzip) written row-free, column by column, without an n x n matrix.
  Always: logs/builds_paley.jsonl gets the recipe record, primality, n, and the SHA-256 of the canonical graph6
  text (so a regenerated file can be matched even where none is stored)."""
import sys, os, gzip, hashlib, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lib2 as L

CELLS = {4457: ('17,17', 8917, 15, 'LuSL AJC 25 (2002) Thm 2 (1) pp.112-114: c(G_p) = 15'),
         5501: ('18,18', 11005, 16, 'LuSL AJC 25 (2002) Thm 2 (2) pp.114-115: c(G_p) = 16'),
         8941: ('19,19', 17885, 17, 'LuSL AJC 25 (2002) Thm 2 (3) p.115: c(G_p) = 17'),
         10861: ('20,20', 21725, 18, 'Exoo, Largest Paley Graphs with Small Clique Numbers, cs.indstate.edu/ge/Paley/ramsey.html (sha256 3bbd44c5...a7): k=18'),
         15461: ('21,21', 30925, 19, 'Exoo Paley page: k=19'),
         19553: ('22,22', 39109, 20, 'Exoo Paley page: k=20'),
         24709: ('23,23', 49421, 21, 'Exoo Paley page: k=21 ("the last entry gives R(23,23) > 49420")')}


def is_prime(p):
    return p > 1 and all(p % q for q in range(2, int(p ** .5) + 1))


def column_bits(p, QR, j):
    """adjacency of vertex j to vertices 0..j-1 in the vertex order w3, w1, H, H' (bool array of length j)."""
    if j == 0: return np.zeros(0, dtype=bool)
    if j == 1: return np.zeros(1, dtype=bool)                                    # w3 !~ w1
    if j < 2 + p:                                                               # j = x in H
        x = j - 2
        col = np.zeros(j, dtype=bool); col[0] = True                            # w3 ~ H
        col[2:] = QR[(x - np.arange(x)) % p]
        return col
    y = j - 2 - p                                                               # j = y' in H'
    col = np.zeros(j, dtype=bool); col[1] = True                                # w1 ~ H'
    d = (np.arange(p) - y) % p
    col[2:2 + p] = (~QR[d]) & (d != 0)                                          # x ~ y' iff x - y non-square
    col[2 + p:] = QR[(y - np.arange(y)) % p]
    return col


def g6_stream(p, sink):
    """graph6 of the doubling (header-free, one line), fed to sink(bytes) in chunks."""
    n = 2 * p + 2
    QR = np.zeros(p, dtype=bool); QR[[x * x % p for x in range(1, p)]] = True
    if n < 63: head = bytes([n + 63])
    elif n < 258048: head = bytes([126, 63 + (n >> 12 & 63), 63 + (n >> 6 & 63), 63 + (n & 63)])
    else: raise ValueError
    sink(head)
    carry = np.zeros(0, dtype=bool)
    for j in range(1, n):
        bits = np.concatenate([carry, column_bits(p, QR, j)])
        k = len(bits) // 6 * 6
        if k:
            b = bits[:k].reshape(-1, 6).astype(np.uint8)
            vals = (b * np.array([32, 16, 8, 4, 2, 1], dtype=np.uint8)).sum(axis=1) + 63
            sink(vals.astype(np.uint8).tobytes())
        carry = bits[k:]
    if len(carry):
        b = np.concatenate([carry, np.zeros(6 - len(carry), dtype=bool)]).astype(np.uint8)
        sink(bytes([int((b * np.array([32, 16, 8, 4, 2, 1])).sum()) + 63]))
    sink(b'\n')


def selftest():
    import networkx as nx
    sys.path.insert(0, '<cloud>/ramsey-p2/build_G1_G2/scripts')
    import constructions as K
    out = {}
    for p in (13, 101, 797):
        buf = []; g6_stream(p, buf.append); mine = b''.join(buf)
        C = K.paley_doubling(p); A = (C == 1).astype(int)
        ref = nx.to_graph6_bytes(nx.from_numpy_array(A), header=False)
        out[p] = mine == ref
    for p, f in ((101, 'mathon101_R7_7.g6'),):
        buf = []; g6_stream(p, buf.append)
        out['repo_' + f] = b''.join(buf).strip() == open(L.REPO + '/constructions/witnesses/' + f, 'rb').read().strip()
    L.log('builds_paley.jsonl', dict(selftest_identical_to_round1_paley_doubling_and_repo=out))


def main():
    if sys.argv[1] == 'selftest': return selftest()
    p = int(sys.argv[1]); write = len(sys.argv) > 2 and sys.argv[2] == 'write'
    cell, sl, alpha, src = CELLS[p]
    n = 2 * p + 2
    h = hashlib.sha256(); size = [0]
    fname = 'mathon%d_R%s.g6.gz' % (p, cell.replace(',', '_'))
    gz = gzip.GzipFile(os.path.join(L.BUILT, fname), 'wb', mtime=0) if (write and n <= 40000) else None
    def sink(b):
        h.update(b); size[0] += len(b)
        if gz: gz.write(b)
    g6_stream(p, sink)
    if gz: gz.close()
    rec = dict(cell=cell, survey_lower=sl, p=p, p_prime=is_prime(p), p_mod_4=p % 4, N=n, N_ok=(n == sl - 1),
               published_clique_number_of_Q_p=alpha, clique_number_source=src,
               bound_from_doubling='R(%d,%d) > %d needs omega(Q_p) <= %d' % (alpha + 2, alpha + 2, n, alpha),
               construction='Shearer (JCTA 42 (1986)) / Mathon (JCTB 42 (1987)) doubling as stated in XXER EJC 11 (2004) #R35 pp.12-13; LuSL Lemma 1 p.103',
               vertex_order='w3, w1, H=Z_p, H\'=Z_p', g6_sha256_uncompressed=h.hexdigest(), g6_bytes=size[0],
               file=('built/' + fname) if gz else None, sha256=L.sha256_file(os.path.join(L.BUILT, fname)) if gz else None)
    L.log('builds_paley.jsonl', rec)


if __name__ == '__main__':
    main()
