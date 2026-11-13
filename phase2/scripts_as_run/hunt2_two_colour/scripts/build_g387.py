"""Build G387 of XSR2 Thm 5 (p.7): one colour class of the XuR1 colouring M_127' (3p+6 = 387 vertices),
using a verbatim copy of build_G1_G2/scripts/constructions.py (xur1, sha256 4a25115b...).
Writes witnesses/G387_colour{c}.g6 for c = 0,1,2 and checks K5 in that colour (fast); the K17 half
of the complement is checked separately.  Usage: python3 build_g387.py"""
import os, sys, numpy as np, networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools')); sys.path.insert(0, HERE)
import verify_ramsey as V
import g1_constructions as K
C, info = K.xur1(127)
assert len(C) == 387
for c in range(3):
    A = (C == c).astype(int); np.fill_diagonal(A, 0)
    G = nx.from_numpy_array(A)
    path = os.path.join(HERE, '..', 'witnesses', 'G387_colour%d.g6' % c)
    open(path, 'wb').write(nx.to_graph6_bytes(G, header=False))
    D = V.from_adjacency(A)
    k5 = V.has_clique(D, 1, 5)[0]; k4 = V.has_clique(D, 1, 4)[0]
    print('colour', c, 'edges', G.number_of_edges(), 'K4', k4, 'K5', k5, flush=True)
