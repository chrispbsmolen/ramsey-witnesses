"""R(5,23) >= 521: XXER EJC 11 (2004) #R35 Theorem 9 (pp.15-16; (14): R(5,l) >= 4R(3,l-1)-3), applied to the
(3,22;130) circulant of Wu-Su-Luo-Xu EJC 17 (2010) #N25 Thm 1 proof part 1) p.7 (WSLX2 p.8 states this use).
The T9 graph is built with build_G3/g3lib.py t9() (round-1 G3 code, used there for 14 cells), unchanged.
Checks (one JSON line each to logs/verify_r5_23.jsonl):
  clique half: no K5, by verify_ramsey.has_clique (repo clique.c) with --sym and by networkx find_cliques on
  the neighbourhood of vertex 0, after the generators (input rotation lifted to the four blocks, block
  permutations (U1 U2), (U3 U4), (U1 U3)(U2 U4)) are checked to be automorphisms acting transitively.
  independence half: no independent 23-set; timed attempt only (clique.c --sym, 300 s)."""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '<cloud>/ramsey-p2/build_G3')
import numpy as np, networkx as nx
import lib2 as L, g3lib as G3
import verify_ramsey as V

path = L.pin('r3_22_130')
n0, ds = open(path).read().strip().split(':'); n0 = int(n0); ds = [int(x) for x in ds.split(',')]
A = np.zeros((n0, n0), dtype=np.uint8)
for i in range(n0):
    for d in ds: A[i][(i + d) % n0] = A[(i + d) % n0][i] = 1
F = G3.t9(A)
n = len(F)
g6 = nx.to_graph6_bytes(nx.from_numpy_array(F.astype(int)), header=False)
out = os.path.join(L.BUILT, 'R5_23_n520.g6'); open(out, 'wb').write(g6)
gens = [G3.t9_lift_perm((np.arange(n0) + 1) % n0, n0)] + G3.t9_block_perms(n0)
auto = all(G3.is_automorphism(F, g) for g in gens); trans = G3.orbit_of_0(n, gens) == n
rec = dict(cell='5,23', survey_lower=521, N=n, N_ok=(n == 520), file='built/R5_23_n520.g6', sha256=L.sha256_file(out),
           construction='XXER EJC 11 (2004) #R35 Theorem 9 pp.15-16 (eq. (14)) on the (3,22;130) WSLX2 circulant; build_G3/g3lib.py t9()',
           inputs=[L.input_record('r3_22_130'), dict(name='g3lib.py', file='<cloud>/ramsey-p2/build_G3/g3lib.py', sha256=L.sha256_file('<cloud>/ramsey-p2/build_G3/g3lib.py'))],
           input_check=dict(triangle_free_input=not V.has_clique(np.where(A == 1, 1, 0) - np.eye(n0, dtype=int) * 1, 1, 3, sym=True)[0]),
           automorphisms=dict(generators=len(gens), all_automorphisms=auto, transitive=trans))
L.log('builds_two.jsonl', rec)
C = F.astype(np.int64); np.fill_diagonal(C, -1)
t = time.time(); r = V.has_clique(C, 1, 5, sym=True)
L.log('verify_r5_23.jsonl', dict(cell='5,23', half='clique (no K5)', checker='repo clique.c --sym', result=r[1], seconds=round(time.time() - t, 1)))
t = time.time(); nb = np.nonzero(F[0])[0]
w = max(len(c) for c in nx.find_cliques(nx.from_numpy_array(F[np.ix_(nb, nb)].astype(int)))) + 1
L.log('verify_r5_23.jsonl', dict(cell='5,23', half='clique (no K5)', checker='networkx find_cliques on N(0) (+1)', omega=int(w), result='NONE' if w < 5 else 'FOUND', seconds=round(time.time() - t, 1)))
# negative control: K4 must be found
L.log('verify_r5_23.jsonl', dict(cell='5,23', half='negative control: K4 must exist', checker='repo clique.c --sym', result=V.has_clique(C, 1, 4, sym=True)[1][:60]))
t = time.time()
try:
    r = V.has_clique(C, 0, 23, sym=True, timeout=300); res = r[1][:80]
except subprocess.TimeoutExpired:
    res = 'TIMEOUT 300 s'
    subprocess.run(['pkill', '-f', os.path.join(L.CHECKER, 'clique') + ' 23'])
L.log('verify_r5_23.jsonl', dict(cell='5,23', half='independence (no independent 23-set)', checker='repo clique.c --sym', result=res, seconds=round(time.time() - t, 1)))
