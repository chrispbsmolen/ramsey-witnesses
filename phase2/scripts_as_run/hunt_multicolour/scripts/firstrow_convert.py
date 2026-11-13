"""Courties (github.com/JuloJC/multicolour-ramsey-numbers) 'first row' files: comment lines start with '#';
the remaining digits are the colours of lengths 1..N-1 (colours 0..r-1).  Writes .lengths (colours +1) and,
if N <= 3000, a .colormat."""
import sys
src, out = sys.argv[1], sys.argv[2]
digits = ''.join(l.strip() for l in open(src) if not l.startswith('#'))
assert digits.isdigit(), set(digits) - set('0123456789')
c = [int(x) + 1 for x in digits]; N = len(c) + 1
cyc = all(c[d - 1] == c[N - d - 1] for d in range(1, N))
open(out + '.lengths', 'w').write('%d\n%s\n' % (N, ' '.join(map(str, c))))
if N <= 3000:
    with open(out + '.colormat', 'w') as f:
        for i in range(N): f.write(''.join('0' if i == k else str(c[abs(i - k) - 1]) for k in range(N)) + '\n')
print(dict(src=src, N=N, colours=sorted(set(c)), cyclic=cyc))
