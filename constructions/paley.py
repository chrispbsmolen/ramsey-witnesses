"""Paley graphs Q_p (p prime, p = 1 mod 4) and Mathon-Shearer doublings on 2p+2 vertices."""
import numpy as np, itertools, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import verify_ramsey as V

def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True

def residues(p): return {(x * x) % p for x in range(1, p)}

def paley(p):
    Q = residues(p)
    A = np.zeros((p, p), dtype=np.int64)
    for i in range(p):
        for j in range(p):
            if i != j and (i - j) % p in Q: A[i][j] = 1
    return A

def mathon(p, cross='nonres', inf_inf=0, inf_cross=0):
    """vertices: u, v, (x,1) for x in Z_p, (x,2) for x in Z_p.
    within each copy: Paley adjacency; u ~ all (x,1); v ~ all (x,2) (or the reverse if inf_cross);
    (x,1) ~ (y,2) iff x - y is in the chosen class; u ~ v iff inf_inf."""
    Q = residues(p); N = set(range(1, p)) - Q
    cls = {'nonres': N, 'res': Q, 'nonres0': N | {0}, 'res0': Q | {0}}[cross]
    n = 2 * p + 2; A = np.zeros((n, n), dtype=np.int64)
    P = paley(p)
    A[2:2 + p, 2:2 + p] = P; A[2 + p:, 2 + p:] = P
    for x in range(p):
        for y in range(p):
            if (x - y) % p in cls: A[2 + x][2 + p + y] = A[2 + p + y][2 + x] = 1
    if not inf_cross:
        A[0, 2:2 + p] = A[2:2 + p, 0] = 1; A[1, 2 + p:] = A[2 + p:, 1] = 1
    else:
        A[0, 2 + p:] = A[2 + p:, 0] = 1; A[1, 2:2 + p] = A[2:2 + p, 1] = 1
    A[0][1] = A[1][0] = inf_inf
    return A

def clique_number(A, upto=60, sym=False):
    C = V.from_adjacency(A); w = 1
    for s in range(2, upto):
        if V.has_clique(C, 1, s, sym=sym)[0]: w = s
        else: break
    return w

if __name__ == '__main__':
    # derive the doubling rule on small primes: Q_p with omega = k - 1 must give a (k+1,k+1)-graph on 2p+2 vertices
    for p in [5, 13, 17, 29, 37, 41]:
        P = paley(p); w = clique_number(P, sym=True)
        ok = []
        for cross in ['nonres', 'res', 'nonres0', 'res0']:
            for ii in (0, 1):
                for ic in (0, 1):
                    A = mathon(p, cross, ii, ic)
                    C = V.from_adjacency(A)
                    good = not V.has_clique(C, 1, w + 2)[0] and not V.has_clique(C, 0, w + 2)[0]
                    if good: ok.append((cross, ii, ic))
        print('p=%d omega(Q_p)=%d  variants giving R(%d,%d) > %d:' % (p, w, w + 2, w + 2, 2 * p + 2), ok, flush=True)
