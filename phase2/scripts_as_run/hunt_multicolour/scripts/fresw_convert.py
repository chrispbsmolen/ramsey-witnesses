"""Fredricksen-Sweet EJC 7 (2000) #R32, p.6: 'Partition of 536 into 6 symmetric sumfree sets'
(only the smaller of each symmetric pair x, 537-x is printed).  Reads the pdftotext -layout output,
rebuilds the partition of [1,536], checks it, and writes a .lengths/.colormat for K_537."""
import re, sys
txt = open(sys.argv[1]).read()
blk = txt.split('Partition of 536 into 6 symmetric sumfree sets:')[1].split('(D(P ) = 161)')[0]
sets = {}
for m in re.finditer(r'Set (\d):(.*?)(?=Set \d:|\Z)', blk, re.S):
    sets[int(m.group(1))] = [int(x) for x in m.group(2).split()]
n = 536; part = {}
for k, xs in sets.items():
    for x in xs:
        assert x not in part, ('listed twice', x); part[x] = k
listed = dict(part)
for x, k in listed.items():
    y = n + 1 - x
    if y not in listed: part[y] = k
missing = [x for x in range(1, n + 1) if x not in part]
print('sets', {k: len(v) for k, v in sets.items()}, 'listed', len(listed), 'total', len(part), 'missing', missing)
asym = [x for x in range(1, n + 1) if part.get(x) != part.get(n + 1 - x)]
print('asymmetric pairs (x with part[x] != part[537-x]):', asym)
S = {}
for x, k in part.items(): S.setdefault(k, set()).add(x)
bad = [(a, b, k) for k, X in S.items() for a in X for b in X if a <= b and a + b in X]
print('sum-free violations', bad[:10], len(bad))
N = n + 1; c = [part[d] for d in range(1, N)]
out = sys.argv[2]
open(out + '.lengths', 'w').write('%d\n%s\n' % (N, ' '.join(map(str, c))))
with open(out + '.colormat', 'w') as f:
    for i in range(N): f.write(''.join('0' if i == k else str(c[abs(i - k) - 1]) for k in range(N)) + '\n')
