"""Check that a symmetric partition (full 5-line file) is equivalent, by multiplication with a unit mod 161
(Fredricksen-Sweet equivalence), to one of the enumerated depth-44 partitions (partitions/symmetric_depth44_all.txt,
one line per partition: colours of 1..80, colour 4 = the depth set, colours 0..3 in first-occurrence order)."""
import sys
N = 161
enum = set(tuple(map(int, l.split())) for l in open(sys.argv[1]))
rows = [[int(v) for v in l.split()] for l in open(sys.argv[2]) if l.strip() and not l.startswith('#')]
col = {v: c for c, r in enumerate(rows) for v in r}
hits = []
for m in range(1, N):
    if m % 7 == 0 or m % 23 == 0: continue
    cm = {(m * v) % N: col[v] for v in range(1, N)}         # element m*v gets the colour of v
    seq = [cm[i] for i in range(1, 81)]
    deep = set(seq[43:]) - set(seq[:43])                   # a set whose minimum is >= 44
    if len(set(seq[:43])) != 4 or not deep: continue
    d = [c for c in set(seq) if c not in seq[:43]][0]
    order = []; 
    for c in seq:
        if c != d and c not in order: order.append(c)
    relab = {c: k for k, c in enumerate(order)}; relab[d] = 4
    can = tuple(relab[c] for c in seq)
    hits.append((m, can in enum))
print(sys.argv[2], 'multipliers giving depth 44:', [m for m, _ in hits], 'found in enumeration:', [ok for _, ok in hits])
