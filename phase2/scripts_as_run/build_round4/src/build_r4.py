"""build_round4: build the witnesses for R(6,15) >= 401, R(7,18) >= 797 and R(6,21) >= 888 twice
(implementation A = build_G3/g3lib.py, unchanged copy; implementation B = impl_b.py, written here from
the papers) and compare SHA-256 of the canonical labelled adjacency text.  Writes built/*.g6,
built/MANIFEST.json and logs/build.jsonl.   Run from build_round4/:  python3 src/build_r4.py
"""
import os, sys, json, hashlib, random, time
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools')); sys.path.insert(0, os.path.join(HERE, 'src'))
import verify_ramsey as V
import g3lib as A
import impl_b as B
import networkx as nx

INP = os.path.join(HERE, 'inputs'); OUT = os.path.join(HERE, 'built'); LOG = os.path.join(HERE, 'logs')
INPUTS = {   # file -> (SHA-256 recorded by the folder that produced it, where it was recorded)
    'R5_8_n100_circ.g6': ('2ac7e64e0da4c3112846080c8ffd7384bc057fdcf2816d2f0f500b2e7959ea96', 'phase2/hunt3_two_colour/results.csv row 5,8'),
    'R4_17_n199_cyclo11.g6': ('712e243ab02e166b4635832040928022643904c99a0a352fdbce7881fe36f7a6', 'phase2/hunt3_two_colour/results.csv row 4,17'),
    'R6_20_n877_SLLLcubic.g6': ('ef50e6ab42e3814f4abd9118d26724df25c3a4ccd819774d7add6964a8ed20be', 'phase2/hunt2_two_colour/results.csv row 6,20'),
}
sha = lambda b: hashlib.sha256(b).hexdigest()
recs = []
def log(r):
    recs.append(r); print(json.dumps(r), flush=True)


def load_input(name, k, l):
    """returns 0/1 numpy adjacency with no K_k (orientation checked), and the edge list"""
    path = os.path.join(INP, name)
    h = V.sha256_file(path); assert h == INPUTS[name][0], (name, h)
    C = V.load_g6(path)
    n = len(C)
    # the .circ file next to it must describe the same graph
    circ = open(path.replace('.g6', '.circ')).read().strip()
    Cc = V.load('circulant', circ)
    assert (Cc == C).all(), 'g6 and circ differ'
    assert V.is_circulant(C)
    found_k, out_k = V.has_clique(C, 1, k, sym=True)
    found_k1, out_k1 = V.has_clique(C, 1, k - 1, sym=True)
    assert not found_k and found_k1, (name, out_k, out_k1)
    Adj = (C == 1).astype(np.uint8); np.fill_diagonal(Adj, 0)
    E = [(a, b) for a in range(n) for b in range(a + 1, n) if Adj[a][b]]
    log(dict(step='input', file=name, sha256=h, recorded_in=INPUTS[name][1], n=n, edges=len(E), degree=int(Adj[0].sum()),
             circ_file=os.path.basename(path.replace('.g6', '.circ')), circ_sha256=V.sha256_file(path.replace('.g6', '.circ')),
             g6_equals_circ=True, circulant=True, orientation='edges have no K_%d (clique.c --sym %s; K_%d present: %s)' % (k, out_k, k - 1, out_k1[:40])))
    return Adj, E


def first_clique(n, E, s):
    """lexicographically first s-clique, plain depth-first search (independent of clique.c)"""
    nb = [set() for _ in range(n)]
    for a, b in E: nb[a].add(b); nb[b].add(a)
    def ext(cl, cand):
        if len(cl) == s: return cl
        for x in sorted(cand):
            r = ext(cl + [x], {y for y in cand if y > x and y in nb[x]})
            if r: return r
        return None
    return ext([], set(range(n)))


def key_from_matrix(F):
    n = len(F)
    rows = [bytes((F[a, a + 1:] + 48).astype(np.uint8)) for a in range(n)]
    return b'%d\n' % n + b'\n'.join(rows) + b'\n'


def save(name, F, meta):
    g6 = nx.to_graph6_bytes(nx.from_numpy_array(F.astype(np.int64)), header=False)
    path = os.path.join(OUT, name); open(path, 'wb').write(g6)
    back = V.load_g6(path); Ab = (back == 1).astype(np.uint8); np.fill_diagonal(Ab, 0)
    assert (Ab == F).all(), 'g6 round trip'
    meta.update(file='built/' + name, sha256_file=V.sha256_file(path), n=int(len(F)), edges=int(F.sum() // 2),
                degrees=sorted(set(int(d) for d in F.sum(1))))
    return meta


def selftest():
    """implementations A and B agree on random small inputs (both constructions)"""
    rnd = random.Random(20261112); cnt = 0
    for t in range(30):
        m = rnd.randint(2, 9); E = [(a, b) for a in range(m) for b in range(a + 1, m) if rnd.random() < 0.5]
        M = np.zeros((m, m), np.uint8)
        for a, b in E: M[a][b] = M[b][a] = 1
        n, EB = B.thm9_edges(m, E)
        assert key_from_matrix(A.t9(M)) == B.adjacency_key(n, EB); cnt += 1
        k = rnd.randint(4, 6)
        if m >= k - 1:
            K = list(range(k - 1)); rnd.shuffle(K)
            for i in K:
                for j in K:
                    if i < j: M[i][j] = M[j][i] = 1
            E = [(a, b) for a in range(m) for b in range(a + 1, m) if M[a][b]]
            H = np.ones((k - 1, k - 1), np.uint8); np.fill_diagonal(H, 0)
            EH = [(a, b) for a in range(k - 1) for b in range(a + 1, k - 1)]
            FA = A.xsr2_thm3(M, H, K, list(range(k - 1)), 2)
            n, EB = B.xsr2_thm3_edges(m, E, k - 1, EH, K, list(range(k - 1)), 2)
            assert key_from_matrix(FA) == B.adjacency_key(n, EB); cnt += 1
    log(dict(step='selftest', random_cases=cnt, A_equals_B=True))


def main():
    os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)
    selftest()
    man = {}
    # ---------------- R(6,15) >= 401: XXER Thm 9 with k = 8, l = 6 on the (8,5;100)-graph = complement of the
    # (5,8;100) circulant; T9 gives an (15,6;400)-graph; its complement is the (6,15;400) witness.
    G58, E58 = load_input('R5_8_n100_circ.g6', 5, 8)
    G85 = A.complement(G58)
    FA = A.complement(A.t9(G85))
    _, E85 = B.complement_edges(100, E58)
    n, EB = B.thm9_edges(100, sorted(E85)); n, EB = B.complement_edges(n, EB)
    kA, kB = key_from_matrix(FA), B.adjacency_key(n, EB)
    meta = dict(cell='6,15', survey_lower=401, construction='XXER Theorem 9 (EJC 11 (2004) #R35, p. 15-16; colouring of Theorem 7, p. 11) with k = 8, l = 6, applied to the (8,5;100)-graph that is the complement of the (5,8;100) circulant; the resulting (15,6;400)-graph is complemented, so edges avoid K6 and non-edges avoid K15',
                survey_ref='DS1 rev 18, Table IIa p. 10 (6,15) 401 [2.3.i]; item 2.3.i p. 12',
                input=dict(file='R5_8_n100_circ.g6', sha256=INPUTS['R5_8_n100_circ.g6'][0]),
                impl_A_sha256=sha(kA), impl_B_sha256=sha(kB), identical=kA == kB)
    assert kA == kB
    man['6,15'] = save('R6_15_n400.g6', FA, meta); man['6,15']['canonical_adjacency_sha256'] = sha(kA)
    man['6,15']['vt_generators'] = 'input rotation lifted to the 4 blocks, block swaps (U1 U2), (U3 U4), (U1 U3)(U2 U4) (g3lib.t9_lift_perm, t9_block_perms)'
    log(dict(step='built', **{k: v for k, v in man['6,15'].items()}))

    # ---------------- R(7,18) >= 797: XXER Thm 9 with k = 4, l = 18 on the (4,17;199) graph -> (7,18;796), no complement.
    G417, E417 = load_input('R4_17_n199_cyclo11.g6', 4, 17)
    FA = A.t9(G417)
    n, EB = B.thm9_edges(199, E417)
    kA, kB = key_from_matrix(FA), B.adjacency_key(n, EB)
    meta = dict(cell='7,18', survey_lower=797, construction='XXER Theorem 9 (EJC 11 (2004) #R35, p. 15-16; colouring of Theorem 7, p. 11) with k = 4, l = 18, applied to the (4,17;199) cyclotomic circulant; edges avoid K7, non-edges avoid K18',
                survey_ref='DS1 rev 18, Table IIa p. 10 (7,18) 797 [2.3.i]; item 2.3.i p. 12',
                input=dict(file='R4_17_n199_cyclo11.g6', sha256=INPUTS['R4_17_n199_cyclo11.g6'][0]),
                impl_A_sha256=sha(kA), impl_B_sha256=sha(kB), identical=kA == kB)
    assert kA == kB
    man['7,18'] = save('R7_18_n796.g6', FA, meta); man['7,18']['canonical_adjacency_sha256'] = sha(kA)
    man['7,18']['vt_generators'] = man['6,15']['vt_generators']
    log(dict(step='built', **man['7,18']))

    # ---------------- R(6,21) >= 888: XSR2 Theorem 3 / Corollary 3 with k = 6, s = 20, t = 2: G = (6,20;877) cubic-residue
    # graph, H = M = K5 (M = the lexicographically first K5 of G), W1 = first 2 vertices of M, W2 = last 3.
    G620, E620 = load_input('R6_20_n877_SLLLcubic.g6', 6, 20)
    K = first_clique(877, E620, 5)
    assert G620[np.ix_(K, K)].sum() == 20
    H5 = np.ones((5, 5), np.uint8); np.fill_diagonal(H5, 0)
    FA = A.xsr2_thm3(G620, H5, K, list(range(5)), 2)
    n, EB = B.xsr2_thm3_edges(877, E620, 5, [(a, b) for a in range(5) for b in range(a + 1, 5)], K, list(range(5)), 2)
    kA, kB = key_from_matrix(FA), B.adjacency_key(n, EB)
    meta = dict(cell='6,21', survey_lower=888, construction='XSR2 Theorem 3 (SIAM J. Discrete Math. 25 (2011) 394-400; preprint p. 4-5) in the special case of Corollary 3 (preprint p. 6: H = M = K_{k-1}, W1 = K2, W2 = K_{k-3}) with k = 6, s = 20, t = 2: G = (6,20;877) cubic-residue graph Cay(Z_877, cubes) (SLLL), H = K5, M = K5 on G-vertices %s; vertex order V(G) 0..876, V(H) 877..881, W 882..886; edges avoid K6, non-edges avoid K21' % K,
                survey_ref='DS1 rev 18, Table IIa p. 10 (6,21) 888 [2.3.h]; item 2.3.h p. 12 (term k-2 for k >= 5 from XSR2)',
                input=dict(file='R6_20_n877_SLLLcubic.g6', sha256=INPUTS['R6_20_n877_SLLLcubic.g6'][0]),
                clique_in_G=K, impl_A_sha256=sha(kA), impl_B_sha256=sha(kB), identical=kA == kB)
    assert kA == kB
    man['6,21'] = save('R6_21_n887.g6', FA, meta); man['6,21']['canonical_adjacency_sha256'] = sha(kA)
    log(dict(step='built', **man['6,21']))
    json.dump(man, open(os.path.join(OUT, 'MANIFEST.json'), 'w'), indent=1)
    with open(os.path.join(LOG, 'build.jsonl'), 'a') as f:
        for r in recs: f.write(json.dumps(r) + '\n')


if __name__ == '__main__':
    main()
