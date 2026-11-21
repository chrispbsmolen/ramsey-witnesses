#!/usr/bin/env python3
"""build_xxer7.py - the (3,k,l;4m) colouring of Xu, Xie, Exoo, Radziszowski, EJC 11 (2004) #R35, Theorem 7 (p.11),
from a (k,l-1;m)-graph G, built with the unchanged function xxer_quadruple() of
phase2/build_G1_G2/scripts/constructions.py (byte copy in ../tools, SHA-256 printed).

Input: matrix01 file (n lines of n characters 0/1), '1' = edge of G.  The file is loaded with
verify_ramsey.load_matrix01 (colour 1 = edge, colour 0 = non-edge).  xxer_quadruple(G, a_colour=0) returns a matrix
with 0 = non-edge of G (paper colour 3), 1 = edge of G (paper colour 2), 2 = the new colour (paper colour 1).
Canonical output: colormat, 4m lines of 4m digits, vertex (u_i, v_j) at index (i-1)m + (j-1), digit = paper colour - 1
(0: new triangle-free colour 1; 1: colour 2, edges of G; 2: colour 3, non-edges of G), diagonal written '0'.
usage: build_xxer7.py G.matrix01 OUT.colormat"""
import sys, os, json, hashlib
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import verify_ramsey as V
import constructions as K
src, out = sys.argv[1], sys.argv[2]
G = V.load_matrix01(src); m = len(G)
assert set(G[G >= 0].tolist()) == {0, 1}
F = K.xxer_quadruple(G, 0)
n = len(F); assert n == 4 * m
off = ~np.eye(n, dtype=bool)
assert (F == F.T).all() and set(F[off].tolist()) == {0, 1, 2} and (np.diag(F) == -1).all()
paper = {2: 1, 1: 2, 0: 3}                      # constructions.py colour -> paper colour
with open(out, 'w') as f:
    f.write('\n'.join(''.join('0' if i == j else str(paper[int(F[i][j])] - 1) for j in range(n)) for i in range(n)) + '\n')
print(json.dumps({'input': os.path.basename(src), 'input_sha256': hashlib.sha256(open(src, 'rb').read()).hexdigest(),
                  'input_n': m, 'input_edges': int((G == 1).sum() // 2), 'n': n,
                  'constructions_py_sha256': hashlib.sha256(open(K.__file__, 'rb').read()).hexdigest(),
                  'out_sha256': hashlib.sha256(open(out, 'rb').read()).hexdigest(),
                  'digits': '0 = paper colour 1 (new), 1 = paper colour 2 (edges of G), 2 = paper colour 3 (non-edges of G)'}))
