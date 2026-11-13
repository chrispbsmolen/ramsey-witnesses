"""Convert a column prefix of Rowley's arXiv:2203.13476 ancillary spreadsheet into a colour matrix.
The colour of edge {i,j} on vertices 0..N-1 is col[|i-j|-1] (a linear colouring, as Rowley defines
it in the spreadsheet's Introduction sheet).  Also reports whether it is cyclic (col[d]=col[N-d])."""
import json, sys
cols = json.load(open(sys.argv[1])); j, N, out = sys.argv[2], int(sys.argv[3]), sys.argv[4]
c = cols[j]['col'][:N - 1]
assert len(c) == N - 1, (len(c), N)
cyc = all(c[d - 1] == c[N - d - 1] for d in range(1, N))
with open(out, 'w') as f:
    for i in range(N):
        f.write(''.join('0' if i == k else str(c[abs(i - k) - 1]) for k in range(N)) + '\n')
with open(out.replace('.colormat', '.lengths'), 'w') as f:
    f.write('%d\n' % N + ' '.join(map(str, c)) + '\n')
print(json.dumps(dict(col=j, N=N, colours=sorted(set(c)), cyclic=cyc)))
