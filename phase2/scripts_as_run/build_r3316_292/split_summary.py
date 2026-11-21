#!/usr/bin/env python3
"""split_summary.py - coverage check of a split_check.py log.  For each checker: every vertex v = 0..n-1 must occur
exactly once, with answer NONE.  The pieces are recomputed here from the colouring file (own code): |P(v)| and the
SHA-256 of the piece text must equal the logged values, the sizes must add up to the number of edges of the class,
and the two checkers must have been given identical pieces.
usage: split_summary.py COLORMAT DIGIT K LOG"""
import sys, json, hashlib
path, digit, k, log = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
rows = [l.strip() for l in open(path) if l.strip()]; n = len(rows)
sha = hashlib.sha256(open(path, 'rb').read()).hexdigest()
edges = sum(1 for i in range(n) for j in range(i) if rows[i][j] == digit)
piece = {}
for v in range(n):
    P = [w for w in range(v + 1, n) if rows[v][w] == digit]
    txt = '%d\n' % len(P) + ''.join(''.join('1' if (x != y and rows[x][y] == digit) else '0' for y in P) + '\n' for x in P)
    piece[v] = (len(P), hashlib.sha256(txt.encode()).hexdigest())
recs = [json.loads(l) for l in open(log) if l.strip()]
recs = [r for r in recs if r['file_sha256'] == sha and r['colour_digit'] == digit and r['k'] == k]
out = {'file_sha256': sha, 'n': n, 'colour_digit': digit, 'k': k, 'class_edges': edges,
       'sum_of_piece_sizes': sum(p[0] for p in piece.values()), 'largest_piece': max(p[0] for p in piece.values()),
       'pieces_below_k_minus_1_vertices': sum(1 for p in piece.values() if p[0] < k - 1), 'checkers': {}}
ok = out['sum_of_piece_sizes'] == edges
for chk in ('clique', 'gen0'):
    rs = [r for r in recs if r['checker'] == chk]
    vs = sorted(r['v'] for r in rs)
    c = {'records': len(rs), 'every_v_once': vs == list(range(n)),
         'all_none': all(r['none'] and not r['found'] for r in rs),
         'pieces_match_recomputation': all(piece[r['v']] == (r['piece_vertices'], r['piece_sha256']) for r in rs),
         'all_asked_for_k_minus_1': all(r['asked_for'] == k - 1 for r in rs),
         'seconds_total': round(sum(r['seconds'] for r in rs), 1), 'seconds_max_piece': max(r['seconds'] for r in rs)}
    c['complete'] = all(c[x] for x in ('every_v_once', 'all_none', 'pieces_match_recomputation', 'all_asked_for_k_minus_1'))
    ok = ok and c['complete']; out['checkers'][chk] = c
out['verdict'] = ('NONE: no K_%d in the class (exact split by smallest vertex, every piece present once, both checkers)' % k) if ok else 'INCOMPLETE'
print(json.dumps(out, sort_keys=True, indent=1))
