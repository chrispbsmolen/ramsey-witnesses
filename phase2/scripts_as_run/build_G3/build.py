"""Build the G3 graphs.  Run: python3 build.py   (writes built/*.g6[.gz] and built/manifest.json)

Inputs are read from the ramsey-witnesses working copy (<cloud>/ramsey-witnesses, the same
files as repo/sources/manifest.csv; every input's SHA-256 is checked against that manifest before
use).  The checker code used here is an unchanged copy of repo/verify_ramsey.py and repo/clique.c
in tools/ (same SHA-256), so nothing is written into the repository.

Every output graph is written so that it has no K_k and no independent l-set for its cell (k,l)
with k < l, i.e. "edges avoid the smaller clique".
"""
import os, sys, json, gzip, csv, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools')); sys.path.insert(0, HERE)
import verify_ramsey as V
import g3lib as L

REPO = os.path.join(HERE, '..', 'repo')
DATA = '<cloud>/ramsey-witnesses/'
MAN = {r['id']: r for r in csv.DictReader(open(os.path.join(REPO, 'sources', 'manifest.csv')))}
OUT = os.path.join(HERE, 'built'); os.makedirs(OUT, exist_ok=True)
log = []
def say(s): log.append(s); print(s, flush=True)


def load_input(mid, a, b, orient=True):
    """Return (A, info): A a 0/1 adjacency with no K_a and no independent b-set, read from manifest
    entry `mid`, SHA-256 checked.  Orientation is decided by verify_ramsey.verify (a full recheck)."""
    r = MAN[mid]
    path = r['path'] if r['path'].startswith('constructions') else r['path']
    full = os.path.join(REPO, path) if path.startswith('constructions') else os.path.join(DATA, path)
    if r['format'] == 'circcsv':
        n, D = V.circcsv_entry(full, r['entry']); sha = V.sha256_text(V.circulant_key(n, D))
        C = V.circulant_matrix(n, D)
    else:
        sha = V.sha256_file(full); C = V.load(r['format'], full, r['entry'])
    assert sha == r['sha256'], (mid, sha, r['sha256'])
    info = dict(id=mid, path=full, sha256=sha, n=len(C), url=r['url'])
    if orient:
        t0 = time.time(); res = V.verify(C, [a, b])
        assert res['verdict'] == 'PASS', (mid, res)
        col = [c for c, k in res['assignment'].items() if k == a][0] if a != b else 1
        info['recheck'] = 'verify_ramsey PASS R(%d,%d) > %d in %.1f s' % (a, b, len(C), time.time() - t0)
    else:
        col = 1; info['recheck'] = 'not rechecked here (repo ledger PASS)'
    A = (C == col).astype(np.uint8); np.fill_diagonal(A, 0)
    if r['format'] == 'circcsv' or mid.endswith('paley101_R6_6.g6'):
        info['circulant'] = bool(V.is_circulant(V.from_adjacency(A)))
    say('input %s: n=%d sha256 ok; %s' % (mid, len(A), info['recheck']))
    return A, info


def find_clique(A, s):
    found, out = V.has_clique(V.from_adjacency(A), 1, s)
    assert found, 'no K_%d found' % s
    verts = [int(x) for x in out.split()[2:]][:s]
    sub = A[np.ix_(verts, verts)]
    assert sub.sum() == s * (s - 1), 'reported clique is not a clique'
    return verts


def shift_perm(n): return (np.arange(n) + 1) % n


def save(name, A, meta):
    b = L.g6_bytes(A)
    gz = len(b) > 20000
    fn = name + '.g6' + ('.gz' if gz else '')
    path = os.path.join(OUT, fn)
    if gz:
        with gzip.GzipFile(path, 'wb', mtime=0) as f: f.write(b)
    else:
        open(path, 'wb').write(b)
    meta.update(file='built/' + fn, n=int(len(A)), sha256_file=V.sha256_file(path), sha256_g6=L.sha256(b),
                edges=int(A.sum() // 2))
    say('built %-28s n=%4d edges=%7d sha256(file)=%s' % (fn, len(A), meta['edges'], meta['sha256_file'][:16]))
    return meta


def main():
    M = {}
    paley, i_paley = load_input('constructions/paley101_R6_6.g6', 6, 6)
    mat204, i_m204 = load_input('constructions/mathon101_R7_7.g6', 7, 7)
    mat564, i_m564 = load_input('constructions/mathon281_R9_9.g6', 9, 9, orient=False)
    g67, i_g67 = load_input('exoo_tatarevic/g67.114', 6, 7)
    g87, i_g87 = load_input('tatarevic/g78.218', 8, 7)
    g97, i_g97 = load_input('kuznetsov/table2(7,9)', 9, 7)
    g415, i_g415 = load_input('tatarevic/g415.157', 4, 15)
    g96, i_g96 = load_input('kuznetsov/table2(6,9)', 9, 6)
    g320, i_g320 = load_input('exoo_site/r3.20.110', 3, 20)
    g514, i_g514 = load_input('kuznetsov/table2(5,14)', 5, 14)

    def t9cell(cell, A, k, lm1, inputs, comp, vt_gens=None, src=''):
        """A: (k, lm1)-graph.  Theorem 9 gives a (2k-1, lm1+1)-graph; complemented if comp."""
        F = L.t9(A); m = len(A)
        meta = dict(cell=cell, construction='XXER Theorem 9 (EJC 11 (2004) #R35 p. 15-16) on a (%d,%d)-graph of order %d -> (%d,%d)-graph of order %d%s' % (
            k, lm1, m, 2 * k - 1, lm1 + 1, 4 * m, ', complemented' if comp else ''), inputs=inputs, survey_ref=src)
        if vt_gens is not None:
            gens = [L.t9_lift_perm(g, m) for g in vt_gens] + L.t9_block_perms(m)
            meta['vt_generators'] = [g.tolist() for g in gens]
        out = L.complement(F) if comp else F
        return out, meta, F

    # ---- Theorem 9 cells
    G711, meta, F711 = t9cell('7,11', paley, 6, 6, [i_paley], True, [shift_perm(101)], 'XXER')
    M['7,11'] = save('G3_R7_11_404', G711, meta)
    G813, meta, _ = t9cell('8,13', mat204, 7, 7, [i_m204], True, None, 'XXER')
    M['8,13'] = save('G3_R8_13_816', G813, meta)
    G, meta, _ = t9cell('8,11', g67, 6, 7, [i_g67], True, None, '2.3.i')
    M['8,11'] = save('G3_R8_11_456', G, meta)
    G, meta, _ = t9cell('8,15', g87, 8, 7, [i_g87], True, None, '2.3.i')
    M['8,15'] = save('G3_R8_15_872', G, meta)
    G, meta, _ = t9cell('8,17', g97, 9, 7, [i_g97], True, [shift_perm(251)], '2.3.i')
    M['8,17'] = save('G3_R8_17_1004', G, meta)
    G, meta, _ = t9cell('7,16', g415, 4, 15, [i_g415], False, None, '2.3.i')
    M['7,16'] = save('G3_R7_16_628', G, meta)
    G, meta, _ = t9cell('7,17', g96, 9, 6, [i_g96], True, [shift_perm(182)], '2.3.i')
    M['7,17'] = save('G3_R7_17_728', G, meta)
    G, meta, _ = t9cell('5,21', g320, 3, 20, [i_g320], False, None, '2.3.i')
    M['5,21'] = save('G3_R5_21_440', G, meta)
    # (8,21): Theorem 9 applied to the (11,7)-graph F711 built above (before complementing)
    gens711 = [np.array(g) for g in M['7,11']['vt_generators']]
    G, meta, _ = t9cell('8,21', F711, 11, 7, [dict(id='built G3_R7_11_404 (complement, an (11,7)-graph)', sha256=M['7,11']['sha256_g6'])], True,
                        gens711, '2.3.i')
    M['8,21'] = save('G3_R8_21_1616', G, meta)

    # ---- XSR2 Corollary 3 (Theorem 3 with H = M = K_{k-1}, |W1| = 2, |W2| = k-3)
    def cor3cell(cell, G, k, s, inputs, src):
        K = find_clique(G, k - 1)
        H = np.ones((k - 1, k - 1), dtype=np.uint8); np.fill_diagonal(H, 0)
        F = L.xsr2_thm3(G, H, K, list(range(k - 1)), 2)
        meta = dict(cell=cell, construction='XSR2 Theorem 3 / Corollary 3 (preprint p. 4-6): G = (%d,%d)-graph of order %d, H = M = K_%d, W1 = 2 vertices, W2 = %d vertices -> (%d,%d)-graph of order %d' % (
            k, s, len(G), k - 1, k - 3, k, s + 1, len(F)), inputs=inputs, survey_ref=src, clique_in_G=K)
        return F, meta
    G, meta = cor3cell('5,15', g514, 5, 14, [i_g514], '2.3.h')
    M['5,15'] = save('G3_R5_15_274', G, meta)
    G, meta = cor3cell('7,12', G711, 7, 11, [dict(id='built G3_R7_11_404', sha256=M['7,11']['sha256_g6'])], 'XSR2')
    M['7,12'] = save('G3_R7_12_416', G, meta)
    G, meta = cor3cell('9,10', mat564, 9, 9, [i_m564], 'XSR2')
    M['9,10'] = save('G3_R9_10_580', G, meta)

    # ---- (8,19), survey 2.2.h: G = the (8,13)-graph above, H = complement of the XSR2 (7,8;216)-graph
    # built on the Mathon (7,7;204)-graph (XSR2 Theorem 4: R(7,8) >= R(7,7) + 12), M = complement of the
    # Mathon graph (K_7-free), which is induced on U_1 = vertices 0..203 of G813 and on vertices 0..203 of H.
    K6 = find_clique(mat204, 6)
    H6 = np.ones((6, 6), dtype=np.uint8); np.fill_diagonal(H6, 0)
    F78 = L.xsr2_thm3(mat204, H6, K6, list(range(6)), 2)          # (7,8)-graph on 216
    M['aux_7,8'] = save('G3_aux_R7_8_216', F78, dict(cell='aux 7,8', construction='XSR2 Theorem 4 (R(7,8) >= R(7,7)+12): Corollary 3 on the Mathon (7,7;204)-graph, H = M = K_6', inputs=[i_m204], clique_in_G=K6))
    H87 = L.complement(F78)
    phi = list(range(204))
    assert (G813[np.ix_(phi, phi)] == L.complement(mat204)).all() and (H87[np.ix_(phi, phi)] == L.complement(mat204)).all()
    G819 = L.xsr2_thm3(G813, H87, phi, phi, 102)
    meta = dict(cell='8,19', construction='survey 2.2.h: XSR2 Theorem 3 (= 2.3.h with a partition of M) with G = G3_R8_13_816 ((8,13)), H = complement of G3_aux_R7_8_216 ((8,7)), M = complement of the Mathon 204-vertex graph (no K_7, so any W1/W2 split is allowed; W1 = first 102), order 816+216+204',
                inputs=[dict(id='built G3_R8_13_816', sha256=M['8,13']['sha256_g6']), dict(id='built G3_aux_R7_8_216', sha256=M['aux_7,8']['sha256_g6'])], survey_ref='2.2.h')
    M['8,19'] = save('G3_R8_19_1236', G819, meta)

    # ---- (10,15): Theorem 9 on an (8,9;328)-graph.  Input NOT in the repo's verified tier: the first
    # n = 328 entry under the label (8,9) in Kuznetsov's arXiv:1505.07186 source file review.py (lines 771-772),
    # decoded as bit y of the concatenated 64-bit words -> distance y+1 (y = 0..326; the decoded set is
    # symmetric, d in D iff 328-d in D).  Distance set saved in downloads/kuznetsov_lead/.
    rp = '<cloud>/ramsey-work/downloads/papers/kuznetsov/src/review.py'
    assert V.sha256_file(rp) == '8b39c23a040fba06bb941f8b1431e3f804c5ccee19df64b6f7ca683461e13d68'
    words = [0x642863427e0ba730, 0x4fe174ee10ce5d07, 0xbdfebfddfebfdeeb, 0x5d39843b9743f96b, 0x72e83f21630a1370, 0x6]
    assert '(328, ' + ', '.join(hex(w) for w in words) + ')' in open(rp).read()
    x = sum(w << (64 * i) for i, w in enumerate(words))
    D = [y + 1 for y in range(327) if (x >> y) & 1]
    assert all((d in D) == ((328 - d) in D) for d in range(1, 328))
    C = V.circulant_matrix(328, D); t0 = time.time(); res = V.verify(C, [8, 9]); assert res['verdict'] == 'PASS', res
    col8 = [c for c, k in res['assignment'].items() if k == 8][0]
    g89 = (C == col8).astype(np.uint8); np.fill_diagonal(g89, 0)
    i_g89 = dict(id='kuznetsov review.py (8,9) n=328 entry 1 (decoded here)', path=rp, sha256_source_file=V.sha256_file(rp),
                 sha256_circulant_key=V.sha256_text(V.circulant_key(328, D)), n=328,
                 recheck='verify_ramsey PASS R(8,9) > 328 in %.1f s (circulant, through vertex 0)' % (time.time() - t0))
    say('input kuznetsov (8,9;328) decoded: %s' % i_g89['recheck'])
    G, meta, _ = t9cell('10,15', g89, 8, 9, [i_g89], True, [shift_perm(328)], '2.3.i')
    M['10,15'] = save('G3_R10_15_1312', G, meta)

    json.dump(M, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'logs', 'build.txt'), 'w').write('\n'.join(log) + '\n')


if __name__ == '__main__':
    main()
