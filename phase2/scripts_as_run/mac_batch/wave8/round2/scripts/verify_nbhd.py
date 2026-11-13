"""Symmetry-reduced check of a vertex-transitive colouring stored as built/*.colormat.gz (XXER Cor.5
quadruplings) or as a two-colour g6 file.  Steps, all on the built file itself:
  1. load it, check its SHA-256 against the build log, check symmetry/zero diagonal;
  2. rebuild the automorphism generators (rotation of the cyclic input lifted through each quadrupling, and
     the block permutations (U1 U2), (U3 U4), (U1 U3)(U2 U4) at each level; build_quad.py), check that each
     is an automorphism of the loaded matrix and that they move vertex 0 to every vertex;
  3. feed the subgraph induced by N(0) in colour COL to ONE checker, looking for K_{k-1}:
       repo : checker/clique_r2 (= repo clique.c, compiled under a new name), no --sym
       gen0 : checker/gen0_r2 (linear0.c's search on a plain graph; independent of clique.c)
Usage: python3 verify_nbhd.py FILE N0 LEVELS COL K CHECKER [MAXV|-] [TIMEOUT]
  N0 = order of the cyclic input, LEVELS = number of quadruplings (2 here).
Appends one JSON line to logs/verify_nbhd.jsonl.
"""
import sys, os, json, time, gzip, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lib2 as L
import build_quad as Q

def load_colormat_gz(path):
    rows = gzip.open(path).read().split(b'\n')
    rows = [r for r in rows if r]
    n = len(rows)
    C = np.frombuffer(b''.join(rows), dtype=np.uint8).reshape(n, n) - 48
    return C

def main():
    path, N0, levels, col, k, checker = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    maxv = sys.argv[7] if len(sys.argv) > 7 else '-'
    T = float(sys.argv[8]) if len(sys.argv) > 8 else 560
    full = os.path.join(L.OUT, path)
    rec = dict(file=path, sha256=L.sha256_file(full), colour=col, k=k, checker=checker, maxv=maxv, timeout=T)
    t0 = time.time()
    C = load_colormat_gz(full); n = len(C)
    assert (C == C.T).all() and (np.diag(C) == 0).all()
    rot = (np.arange(N0) + 1) % N0
    gens = [rot]; m = N0
    for _ in range(levels):
        gens = [Q.lift(g, m) for g in gens] + Q.block_perms(m); m *= 4
    assert m == n
    rec['automorphisms'] = dict(generators=len(gens), all_automorphisms=all(Q.is_aut(C, g) for g in gens), transitive=Q.orbit0(n, gens) == n)
    assert rec['automorphisms']['all_automorphisms'] and rec['automorphisms']['transitive']
    S = np.nonzero(C[0] == col)[0]
    rec['n'] = n; rec['degree0'] = int(len(S))
    exe = {'repo': [os.environ.get('CLIQUE_BIN', os.path.join(L.CHECKER, 'clique_r2')), str(k - 1)],
           'gen0': [os.environ.get('GEN0_BIN', os.path.join(L.CHECKER, 'gen0_r2')), str(k - 1)] + ([maxv] if maxv != '-' else [])}[checker]
    outf = tempfile.TemporaryFile(); errf = tempfile.TemporaryFile()
    pr = subprocess.Popen(['bash', '-c', 'ulimit -s unlimited; exec "$@"', 'x'] + exe, stdin=subprocess.PIPE, stdout=outf, stderr=errf)
    pr.stdin.write(b'%d\n' % len(S))
    sub = C[np.ix_(S, S)] == col
    for i in range(len(S)):
        pr.stdin.write((sub[i].astype(np.uint8) + 48).tobytes() + b'\n')
    pr.stdin.close()
    try:
        pr.wait(timeout=T)
        outf.seek(0); errf.seek(0)
        rec['result'] = outf.read().decode().strip(); rec['stderr'] = errf.read().decode().strip()[-200:]
    except subprocess.TimeoutExpired:
        pr.kill(); rec['result'] = 'TIMEOUT'
    rec['seconds'] = round(time.time() - t0, 1)
    L.log('verify_nbhd.jsonl', rec)

if __name__ == '__main__':
    main()
