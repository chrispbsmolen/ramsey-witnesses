"""Exoo EJC 1 (1994) #R8, p.2: symmetric sum-free partition of [1,160] into 5 sets; only 1..80 printed,
i and 161-i in the same set.  Rebuilds it from the pdftotext output, checks it, writes K_161 colouring."""
import re, sys
txt = open(sys.argv[1]).read()
sets = {int(k): [int(x) for x in v.split()] for k, v in re.findall(r'^Set (\d): ([\d ]+)$', txt, re.M)}
n = 160; part = {}
for k, xs in sets.items():
    for x in xs:
        assert x not in part; part[x] = k; part[n + 1 - x] = k
assert sorted(part) == list(range(1, n + 1)), [x for x in range(1, n + 1) if x not in part]
S = {}
for x, k in part.items(): S.setdefault(k, set()).add(x)
bad = [(a, b) for X in S.values() for a in X for b in X if a <= b and a + b in X]
print('sets', {k: len(v) for k, v in sets.items()}, 'covers [1,160]', 'sum-free violations', len(bad))
N = n + 1; c = [part[d] for d in range(1, N)]; out = sys.argv[2]
open(out + '.lengths', 'w').write('%d\n%s\n' % (N, ' '.join(map(str, c))))
with open(out + '.colormat', 'w') as f:
    for i in range(N): f.write(''.join('0' if i == k else str(c[abs(i - k) - 1]) for k in range(N)) + '\n')
