"""Build the G1 colourings.  Usage: python3 build_G1.py CELL [CELL ...]
CELL in: 3333, 3337demo, 348, 357, 33310, 33311, 3444, 777 (777 needs a long run, see REPORT.md).
Writes built/<name> and appends a JSON line per build to logs/builds.jsonl."""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, constructions as K
V = lib.V
B = os.path.join(lib.OUT, 'built')


def log(rec):
    rec['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    open(os.path.join(lib.OUT, 'logs', 'builds.jsonl'), 'a').write(json.dumps(rec) + '\n')
    print(json.dumps(rec), flush=True)


def save(C, name, cell, ks, inputs, extra=None):
    r = len(ks); lib.check_matrix(C, r)
    path = os.path.join(B, name)
    sha = lib.write_colormat(C, path) if r > 2 else lib.write_g6(C, path)
    rec = dict(cell=cell, file='built/' + name, n=len(C), ks=ks, sha256=sha,
               inputs={k: lib.INPUTS[k][1] for k in inputs})
    if extra: rec.update(extra)
    log(rec)
    return path


def roles_by_clique(C, sizes):
    """Assign the colours of C to the requested forbidden sizes (list, one per colour), exactly."""
    import itertools
    cols = sorted(set(C[C >= 0].tolist()))
    for perm in itertools.permutations(cols):
        if all(not V.has_clique(C, c, s)[0] for c, s in zip(perm, sizes)): return list(perm)
    raise RuntimeError('input colouring does not have the claimed property')


def robertson_cell(Tname, Tsizes, G, g_roles, n_expected, name, cell, ks, Tcut=None):
    T = lib.load_input(Tname)
    if Tcut: T = lib.induced(T, Tcut)
    perm = roles_by_clique(T, Tsizes)            # perm[i] = colour of T with role i+1
    roles = {c: i + 1 for i, c in enumerate(perm)}
    C = K.robertson(T, roles, G, g_roles)
    assert len(C) == n_expected, (len(C), n_expected)
    return save(C, name, cell, ks, [Tname], dict(construction='Robertson 1999 Part Two (Chung 1973)',
                                                   T_roles={int(c): r for c, r in roles.items()}))


def xxer_cell(Gname, a_size, other_sizes, n_expected, name, cell, ks, cut=None, merge_with=None):
    G = lib.load_input(Gname)
    if cut: G = lib.induced(G, cut)
    perm = roles_by_clique(G, [a_size] + other_sizes)
    a = perm[0]
    F = K.xxer_quadruple(G, a)
    extra = dict(construction='XXER Theorem 7 / Corollary 3', a_colour=int(a), new_colour=int(G.max()) + 1,
                 input_order=len(G))
    if merge_with is not None:                   # Corollary 5: merge new colour 1 with the colour of role merge_with
        c2 = perm[merge_with]
        F = K.merge(F, int(G.max()) + 1, c2)
        extra.update(construction='XXER Corollary 5 (merge of Corollary 3 colouring)', merged=[int(G.max()) + 1, int(c2)])
    assert len(F) == n_expected, (len(F), n_expected)
    return save(F, name, cell, ks, [Gname], extra)


def cell_3444():
    U = lib.load_input('cubic3_127')
    cU = K.length_colouring(U)               # colours 0,1,2
    cV = [None, 3]                           # V = K_2, one new colour 3 (forbidden K_3)
    C, cW = K.rowley(cU, 127, cV, 2)
    assert len(C) == 380
    assert V.is_circulant(C), 'W should be cyclic (Rowley Cor. 3.2)'
    return save(C, 'R3_4_4_4_n380.txt', '3,4,4,4', [4, 4, 4, 3], ['cubic3_127'],
                dict(construction='Rowley 2017 Thm 3.1 / Giraud (U = cubic 127, V = K_2)'))


def main():
    os.makedirs(B, exist_ok=True)
    for cell in sys.argv[1:]:
        if cell == '3333':
            G = np.array([[-1, 0], [0, -1]])          # K_2 in one colour (no K_3): R(3) - 1 = 2 vertices
            robertson_cell('clebsch16', [3, 3, 3], G, {0: 1}, 50, 'R3_3_3_3_n50.txt', '3,3,3,3', [3, 3, 3, 3])
        elif cell == '3337demo':
            G = np.full((6, 6), 0); np.fill_diagonal(G, -1)   # K_6 in one colour (no K_7)
            robertson_cell('g337.78', [3, 3, 7], G, {0: 1}, 240, 'R3_3_3_7_n240_demo.txt', '3,3,3,7', [3, 3, 3, 7])
        elif cell == '348':
            xxer_cell('r4.7.48', 7, [4], 192, 'R3_4_8_n192.txt', '3,4,8', [3, 4, 8])
        elif cell == '357':
            xxer_cell('g336.60', 6, [3, 3], 240, 'R3_5_7_n240.txt', '3,5,7', [5, 7, 3], merge_with=1)
        elif cell == '33310':
            xxer_cell('lachy_r339', 9, [3, 3], 512, 'R3_3_3_10_n512.txt', '3,3,3,10', [3, 3, 3, 10], cut=128)
        elif cell == '33311':
            xxer_cell('g3310.149', 10, [3, 3], 596, 'R3_3_3_11_n596.txt', '3,3,3,11', [3, 3, 3, 11])
        elif cell == '3444':
            cell_3444()
        else:
            raise SystemExit('unknown cell ' + cell)


if __name__ == '__main__':
    main()
