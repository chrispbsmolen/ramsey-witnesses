"""Rowley arXiv:2107.03560 ancillary xls, sheet 'S(7) >= 1696': columns D (integer) and E (subset).
Writes a .lengths file (N = 1697; colour of edge-length d = subset of d) and a colour matrix."""
import xlrd, sys
b = xlrd.open_workbook(sys.argv[1]); s = b.sheet_by_name('S(7) >= 1696')
part = {}
for r in range(s.nrows):
    x, y = s.cell_value(r, 3), s.cell_value(r, 4)
    if isinstance(x, float) and isinstance(y, float): part[int(x)] = int(y)
n = max(part); assert sorted(part) == list(range(1, n + 1)), 'gaps'
N = n + 1; c = [part[d] for d in range(1, N)]
# independent sum-free check of the partition itself
S = {}
for x, k in part.items(): S.setdefault(k, set()).add(x)
bad = [(a, b) for k, X in S.items() for a in X for b in X if a <= b and a + b in X]
print('n =', n, 'subsets', len(S), 'sum-free violations', len(bad), 'symmetric x<->%d-x:' % N, all(part[x] == part[N - x] for x in range(1, N)))
out = sys.argv[2]
open(out + '.lengths', 'w').write('%d\n%s\n' % (N, ' '.join(map(str, c))))
with open(out + '.colormat', 'w') as f:
    for i in range(N): f.write(''.join('0' if i == k else str(c[abs(i - k) - 1]) for k in range(N)) + '\n')
