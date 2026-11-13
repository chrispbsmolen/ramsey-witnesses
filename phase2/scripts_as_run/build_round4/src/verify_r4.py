"""Check one half of one build_round4 graph with one checker.  One JSON line to logs/verify.jsonl.

  python3 src/verify_r4.py CELL HALF CHECKER MODE TIMEOUT [NEG]
    CELL     6,15 | 7,18 | 6,21                    (key of built/MANIFEST.json)
    HALF     clique (no K_k, colour = edges)  |  indep (no independent l-set, colour = non-edges)
    CHECKER  repo  tools/verify_ramsey.py has_clique = clique.c (unchanged repo copy, SHA-256 137a1002...)
             nx    networkx find_cliques (as in repo crosscheck.py; no shared solver code)
             gen0  build_round2 checker/gen0.c (linear0 search, independent of clique.c)
    MODE     full  whole graph, no symmetry
             sym   cliques through vertex 0 only, after the generators (input rotation lifted to the four
                   blocks, block swaps (U1 U2), (U3 U4), (U1 U3)(U2 U4)) are checked on the loaded matrix to be
                   automorphisms acting transitively (Theorem 9 cells only).  repo: clique.c --sym;
                   nx and gen0: search K_(s-1) in the subgraph induced by the colour-neighbourhood of 0.
    NEG      'neg' = negative control: search size s-1 instead of s (must be FOUND).
"""
import os, sys, json, time, subprocess, tempfile
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools')); sys.path.insert(0, os.path.join(HERE, 'src'))
import verify_ramsey as V
import g3lib as L

NXCHILD = r'''
import sys, json, numpy as np, networkx as nx
A = np.load(sys.argv[1]); need = int(sys.argv[2])
G = nx.from_numpy_array(A)
best = 0; cnt = 0
for c in nx.find_cliques(G):
    cnt += 1
    if len(c) > best: best = len(c)
    if best >= need: break
print(json.dumps(dict(best=best, maximal_cliques=cnt, found=best >= need)), flush=True)
'''
INPUT_N = {'6,15': 100, '7,18': 199}


def main():
    cell, half, checker, mode, T = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5])
    neg = len(sys.argv) > 6 and sys.argv[6] == 'neg'
    man = json.load(open(os.path.join(HERE, 'built', 'MANIFEST.json')))[cell]
    path = os.path.join(HERE, man['file'])
    h = V.sha256_file(path); assert h == man['sha256_file']
    C = V.load_g6(path); n = len(C)
    k, l = [int(x) for x in cell.split(',')]
    A = (C == 1).astype(np.uint8); np.fill_diagonal(A, 0)
    rec = dict(cell=cell, half=half, checker=checker, mode=mode, n=n, n_ok=n == man['survey_lower'] - 1, sha256_file=h, timeout=T)
    colour, s = (1, k) if half == 'clique' else (0, l)
    if neg: s -= 1; rec['negative_control'] = 'size %d must be FOUND' % s
    X = A if colour == 1 else L.complement(A)
    if mode == 'sym':
        m = INPUT_N[cell]
        gens = [L.t9_lift_perm((np.arange(m) + 1) % m, m)] + L.t9_block_perms(m)
        auto = all(L.is_automorphism(A, g) for g in gens); trans = L.orbit_of_0(n, gens) == n
        rec['automorphisms'] = dict(generators=len(gens), all_automorphisms=auto, transitive=trans)
        assert auto and trans
    rec['claim'] = ('no K_%d' if half == 'clique' else 'no independent %d-set') % s
    t0 = time.time()
    if checker == 'repo':
        try:
            found, out = V.has_clique(C, colour, s, sym=(mode == 'sym'), timeout=T)
            rec['result'] = 'FOUND' if found else 'NONE'; rec['solver'] = out[:120]
        except subprocess.TimeoutExpired:
            rec['result'] = 'TIMEOUT'
    else:
        if mode == 'sym':
            nb = np.nonzero(X[0])[0]; Y = X[np.ix_(nb, nb)]; need = s - 1
        else:
            Y = X; need = s
        rec['searched_order'] = int(len(Y)); rec['searched_size'] = need
        if checker == 'nx':
            tmp = tempfile.NamedTemporaryFile(suffix='.npy', delete=False); tmp.close()
            np.save(tmp.name, Y.astype(np.uint8))
            try:
                p = subprocess.run([sys.executable, '-c', NXCHILD, tmp.name, str(need)], capture_output=True, text=True, timeout=T)
                r = json.loads(p.stdout.strip().split('\n')[-1]); rec['nx'] = r
                rec['result'] = 'FOUND' if r['found'] else 'NONE'
            except subprocess.TimeoutExpired:
                rec['result'] = 'TIMEOUT'
            finally:
                os.remove(tmp.name)
        else:
            inp = ('%d\n' % len(Y)).encode() + b'\n'.join(bytes((row + 48).astype(np.uint8)) for row in Y) + b'\n'
            try:
                p = subprocess.run([os.path.join(HERE, 'tools', 'gen0'), str(need)], input=inp, capture_output=True, timeout=T)
                out = p.stdout.decode().strip(); rec['solver'] = out
                rec['result'] = out.split()[0] if out.split()[0] in ('FOUND', 'NONE') else 'ERROR'
            except subprocess.TimeoutExpired:
                rec['result'] = 'TIMEOUT'
    rec['seconds'] = round(time.time() - t0, 1)
    print(json.dumps(rec), flush=True)
    open(os.path.join(HERE, 'logs', 'verify.jsonl'), 'a').write(json.dumps(rec) + '\n')


if __name__ == '__main__':
    main()
