#!/usr/bin/env python3
"""build_3337.py - R(3,3,3,7) from a (3,3,7) colouring by Robertson's construction (EJC 6 (1999) #R3, Part Two,
survey 6.2.h), using the unchanged function robertson() of build_G1_G2/scripts/constructions.py (staged copy).
T: (3,3,7;m) colormat with colours 0, 1 triangle-free and colour 2 K7-free (checked here exactly first);
G: K_6 in one colour (no K_7).  Output 3m + 6 vertices; with --cut N the first N vertices (an induced
sub-colouring keeps every clique bound).
usage: build_3337.py T.colormat OUT.colormat [--cut N]"""
import sys, os, json, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
sys.path.insert(0, '<ramsey>/phase2/build_G1_G2/scripts')
import verify_ramsey as V
import constructions as K
V.CLIQUE = os.path.join(HERE, '..', 'tools', 'clique')
src, out = sys.argv[1], sys.argv[2]
cut = int(sys.argv[sys.argv.index('--cut') + 1]) if '--cut' in sys.argv else None
T = V.load_colormat(src); m = len(T)
for c, k in ((0, 3), (1, 3), (2, 7)):
    assert not V.has_clique(T, c, k)[0], 'input lacks the (3,3,7) property in colour %d' % c
G = np.zeros((6, 6), dtype=np.int64); np.fill_diagonal(G, -1)
H = K.robertson(T, {0: 1, 1: 2, 2: 3}, G, {0: 1})
assert len(H) == 3 * m + 6
if cut: H = H[:cut, :cut]
with open(out, 'w') as f:
    f.write('\n'.join(''.join('0' if i == j else str(int(H[i][j])) for j in range(len(H))) for i in range(len(H))) + '\n')
print(json.dumps({'input': src, 'input_sha256': hashlib.sha256(open(src, 'rb').read()).hexdigest(), 'input_n': m,
                  'built_n_full': 3 * m + 6, 'cut': cut, 'out': out, 'n': len(H),
                  'constructions_py_sha256': hashlib.sha256(open(K.__file__, 'rb').read()).hexdigest(),
                  'sha256': hashlib.sha256(open(out, 'rb').read()).hexdigest(),
                  'colour_roles_in_output': 'colours 0,1,2 triangle-free, colour 3 K7-free (per robertson(): role j -> colour j-1, G colour -> 3)'}))
