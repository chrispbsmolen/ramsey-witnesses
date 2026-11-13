"""Build the linear (length-vector) multicolour cells of build_round2.

Usage: python3 build_linear.py [CELL ...]   (default: all)
Writes built/<name>.lengths(.gz), appends to logs/builds_linear.jsonl.
"""
import sys, os, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lib2 as L
import constructions2 as K

FIG1 = {  # Rowley AJC 81(2) p.251 Figure 1 (colour of edge-length 1..m-1; template colour 2)
    '6,3;12': '11112122212',
    '5,3;10': '111212212',
}


def vec(s): return [None] + [int(x) for x in s]


def jan2021(param):
    """Template (k,3) columns of sheet Jan_2021_trg(k,3) (Rowley arXiv:2203.13476 ancillary)."""
    R = [r for r in csv.reader(open(L.pin('rowley_jan2021'))) if r]
    j = R[1].index(param)
    order = int(R[2][j]); phi = int(R[3][j])
    rows = [r for r in R if len(r) > 1 and r[1].strip().isdigit()]
    col = [r[j] for r in rows if j < len(r) and r[j].strip()]
    assert len(col) == order - 1
    return order, phi, vec(''.join(col))


def sheet_col(j, m):
    """first m-1 lengths of column j of sheet Paper_Sep_2022 (round-1 extraction cols.json)."""
    d = json.load(open(L.pin('rowley_cols')))[str(j)]
    col = d['col']; assert len(col) >= m - 1
    return d['info'], [None] + col[:m - 1]


def paley_from_repo(name, p):
    """Q_p as length vector, read from the repo g6 file and checked equal to the QR definition."""
    A = L.g6_adj(L.pin(name))
    n, c = L.circulant_lengths_from_adj(A, 1, 2)
    n2, c2 = L.paley_lengths(p, 1, 2)
    assert n == p and c == c2, 'repo Paley file differs from the QR definition'
    return n, c


def circ_doubled(p):
    """Circulant on Z_{2p}: d -> edge iff (d even and d mod p a nonzero square) or (d odd and d mod p a
    non-square, d mod p != 0).  Under z -> (z mod p, z mod 2) (CRT, p odd) this is the subgraph of the
    Shearer-Mathon doubling of Q_p induced by H u H' (x ~ y iff x-y in QR, x ~ y' iff x-y in NQR,
    x !~ x'; XXER p.12-13), i.e. a linear isomorphic image of the (alpha+2, alpha+2; 2p) graph that
    Rowley AJC 78(1) Sec.6 (p.7) uses as prototype.  Checked against that definition in check_circ_doubled."""
    Q = {x * x % p for x in range(1, p)}
    c = [None]
    for d in range(1, 2 * p):
        r = d % p
        e = (d % 2 == 0 and r in Q) or (d % 2 == 1 and r != 0 and r not in Q)
        c.append(1 if e else 2)
    return 2 * p, c


def check_circ_doubled(p, c):
    Q = {x * x % p for x in range(1, p)}
    n = 2 * p
    for z1 in range(n):
        for z2 in range(z1 + 1, n):
            x, a = z1 % p, z1 % 2; y, b = z2 % p, z2 % 2
            if a == b: e = ((x - y) % p) in Q
            else: e = x != y and ((x - y) % p) not in Q
            assert e == (c[z2 - z1] == 1)
    return True


def cubic():
    n, c = L.colormat_lengths(L.pin('cubic3_127'))
    return n, [None] + [x + 1 for x in c[1:]]      # colours 0..2 -> 1..3


def r555():
    return L.lengths_of('r555_453')


def compose32(cU, m, cV, n):
    N, cW, phi, q = K.rowley32(cU, m, cV, n)
    cW, lut = K.relabel(cW)
    return N, cW, phi, q


def compose31(cU, m, cV, n):
    cV2 = [None] + [100 + x for x in cV[1:]]
    N, cW = K.rowley31(cU, m, cV2, n)
    cW, lut = K.relabel(cW)
    return N, cW


def build(cell):
    info = dict(cell=cell)
    if cell == '4,4,4,4':
        n, c = cubic()
        N, cW = K.giraud(c, n, 4)
        info.update(survey_lower=634, construction='XXER EJC 11 (2004) #R35 Theorem 1 [Giraud] p.5 and Corollary 1 p.5, k_{r+1}=4',
                    inputs=[L.input_record('cubic3_127')], formula='(2k-3)n-k+2 = 5*127-2 = 633')
    elif cell == '6,6,6':
        cU = vec(FIG1['6,3;12']); n, cV = paley_from_repo('paley101', 101)
        N, cW, phi, q = compose32(cU, 12, cV, n)
        info.update(survey_lower=1106, construction='Rowley AJC 81(2) (2021) Theorem 3.2 pp.248-250 with U=(6,3;12) of Figure 1 p.251 and V=Kalbfleisch (6,6;101)=Paley Q_101 (Sec.4 p.250)',
                    inputs=[L.input_record('paley101'), dict(name='U(6,3;12)', source='printed, Rowley AJC 81(2) Fig.1 p.251: ' + FIG1['6,3;12'])],
                    phi=phi, formula='(m-1)(n-1)+1+phi = 11*100+1+4 = 1105', template=K.check_template(cU, 12))
    elif cell == '5,5,5,5':
        cU = vec(FIG1['5,3;10']); n, cV = r555()
        N, cW, phi, q = compose32(cU, 10, cV, n)
        info.update(survey_lower=4073, construction='Rowley AJC 81(2) (2021) Theorem 3.2 pp.248-250 with U=(5,3;10) of Figure 1 p.251 and V=(5,5,5;453) (Exoo; Sec.4 p.250)',
                    inputs=[L.input_record('r555_453'), dict(name='U(5,3;10)', source='printed, Rowley AJC 81(2) Fig.1 p.251: ' + FIG1['5,3;10'])],
                    phi=phi, formula='9*452+1+3 = 4072', template=K.check_template(cU, 10))
    elif cell == '4,4,4,4,4':
        n, cU = cubic(); p, cV = L.paley_lengths(17)
        N, cW = compose31(cU, n, cV, p)
        info.update(survey_lower=4176, construction='Rowley AJC 68(3) (2017) Theorem 3.1, eqs (3.1)-(3.2) p.387, U=(4,4,4;127) cubic residues, V=Paley Q_17 (Cor.3.2/Table 1)',
                    inputs=[L.input_record('cubic3_127'), dict(name='Q_17', source='Paley graph Q_17 from its definition (x~y iff x-y a nonzero square mod 17)')],
                    formula='2*127*17-127-17+1 = 4175')
    elif cell == '4,4,4,4,4,4':
        n, cU = cubic()
        N, cW = compose31(cU, n, cU, n)
        info.update(survey_lower=32006, construction='Rowley AJC 68(3) (2017) Theorem 3.1 p.387 with U=V=(4,4,4;127) (AJC 81(2) Table 1 row E\'*E\')',
                    inputs=[L.input_record('cubic3_127')], formula='2*127*127-127-127+1 = 32005')
    elif cell == '4,4,4,4,4,4,4':
        n, c = cubic(); m4, c4 = K.giraud(c, n, 4)
        N, cW = compose31(c4, m4, c, n)
        info.update(survey_lower=160024, construction='Rowley AJC 68(3) (2017) Theorem 3.1 p.387 with U=(4,4,4,4;633) (XXER Thm 1 on the cubic (4,4,4;127), built here) and V=(4,4,4;127) (AJC 81(2) Table 1 row E\'*F)',
                    inputs=[L.input_record('cubic3_127')], formula='2*633*127-633-127+1 = 160023')
    elif cell in ('6,6,6,6', '7,7,7,7', '8,8,8,8', '9,9,9,9', '5,5,5,5,5,5'):
        spec = {'6,6,6,6': (15, 235, 100, 23502), '7,7,7,7': (19, 472, 201, 94874), '8,8,8,8': (21, 650, 280, 182002),
                '9,9,9,9': (25, 1282, 561, 719204), '5,5,5,5,5,5': (27, 977, 452, 441606)}[cell]
        j, m, phi_tab, sl = spec
        sinfo, cU = sheet_col(j, m)
        if cell == '6,6,6,6': n, cV = paley_from_repo('paley101', 101); vin = [L.input_record('paley101')]; vdesc = 'Paley Q_101'
        elif cell == '8,8,8,8': n, cV = paley_from_repo('paley281', 281); vin = [L.input_record('paley281')]; vdesc = 'Paley Q_281'
        elif cell == '7,7,7,7':
            paley_from_repo('paley101', 101); n, cV = circ_doubled(101); check_circ_doubled(101, cV)
            vin = [L.input_record('paley101')]; vdesc = 'cyclic (7,7;202) = H u H\' of the Shearer-Mathon doubling of Q_101 (circulant on Z_202, see circ_doubled)'
        elif cell == '9,9,9,9':
            paley_from_repo('paley281', 281); n, cV = circ_doubled(281); check_circ_doubled(281, cV)
            vin = [L.input_record('paley281')]; vdesc = 'cyclic (9,9;562) = H u H\' of the Shearer-Mathon doubling of Q_281 (circulant on Z_562)'
        else: n, cV = r555(); vin = [L.input_record('r555_453')]; vdesc = '(5,5,5;453)'
        N, cW, phi, q = compose32(cU, m, cV, n)
        assert phi == phi_tab, (phi, phi_tab)
        info.update(survey_lower=sl, construction='Rowley AJC 81(2) (2021) Theorem 3.2 pp.248-250; template %s;%d (phi=%d) from Rowley arXiv:2203.13476v3 Table 1 and ancillary sheet Paper_Sep_2022 column %d; V = %s' % (
            sinfo['PARAMETERS'], m, phi, j, vdesc), inputs=[L.input_record('rowley_cols'), L.input_record('rowley_sheet')] + vin,
            phi=phi, formula='(m-1)(n-1)+1+phi = %d*%d+1+%d = %d' % (m - 1, n - 1, phi, (m - 1) * (n - 1) + 1 + phi),
            template=K.check_template(cU, m), sheet_info=sinfo)
    elif cell == '6,6,6,6,6':
        _, cU6 = sheet_col(15, 235); n, cV = paley_from_repo('paley101', 101)
        N1, c1, phi1, _ = compose32(cU6, 235, cV, n)
        cU = vec(FIG1['6,3;12'])
        N, cW, phi, q = compose32(cU, 12, c1, N1)
        info.update(survey_lower=258506, construction='Rowley AJC 81(2) Theorem 3.2 applied twice: (6,6,3;235) [arXiv:2203.13476 sheet col 15] & Q_101 -> (6^4;23501), then (6,3;12) [AJC 81(2) Fig.1] & (6^4;23501) (route of hunt2_multicolour; Row5 Table 2 order 258505)',
                    inputs=[L.input_record('rowley_cols'), L.input_record('paley101')], phi=phi,
                    formula='11*23500+1+4 = 258505', intermediate_N=N1)
    elif cell == '6,6,6,6,6,6':
        _, cU6 = sheet_col(15, 235); n, cV = paley_from_repo('paley101', 101)
        N1, c1, phi1, _ = compose32(cU6, 235, cV, n)
        N, cW, phi, q = compose32(cU6, 235, c1, N1)
        info.update(survey_lower=4515702, construction='Rowley AJC 81(2) Theorem 3.2 applied twice with the (6,6,3;235) template [arXiv:2203.13476 sheet col 15]: (6,6,3;235) & ((6,6,3;235) & Q_101) = order 5499101 as in Rowley arXiv:2203.13476 Table 2 (r=6,k=6). The survey order 4515701 is AJC 81(2) Table 1 row H&J with H(6,6,3;213), whose template is not published; the 5499101 colouring is larger, its first 4515701 vertices give a linear colouring of the survey order.',
                    inputs=[L.input_record('rowley_cols'), L.input_record('paley101')], phi=phi,
                    formula='234*23500+1+100 = 5499101 (>= 4515701)', intermediate_N=N1)
    elif cell == '10,10,10':
        m, phi_s, cU = jan2021('10,3'); n, cV = paley_from_repo('paley797', 797)
        N, cW, phi, q = compose32(cU, m, cV, n)
        assert phi == phi_s
        info.update(survey_lower=23094, construction='Rowley AJC 81(2) Theorem 3.2 with U=(10,3;30) from sheet Jan_2021_trg(k,3) of Rowley arXiv:2203.13476 ancillary (phi=8) and V=Paley Q_797 (route of hunt2_multicolour; Row5 Table 2 order 23093)',
                    inputs=[L.input_record('rowley_jan2021'), L.input_record('paley797')], phi=phi,
                    formula='29*796+1+8 = 23093', template=K.check_template(cU, m))
    elif cell in ('3,3,3,3,3,3,3,3', '3,3,3,3,3,3,3,3,3'):
        T = {33: {1: [1, 6, 9, 13, 16, 20, 24, 27, 31], 2: [2, 5, 14, 15, 25, 26], 3: [3, 4, 10, 11, 12, 28, 29, 30],
                  4: [7, 8, 17, 18, 19, 21, 22, 23, 32, 33]},
             111: {1: [1, 5, 8, 12, 14, 21, 23, 30, 32, 36, 39, 43, 45, 52, 103, 106, 110],
                   2: [2, 6, 7, 10, 15, 18, 26, 29, 34, 37, 38, 42, 46, 51, 54, 101, 104, 109],
                   3: [3, 4, 9, 11, 17, 19, 25, 27, 33, 35, 40, 41, 47, 48, 55, 100, 107, 108],
                   4: [13, 16, 20, 22, 24, 28, 31, 58, 61, 67, 88, 94, 97],
                   5: [44, 50, 53, 56, 57, 59, 60, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85,
                       86, 87, 89, 90, 91, 92, 93, 95, 96, 98, 99, 102, 105, 111]}}
        q = 33 if cell.count('3') == 8 else 111
        f = [None] * (q + 1)
        for col, xs in T[q].items():
            for x in xs: assert f[x] is None; f[x] = col
        if q == 111:
            # The printed Table 6 omits the element 49 (checked on the rendered PDF page 18).  Exactly two
            # colours keep Def. 2.1 (1 and 4; tested in logs/template111_missing49.json); colour 1 is used.
            assert f[49] is None; f[49] = 1
            info['template_note'] = 'printed Table 6 omits 49; colours 1 and 4 both satisfy Def. 2.1, colour 1 used here'
        assert all(x is not None for x in f[1:]), 'template is not a partition'
        assert K.check_s_template(f, q), 'S-template condition fails'
        n5, g = L.lengths_of('exoo_s5')       # g[1..160] = Exoo's sum-free 5-partition
        N, h, m, s = K.schur_template(f, q, g, n5 - 1)
        cW, lut = K.relabel(h)
        sl = 5288 if q == 33 else 17805
        info.update(survey_lower=sl, construction='Ageron et al. arXiv:2112.03175v2 Theorem 2.3 pp.3-5 with the S-template of width %d (Table %d p.18, Appendix A) and Exoo\'s sum-free 5-partition of [1,160] (EJC 1 #R8 p.2); Schur partition of [1,%d] -> linear colouring of K_%d' % (q, 5 if q == 33 else 6, N - 1, N),
                    inputs=[L.input_record('exoo_s5'), dict(name='S-template width %d' % q, source='printed, arXiv:2112.03175v2 Table %d (PDF sha256 0bef5716f171992d6b125cfea15551b4e065eecfb243cd7b3e73884cbe5ca703)' % (5 if q == 33 else 6))],
                    m_special=m, formula='S >= %d*160 + %d - 1 = %d, vertices = %d' % (q, m, q * 160 + m - 1, q * 160 + m))
    else:
        raise KeyError(cell)
    info['N'] = N
    info['N_ok'] = (N == info['survey_lower'] - 1) or cell == '6,6,6,6,6,6'
    info['colours'] = L.colours(cW)
    info['cyclic'] = L.is_cyclic(N, cW)
    name = 'R%s_n%d.lengths' % ('_'.join(cell.split(',')), N)
    if len(set(cell.split(','))) == 1 and cell.count(',') >= 2:
        k = cell.split(',')[0]; name = 'R%s^%d_n%d.lengths' % (k, cell.count(',') + 1, N)
    if N > 200000: name += '.gz'
    sha, sha_raw = L.write_lengths(N, cW, os.path.join(L.BUILT, name))
    info.update(file='built/' + name, sha256=sha, sha256_uncompressed=sha_raw)
    if N <= 6000:
        info['degrees_v0'] = {str(col): L.degree(N, cW, col) for col in info['colours']}
    L.log('builds_linear.jsonl', info)
    return N, cW


if __name__ == '__main__':
    cells = sys.argv[1:] or ['4,4,4,4', '6,6,6', '5,5,5,5', '4,4,4,4,4', '4,4,4,4,4,4', '4,4,4,4,4,4,4', '6,6,6,6', '7,7,7,7', '8,8,8,8',
                             '9,9,9,9', '5,5,5,5,5,5', '6,6,6,6,6', '6,6,6,6,6,6', '10,10,10', '3,3,3,3,3,3,3,3', '3,3,3,3,3,3,3,3,3']
    for c in cells: build(c)
