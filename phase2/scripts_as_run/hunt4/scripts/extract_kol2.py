#!/usr/bin/env python3
"""extract_kol2.py - pull the 0/1 adjacency matrices out of a saved copy of Kolodyazhny's page
(aluarium.net/forum/wiki-article-17.html, Wayback Machine capture) and write one matrix01 file per graph.
The page gives each matrix as rows of 0/1 separated by <br />; a matrix block is a maximal run of such rows.
usage: extract_kol2.py PAGE.html[.gz] OUTDIR TAG"""
import sys, re, gzip, os, hashlib
path, out, tag = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(path, 'rb').read()
if raw[:2] == b'\x1f\x8b': raw = gzip.decompress(raw)
t = raw.decode('utf-8')
t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
x = re.sub(r'<br\s*/?>', '\n', t); x = re.sub(r'<[^>]+>', '', x)
blocks, cur = [], []
for l in (l.strip() for l in x.splitlines()):
    if re.fullmatch(r'[01]{20,}', l): cur.append(l)
    elif l == '' and cur: continue
    else:
        if cur: blocks.append(cur)
        cur = []
if cur: blocks.append(cur)
for b in blocks:
    n = len(b)
    assert all(len(r) == n for r in b), 'not square'
    assert all(b[i][i] == '0' for i in range(n)), 'diagonal'
    assert all(b[i][j] == b[j][i] for i in range(n) for j in range(n)), 'not symmetric'
    f = os.path.join(out, 'kol2_%s_n%d.matrix01' % (tag, n))
    open(f, 'w').write('\n'.join(b) + '\n')
    print(n, sum(r.count('1') for r in b) // 2, 'edges', hashlib.sha256(open(f, 'rb').read()).hexdigest(), f)
