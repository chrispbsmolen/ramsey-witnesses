"""Extract sum-free partitions (as colour words over [1,N]) from downloaded sources into one file.
Output line format: source_id<TAB>N<TAB>modulus_or_0<TAB>space-separated colours of 1..N
(modulus M>0 means the source states the partition is sum-free mod M, i.e. on Z_M \\ {0}, N = M-1).
Run: python3 -I extract_words.py <out_file>
Paths are fixed below (all under the ramsey-p2 working folder)."""
import sys, os
import xlrd

W = '<cloud>/ramsey-p2'
out = []


def add(src, word, mod=0):
    out.append((src, len(word), mod, word))


# 1. Chen-Zhu-Long arXiv:2610.31362 / github jeffchen006/Schur-Number-6
R = W + '/hunt3_multicolour/downloads/gh_jeffchen006_Schur-Number-6'
toks = open(R + '/certificate.col').read().split()
assert toks[:2] == ['537', '6']
add('CZL_certificate.col', [int(t) for t in toks[2:]], 538)
for line in open(R + '/solutions537.txt'):
    if line.startswith('#') or not line.strip():
        continue
    ident, digits = line.split()[0], ''.join(line.split()[1:])
    add('CZL_solutions537:' + ident, [int(c) for c in digits], 538)
s8 = open(R + '/data/S8_n5372.txt').read().strip()
add('CZL_S8_n5372', [int(c) for c in s8])

# 2. Rowley arXiv:2107.03560 ancillary xls
x = W + '/hunt_multicolour/downloads/arxiv_2107.03560/x/anc/Specimens_S_7____TFTs-4,5,6.xls'
b = xlrd.open_workbook(x)
for name, ci, cs in [('S(7) >= 1696', 3, 4), ('S(7) >= 1664', 4, 5)]:
    s = b.sheet_by_name(name)
    d = {}
    for r in range(s.nrows):
        a, c = s.cell_value(r, ci), s.cell_value(r, cs)
        if isinstance(a, float) and isinstance(c, float):
            d[int(a)] = int(c)
    n = max(d)
    assert sorted(d) == list(range(1, n + 1)), name
    add('Rowley2107_' + name.replace(' ', ''), [d[i] for i in range(1, n + 1)])

# 3. round-2 partitions of [1,160] (Exoo 1994, Heule 2018), for control
for fn in ['exoo94_full.txt', 'heule2018_fig1_full.txt']:
    p = W + '/hunt2_multicolour/partitions/' + fn
    parts = [[int(t) for t in l.replace(',', ' ').split()] for l in open(p) if l.strip() and not l.startswith('#')]
    col = {}
    for k, pp in enumerate(parts):
        for v in pp:
            col[v] = k
    n = max(col)
    add('round2_' + fn, [col[i] for i in range(1, n + 1)])

with open(sys.argv[1], 'w') as f:
    for src, n, mod, w in out:
        f.write('%s\t%d\t%d\t%s\n' % (src, n, mod, ' '.join(map(str, w))))
print(len(out), 'words written')
