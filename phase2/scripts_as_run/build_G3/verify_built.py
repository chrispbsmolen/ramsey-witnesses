"""Check one half of one built G3 graph with one of the two checkers.

  python3 verify_built.py CELL HALF CHECKER TIMEOUT_S
     CELL     e.g. 7,11 (a key of built/manifest.json)
     HALF     clique  (no K_k in the graph)   or   indep  (no independent l-set)
     CHECKER  repo    (tools/verify_ramsey.py has_clique, i.e. clique.c; an unchanged copy of the repo's)
              nx      (networkx maximal-clique enumeration, as in repo/crosscheck.py; no shared solver code)
Appends one JSON record to logs/verify.jsonl.

Symmetry: when built/manifest.json lists vt_generators for the graph, every generator is first
checked to be an automorphism and the group they generate is checked to be vertex transitive
(orbit of vertex 0 = all vertices).  Only then is the search restricted to cliques through
vertex 0 (repo: clique.c --sym; nx: cliques of the subgraph induced by the neighbourhood of 0).
This is the same shortcut verify_ramsey.py applies to circulants, with the symmetry proved here
by explicit automorphisms instead of the circulant test.
"""
import os, sys, json, time, gzip, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools')); sys.path.insert(0, HERE)
import verify_ramsey as V
import g3lib as L

SURVEY = {'5,15': 275, '6,15': 401, '7,11': 405, '7,12': 417, '8,11': 457, '8,13': 817, '8,15': 873, '9,10': 581,
          '10,15': 1313, '5,18': 396, '5,21': 441, '5,23': 521, '6,21': 888, '7,16': 629, '7,17': 729, '7,18': 797,
          '8,17': 1005, '8,19': 1237, '8,21': 1617, 'aux_7,8': 217}

NXCHILD = r'''
import sys, json, numpy as np, networkx as nx
A = np.load(sys.argv[1]); s = int(sys.argv[2]); sym = sys.argv[3] == '1'
if sym:
    nb = np.nonzero(A[0])[0]; G = nx.from_numpy_array(A[np.ix_(nb, nb)]); need = s - 1
else:
    G = nx.from_numpy_array(A); need = s
best = 0; cnt = 0
for c in nx.find_cliques(G):
    cnt += 1
    if len(c) > best: best = len(c)
    if best >= need: break
print(json.dumps(dict(best=best + (1 if sym else 0), maximal_cliques=cnt, found=best >= need)), flush=True)
'''


def load_built(cell):
    man = json.load(open(os.path.join(HERE, 'built', 'manifest.json')))
    m = man[cell]; path = os.path.join(HERE, m['file'])
    assert V.sha256_file(path) == m['sha256_file']
    raw = gzip.open(path).read() if path.endswith('.gz') else open(path, 'rb').read()
    assert L.sha256(raw.strip() + b'\n') == m['sha256_g6'] or L.sha256(raw) == m['sha256_g6']
    C = V.from_g6(raw.strip())
    return C, m


def main():
    cell, half, checker, T = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
    C, m = load_built(cell)
    k, l = [int(x) for x in cell.replace('aux_', '').split(',')]
    n = len(C)
    rec = dict(cell=cell, half=half, checker=checker, n=n, timeout=T, sha256_file=m['sha256_file'],
               n_ok=(n == SURVEY[cell] - 1))
    A = (C == 1).astype(np.uint8); np.fill_diagonal(A, 0)
    sym = False
    if 'vt_generators' in m:
        gens = [np.array(g) for g in m['vt_generators']]
        auto = all(L.is_automorphism(A, g) for g in gens)
        trans = L.orbit_of_0(n, gens) == n
        rec['vt_checked'] = dict(generators=len(gens), all_automorphisms=auto, transitive=trans)
        sym = auto and trans
    rec['sym'] = sym
    colour, size = (1, k) if half == 'clique' else (0, l)
    t0 = time.time()
    if checker == 'repo':
        try:
            found, out = V.has_clique(C, colour, size, sym=sym, timeout=T)
            rec['result'] = 'FOUND' if found else 'NONE'; rec['solver'] = out[:200]
        except subprocess.TimeoutExpired:
            rec['result'] = 'TIMEOUT'
    else:
        X = A if colour == 1 else L.complement(A)
        tmp = os.path.join(HERE, 'logs', 'tmp_%s_%s.npy' % (cell.replace(',', '_'), half))
        np.save(tmp, X.astype(np.uint8))
        try:
            p = subprocess.run([sys.executable, '-c', NXCHILD, tmp, str(size), '1' if sym else '0'], capture_output=True, text=True, timeout=T)
            r = json.loads(p.stdout.strip().split('\n')[-1]); rec.update(nx=r)
            rec['result'] = 'FOUND' if r['found'] else 'NONE'
        except subprocess.TimeoutExpired:
            rec['result'] = 'TIMEOUT'
        finally:
            os.remove(tmp)
    rec['seconds'] = round(time.time() - t0, 1)
    rec['claim'] = ('no K_%d' if half == 'clique' else 'no independent %d-set') % size
    print(json.dumps(rec))
    open(os.path.join(HERE, 'logs', 'verify.jsonl'), 'a').write(json.dumps(rec) + '\n')


if __name__ == '__main__':
    main()
