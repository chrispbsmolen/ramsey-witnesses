"""G2: Shearer-Mathon doubling of the Paley graph Q_p (survey 2.2.c) for
p = 797, 1277, 1493, 2741, 2801 (R(11,11), R(13,13), R(14,14), R(15,15), R(16,16)).
Usage: python3 build_G2.py omega P...   exact clique number of Q_p (edge-transitivity, as repo/constructions/paley_omega.py)
       python3 build_G2.py build P...   write built/mathon<P>_R<k>_<k>.g6.gz and log it
       python3 build_G2.py compare      check the construction against repo's verified mathon101 / mathon281 files
"""
import sys, os, json, time, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, lib, constructions as K
V = lib.V
LOG = os.path.join(lib.OUT, 'logs')
CELL = {797: '11,11', 1277: '13,13', 1493: '14,14', 2741: '15,15', 2801: '16,16'}


def clique_through_edge(p, s):
    """Q_p is arc-transitive (x -> a x + b, a a nonzero square), so a K_s (s >= 2) exists iff one
    contains the edge {0, 1}, i.e. iff N(0) & N(1) holds a K_{s-2}."""
    Q = set(K.quadratic_residues(p).tolist())
    if s <= 2: return True
    W = [x for x in range(2, p) if x in Q and (x - 1) % p in Q]
    idx = np.array(W)
    D = (idx[:, None] - idx[None, :]) % p
    A = np.isin(D, list(Q)); np.fill_diagonal(A, False)
    C = np.where(A, 1, 0); np.fill_diagonal(C, -1)
    return V.has_clique(C, 1, s - 2)[0], len(W)


def omega(p):
    s = 2; t0 = time.time(); m = None
    while True:
        r = clique_through_edge(p, s + 1)
        if isinstance(r, tuple): r, m = r
        if not r: break
        s += 1
    return s, m, round(time.time() - t0, 1)


def main():
    cmd = sys.argv[1]
    if cmd == 'omega':
        for p in map(int, sys.argv[2:]):
            w, m, sec = omega(p)
            rec = dict(p=p, omega=w, common_nbhd_size=m, seconds=sec, time=time.strftime('%Y-%m-%d %H:%M:%S'),
                       paley_bound='R(%d,%d) > %d' % (w + 1, w + 1, p), doubling_bound='R(%d,%d) > %d' % (w + 2, w + 2, 2 * p + 2))
            open(os.path.join(LOG, 'paley_omega.jsonl'), 'a').write(json.dumps(rec) + '\n'); print(json.dumps(rec), flush=True)
    elif cmd == 'build':
        for p in map(int, sys.argv[2:]):
            C = K.paley_doubling(p)
            assert len(C) == 2 * p + 2
            k = {797: 11, 1277: 13, 1493: 14, 2741: 15, 2801: 16}[p]
            name = 'mathon%d_R%d_%d.g6.gz' % (p, k, k)
            sha = lib.write_g6(C, os.path.join(lib.OUT, 'built', name))
            rec = dict(cell=CELL[p], file='built/' + name, n=len(C), ks=[k, k], sha256=sha, p=p,
                       construction='Shearer-Mathon doubling of Q_p (XXER p. 12-13)', time=time.strftime('%Y-%m-%d %H:%M:%S'))
            open(os.path.join(LOG, 'builds.jsonl'), 'a').write(json.dumps(rec) + '\n'); print(json.dumps(rec), flush=True)
    elif cmd == 'compare':
        import networkx as nx
        for p, f in ((101, 'mathon101_R7_7.g6'), (281, 'mathon281_R9_9.g6')):
            path = os.path.join(lib.REPO, 'constructions', 'witnesses', f)
            R = V.load_g6(path)
            C = K.paley_doubling(p)
            same = bool((R == C).all())
            print(json.dumps(dict(p=p, repo_file=f, repo_sha256=lib.sha256_file(path), identical_matrix=same)))
        # Mathon's own m = 2 scheme in the form of XuR1 p. 2 (vertices (0,1),(0,b), V_i = {(b^i, a)}; edge iff the
        # quadratic character of xt - ys is 'residue'; the special colour on det = 0 pairs taken as non-edge)
        for p in (13, 17, 29, 37, 41, 101):
            b = K.primitive_root(p); QR = set(K.quadratic_residues(p).tolist())
            verts = [(0, 1), (0, b)] + [(pow(b, i, p), a) for i in range(2) for a in range(p)]
            n = len(verts); A = np.zeros((n, n), dtype=int)
            for i in range(n):
                for j in range(i + 1, n):
                    d = (verts[i][0] * verts[j][1] - verts[i][1] * verts[j][0]) % p
                    if d in QR: A[i][j] = A[j][i] = 1
            G1 = nx.from_numpy_array(A); G2 = nx.from_numpy_array((K.paley_doubling(p) == 1).astype(int))
            print(json.dumps(dict(p=p, mathon_m2_isomorphic_to_doubling=nx.is_isomorphic(G1, G2))), flush=True)


if __name__ == '__main__':
    main()
