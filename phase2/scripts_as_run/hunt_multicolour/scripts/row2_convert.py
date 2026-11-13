"""Rowley, AJC 78(1) (2020) p.6 Table 1: distance sets of a cyclic (3,3,4,4;173)-graph (distances 1..86;
larger distances by symmetry d -> 173-d).  Parses pdftotext output, checks coverage, writes files."""
import re, sys
txt = open(sys.argv[1]).read()
blk = txt.split('Colour 1:')[1].split('Table 1: Distance Sets')[0]
parts = re.split(r'Colour (\d):', 'Colour 1:' + blk)
sets = {int(parts[i]): [int(x) for x in re.findall(r'\d+', re.sub(r'F\. ROWLEY.*', '', parts[i + 1]))] for i in range(1, len(parts), 2)}
N = 173; c = {}
for k, ds in sets.items():
    for d in ds:
        assert d not in c, d; c[d] = k
assert sorted(c) == list(range(1, 87)), sorted(set(range(1, 87)) - set(c))
for d in range(87, N): c[d] = c[N - d]
print({k: len(v) for k, v in sets.items()})
L = [c[d] for d in range(1, N)]; out = sys.argv[2]
open(out + '.lengths', 'w').write('%d\n%s\n' % (N, ' '.join(map(str, L))))
with open(out + '.colormat', 'w') as f:
    for i in range(N): f.write(''.join('0' if i == k else str(L[abs(i - k) - 1]) for k in range(N)) + '\n')
