"""R(5,17) >= 388 (XSR2 Thm 5 p.7: G387 = one colour of the XuR1 tripling with p = 127).
Builds M'_127 with round-1 code (build_G1_G2/scripts/constructions.py xur1, used there for R(7,7,7)), for each
recolouring r of the special colour (XuR1 property C allows any) and each colour c: K5 in colour c? and K17 in the
union of the other two colours (= independent 17-set of the colour-c graph)? Any K17 found is re-checked edge by edge.
Also the same on M_127 (384 vertices, W removed).  Writes built/XuR1_Mprime127_n387.colormat (r = 0) and logs/r5_17.jsonl."""
import sys, os, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '<cloud>/ramsey-p2/build_G1_G2/scripts')
import numpy as np
import lib2 as L
import constructions as K
import verify_ramsey as V
for r in range(3):
    C, info = K.xur1(127, c_recolour=r)
    if r == 0:
        path = os.path.join(L.BUILT, 'XuR1_Mprime127_n387.colormat')
        D = C.copy(); np.fill_diagonal(D, 0)
        open(path, 'w').write('\n'.join(''.join(map(str, row)) for row in D.tolist()) + '\n')
        L.log('r5_17.jsonl', dict(file='built/XuR1_Mprime127_n387.colormat', sha256=L.sha256_file(path), n=len(C), p=127, beta=info['beta'],
                                  construction='XuR1 EJC 16 (2009) #N1 pp.2-4 M\'_p, special colour recoloured to 0, via build_G1_G2 constructions.xur1 (sha256 %s)' % L.sha256_file('<cloud>/ramsey-p2/build_G1_G2/scripts/constructions.py')))
    for c in range(3):
        for name, keep in (('Mprime_387', list(range(len(C)))), ('M_384_noW', list(range(384)))):
            S = C[np.ix_(keep, keep)]
            A = np.where(S == c, 1, 0); np.fill_diagonal(A, -1)
            k5 = V.has_clique(A, 1, 5)[1]
            B = np.where(S == c, 0, 1); np.fill_diagonal(B, -1)
            try:
                out = V.has_clique(B, 1, 17, timeout=120)[1]
            except subprocess.TimeoutExpired:
                out = 'TIMEOUT 120 s'
            rec = dict(recolour=r, colour=c, graph=name, n=len(keep), K5_in_colour=k5[:40], K17_in_other_two=out[:120])
            if out.startswith('FOUND'):
                vs = [keep[int(x)] for x in out.split()[2:]]
                rec['K17_set'] = vs
                rec['K17_edges_rechecked'] = all(C[a][b] != c for a in vs for b in vs if a != b) and len(set(vs)) >= 17
            L.log('r5_17.jsonl', rec)
