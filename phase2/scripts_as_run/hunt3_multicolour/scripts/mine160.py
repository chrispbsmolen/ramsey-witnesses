"""Mine 5-colour sum-free partitions of [1,160] out of larger sum-free partitions.
If c is sum-free on [1,N] then i -> c(i*d), i=1..160, is sum-free for any d with 160*d <= N
(x+y=z implies dx+dy=dz).  If c is sum-free on Z_M\\{0} (checked here, not taken on trust), then
i -> c(i*d mod M) is sum-free for any d with M not dividing i*d for i<=160.
Keeps restrictions that use exactly 5 colours, canonicalised (colours renamed by first use), deduplicated.
Also writes the 6-colour restrictions (canonical, dedup) to a second file for an optional triple-merge test.
Usage: python3 -I mine160.py source_words.tsv out5.tsv out6.tsv"""
import sys

def sumfree_int(w):
    n = len(w)
    for x in range(1, n + 1):
        cx = w[x - 1]
        for y in range(x, n + 1 - x):
            if w[y - 1] == cx and w[x + y - 1] == cx:
                return False
    return True

def sumfree_mod(w, M):
    # w[k-1] = colour of k in Z_M, k=1..M-1
    for x in range(1, M):
        cx = w[x - 1]
        for y in range(x, M):
            z = (x + y) % M
            if z and w[y - 1] == cx and w[z - 1] == cx:
                return False
    return True

def canon(sub):
    m = {}
    return tuple(m.setdefault(c, len(m)) for c in sub)

found5, found6 = {}, {}
log = []
for line in open(sys.argv[1]):
    src, n, M, ws = line.rstrip('\n').split('\t')
    n, M = int(n), int(M)
    w = [int(t) for t in ws.split()]
    ok_int = sumfree_int(w)
    ok_mod = (M > 0 and len(w) == M - 1 and sumfree_mod(w, M))
    k = len(set(w))
    if not ok_int:
        log.append('%s N=%d colours=%d NOT sum-free on integers: skipped' % (src, n, k)); continue
    ds = []
    if ok_mod:
        ds = [('mod', d) for d in range(1, M) if all((i * d) % M for i in range(1, 161))]
    else:
        ds = [('int', d) for d in range(1, n // 160 + 1)]
    c5 = c6 = 0
    for kind, d in ds:
        if kind == 'mod':
            sub = [w[(i * d) % M - 1] for i in range(1, 161)]
        else:
            sub = [w[i * d - 1] for i in range(1, 161)]
        nc = len(set(sub))
        cs = canon(sub)
        if nc == 5:
            c5 += 1
            found5.setdefault(cs, []).append('%s:%s%d' % (src, kind, d))
        elif nc == 6:
            c6 += 1
            found6.setdefault(cs, []).append('%s:%s%d' % (src, kind, d))
    log.append('%s N=%d colours=%d sumfree_int=%s sumfree_mod%d=%s dilations=%d five=%d six=%d'
               % (src, n, k, ok_int, M, ok_mod, len(ds), c5, c6))

def sym(cs):
    return all(cs[x - 1] == cs[160 - x] for x in range(1, 161))

with open(sys.argv[2], 'w') as f:
    for cs, srcs in found5.items():
        f.write('%s\t%d\t%s\n' % (' '.join(map(str, cs)), sym(cs), ';'.join(srcs[:5]) + (';+%d more' % (len(srcs) - 5) if len(srcs) > 5 else '')))
with open(sys.argv[3], 'w') as f:
    for cs, srcs in found6.items():
        f.write('%s\t%d\t%s\n' % (' '.join(map(str, cs)), sym(cs), ';'.join(srcs[:3])))
print('\n'.join(log))
print('distinct 5-colour partitions of [1,160]:', len(found5), ' symmetric:', sum(sym(c) for c in found5))
print('distinct 6-colour restrictions:', len(found6))
