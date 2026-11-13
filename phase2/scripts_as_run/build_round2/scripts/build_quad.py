"""XXER Corollary 5 'quadrupling' applied twice (Rowley arXiv:2203.13476v3 Sec.6, NDSATT4.tex l.296-300):
  R(9,9,9):  cyclic (3,8,8;940)  -> (9,5,8;3760)  -> (9,9,9;15040)
  R(8,8,9):  cyclic (3,7,7;673)  -> (8,5,7;2692)  -> (8,9,8;10768)
  R(8,8,8):  neighbourhood of a vertex in the K9-free colour of the 10768 colouring (Rowley Sec.6); its
             order is that vertex's degree, compared here with the 7173 the recipe needs.

XXER EJC 11 (2004) #R35: Theorem 7 (p.10-11) construction F on U_1..U_4, Corollary 3 (p.11) for more
colours, Corollary 5 (p.15): R(k1, 2k2-1, k3, ..) >= 4R(k1-1, k2, k3, ..) - 3, obtained from the Cor.3
colouring by merging the new triangle-free colour 1 with the colour bounded by k2.
Colour roles in quad(G, a, b):  a = the colour of G bounded by k1-1 (Thm 7's colour 3 = non-edges of G:
it also gets the matching between U_1,U_2 and between U_3,U_4); b = the colour bounded by k2 that the new
colour is merged into; every other colour behaves like Thm 7's colour 2.  Same block rules as
build_G1_G2/scripts/constructions.py xxer_quadruple (round 1, used for R(3,4,8), R(3,5,7), R(3,3,3,10/11)),
here in uint8 to fit 15040 x 15040 in memory.

Usage: python3 build_quad.py 9,9,9 | 8,8,9
Writes built/<name>.colormat.gz (one row per vertex, digit per edge, diagonal 0) and logs/builds_quad.jsonl.
"""
import sys, os, gzip, hashlib, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lib2 as L


def lengths_to_matrix(N, c):
    idx = np.abs(np.arange(N)[:, None] - np.arange(N)[None, :])
    C = np.array([0] + c[1:], dtype=np.uint8)[idx]
    return C


def quad(G, a, b):
    """G: n x n uint8, colours 1..r, diagonal 0.  Returns the 4n x 4n Cor.5 colouring (uint8), the new
    triangle-free colour already merged into b."""
    n = len(G)
    new = b                                  # merge (Cor.5): new colour 1 of Thm 7 is written as b
    F = np.zeros((4 * n, 4 * n), dtype=np.uint8)
    I = np.eye(n, dtype=bool)
    cross = G.copy(); cross[I] = new        # U_i1 x U_i2, i1 in {1,2}, i2 in {3,4}: new colour if j1 = j2, else G
    pair = np.full((n, n), new, dtype=np.uint8); pair[I] = a   # U_1 x U_2, U_3 x U_4: a if j1 = j2, else new colour
    blk = lambda i: slice(i * n, (i + 1) * n)
    for i in range(4): F[blk(i), blk(i)] = G
    for i1 in (0, 1):
        for i2 in (2, 3):
            F[blk(i1), blk(i2)] = cross; F[blk(i2), blk(i1)] = cross.T
    for i1, i2 in ((0, 1), (2, 3)):
        F[blk(i1), blk(i2)] = pair; F[blk(i2), blk(i1)] = pair.T
    np.fill_diagonal(F, 0)
    return F


def lift(perm, n):
    perm = np.asarray(perm); return np.concatenate([i * n + perm for i in range(4)])


def block_perms(n):
    return [np.concatenate([bp[i] * n + np.arange(n) for i in range(4)]) for bp in ([1, 0, 2, 3], [0, 1, 3, 2], [2, 3, 0, 1])]


def is_aut(C, perm):
    """C[perm[i], perm[j]] == C[i, j] for all i, j (row blocks to bound memory)."""
    n = len(C); step = 2048
    for s in range(0, n, step):
        if not (C[perm[s:s + step]][:, perm] == C[s:s + step]).all(): return False
    return True


def orbit0(n, gens):
    seen = {0}; todo = [0]
    while todo:
        v = todo.pop()
        for g in gens:
            w = int(g[v])
            if w not in seen: seen.add(w); todo.append(w)
    return len(seen)


def triangle_free_colour(N, c):
    S = {d for d in range(1, N) if True}
    out = []
    for col in sorted(set(c[1:])):
        L_ = [d for d in range(1, N) if c[d] == col]; Ls = set(L_)
        if not any((x + y) in Ls for x in L_ for y in L_ if x <= y and x + y < N): out.append(col)
    return out


def write_colormat_gz(C, path):
    h = hashlib.sha256()
    with gzip.GzipFile(path, 'wb', mtime=0) as f:
        for i in range(len(C)):
            row = (C[i] + 48).tobytes() + b'\n'
            h.update(row); f.write(row)
    return L.sha256_file(path), h.hexdigest()


def main():
    cell = sys.argv[1]
    name = {'9,9,9': 'r388_940', '8,8,9': 'r377_673'}[cell]
    N0, c0 = L.lengths_of(name)
    assert L.is_cyclic(N0, c0)
    tf = triangle_free_colour(N0, c0)
    assert len(tf) == 1, tf
    t = tf[0]; others = [x for x in sorted(set(c0[1:])) if x != t]
    deg0 = {str(col): L.degree(N0, c0, col) for col in sorted(set(c0[1:]))}
    G = lengths_to_matrix(N0, c0)
    X, Y = others
    # step 1: a = X (bound k-1 -> k), b = t (3 -> 5); Y unchanged
    F1 = quad(G, X, t)
    # step 2: (9,9,9): a = Y (8 -> 9), b = t (5 -> 9), X stays 9.
    #         (8,8,9): a = Y (7 -> 8), b = t (5 -> 9), X stays 8.
    F2 = quad(F1, Y, t)
    n1, n2 = len(F1), len(F2)
    deg1 = {str(col): int((F1[0] == col).sum()) for col in (t, X, Y)}
    deg2 = {str(col): int((F2[0] == col).sum()) for col in (t, X, Y)}
    regular2 = {str(col): bool(((F2 == col).sum(axis=1) == deg2[str(col)]).all()) for col in (t, X, Y)}
    # automorphisms: rotation of the cyclic input lifted twice, plus block permutations at both levels
    rot = (np.arange(N0) + 1) % N0
    gens1 = [lift(rot, N0)] + block_perms(N0)
    gens2 = [lift(g, n1) for g in gens1] + block_perms(n1)
    auto = all(is_aut(F2, g) for g in gens2)
    trans = orbit0(n2, gens2) == n2
    if cell == '9,9,9':
        roles = {str(X): 9, str(t): 9, str(Y): 9}; fname = 'R9^3_n15040.colormat.gz'; sl = 15041
    else:
        roles = {str(X): 8, str(t): 9, str(Y): 8}; fname = 'R8_8_9_n10768.colormat.gz'; sl = 10769
    sha, sha_raw = write_colormat_gz(F2, os.path.join(L.BUILT, fname))
    np.save(os.path.join('<scratch>', fname.replace('.colormat.gz', '.npy')), F2)
    rec = dict(cell=cell, survey_lower=sl, N=n2, N_ok=(n2 == sl - 1), file='built/' + fname, sha256=sha, sha256_uncompressed=sha_raw,
               construction='XXER EJC 11 (2004) #R35 Corollary 5 (p.15; Thm 7 construction pp.10-11, Cor.3 p.11) applied twice to the cyclic (3,%s;%d) of Rowley arXiv:2203.13476v3 (ancillary sheet col %s), as in Rowley Sec.6 (NDSATT4.tex l.296-300)' % (
                   '8,8' if cell == '9,9,9' else '7,7', N0, '23' if cell == '9,9,9' else '19'),
               inputs=[L.input_record(name)], input_triangle_free_colour=t, input_degrees=deg0,
               step1=dict(n=n1, a=X, b=t, degrees_v0=deg1), step2=dict(n=n2, a=Y, b=t, degrees_v0=deg2, regular=regular2),
               colour_bounds=roles, automorphisms=dict(generators=len(gens2), all_automorphisms=auto, transitive=trans),
               formula='16 x %d = %d' % (N0, 16 * N0))
    if cell == '8,8,9':
        d1 = deg0[str(t)]
        rec['R888'] = dict(K9_free_colour=t, degree_in_object=deg2[str(t)], predicted_by_XSR2_Lemma1=n1 + 3 * deg1[str(t)] + 1,
                           Rowley_formula_9d1_7x673_5=9 * d1 + 7 * 673 + 5, needed=7173,
                           note='neighbourhood of a vertex in the K9-free colour gives an (8,8,8)-colouring on degree vertices')
    L.log('builds_quad.jsonl', rec)


if __name__ == '__main__':
    main()
