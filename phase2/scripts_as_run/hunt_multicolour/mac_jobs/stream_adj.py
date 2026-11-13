"""Stream the adjacency matrix of one colour class of a linear colouring ('.lengths' file) in the
input format of repo/clique.c ('n' then n lines of n '0'/'1').  Memory O(N).
Usage: python3 -I stream_adj.py FILE COL | ../../repo/clique K --sym      (--sym only if cyclic)"""
import sys, numpy as np
t = open(sys.argv[1]).read().split(); N = int(t[0]); col = int(sys.argv[2])
c = np.array([0] + [int(x) for x in t[1:]], dtype=np.int64)
assert len(c) == N
b = (c == col).astype(np.uint8); b[0] = 0
out = sys.stdout.buffer; out.write(b'%d\n' % N)
for i in range(N):
    row = np.concatenate((b[i:0:-1], b[0:N - i])) if i else b
    out.write((row + 48).tobytes()); out.write(b'\n')
