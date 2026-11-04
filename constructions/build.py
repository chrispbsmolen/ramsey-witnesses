"""Build the witnesses constructed here and write them to constructions/witnesses/.

  c5_R3_3.g6            the 5-cycle: R(3,3) > 5
  clebsch16_R3_3_3.txt  GF(16)* split into the three cosets of the cubes; edge {x, y} gets the coset
                        of x + y (Greenwood-Gleason): R(3,3,3) > 16.  Colour matrix, one digit per edge,
                        the diagonal written as 0 and ignored by the loader
  cubic127_R4_12.g6     Z_127, x ~ y iff x - y is a nonzero cube mod 127: R(4,12) > 127
  cubic3_127_R4_4_4.txt Z_127, edge {x, y} coloured by the coset of x - y modulo the cubes (the discrete
                        logarithm of x - y to the primitive root 3, mod 3): R(4,4,4) > 127.  Colour matrix
                        as for clebsch16
  paleyP_Rk_k.g6        Paley graph Q_p: R(w+1, w+1) > p where w = clique number of Q_p
  mathonP_Rk_k.g6       the doubling of Q_p on 2p + 2 vertices (paley.mathon(p, 'nonres', 0, 0)):
                        R(w+2, w+2) > 2p + 2

The files are deterministic; rerunning this script must reproduce them byte for byte (the SHA-256
values are in sources/manifest.csv).  Whether each one is a witness is decided by run_ramsey.py,
not here.  Run from the repository root: python3 constructions/build.py
"""
import os, sys, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paley import paley, mathon
OUT = os.path.join(HERE, 'witnesses')


def g6(A):
    import networkx as nx
    return nx.to_graph6_bytes(nx.from_numpy_array(np.array(A)), header=False)


def gf16_mul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        b >>= 1; a <<= 1
        if a & 16: a ^= 0b10011          # x^4 + x + 1, for which x is primitive
    return r


def clebsch16():
    pw = [1]
    for _ in range(14): pw.append(gf16_mul(pw[-1], 2))
    log = {v: i for i, v in enumerate(pw)}
    assert len(log) == 15
    rows = []
    for a in range(16):
        rows.append(''.join('0' if a == b else str(log[a ^ b] % 3) for b in range(16)))
    return ('\n'.join(rows) + '\n').encode()


def cubic(p):
    Q = {pow(x, 3, p) for x in range(1, p)}
    A = np.zeros((p, p), dtype=np.int64)
    for i in range(p):
        for j in range(p):
            if i != j and (i - j) % p in Q: A[i][j] = 1
    return A


def cubic_cosets(p, g=3):
    log = {}; x = 1
    for e in range(p - 1):
        log[x] = e; x = x * g % p
    assert len(log) == p - 1                  # g is a primitive root mod p
    rows = [''.join('0' if a == b else str(log[(a - b) % p] % 3) for b in range(p)) for a in range(p)]
    return ('\n'.join(rows) + '\n').encode()


def cycle(n):
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n): A[i][(i + 1) % n] = A[(i + 1) % n][i] = 1
    return A


if __name__ == '__main__':
    files = {
        'c5_R3_3.g6': g6(cycle(5)),
        'clebsch16_R3_3_3.txt': clebsch16(),
        'cubic127_R4_12.g6': g6(cubic(127)),
        'cubic3_127_R4_4_4.txt': cubic_cosets(127),
        'paley101_R6_6.g6': g6(paley(101)),
        'mathon101_R7_7.g6': g6(mathon(101, 'nonres', 0, 0)),
        'paley281_R8_8.g6': g6(paley(281)),
        'mathon281_R9_9.g6': g6(mathon(281, 'nonres', 0, 0)),
        'paley797_R10_10.g6': g6(paley(797)),
    }
    os.makedirs(OUT, exist_ok=True)
    for name, data in files.items():
        open(os.path.join(OUT, name), 'wb').write(data)
        print(name, hashlib.sha256(data).hexdigest())
