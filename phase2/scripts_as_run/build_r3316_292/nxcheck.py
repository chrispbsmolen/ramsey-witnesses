#!/usr/bin/env python3
"""nxcheck.py - third check, independent of clique.c and gen0.c: for each digit of the matrix file the clique number
of that class, by networkx maximal-clique enumeration (nx.find_cliques); the file is parsed here.
The largest clique met so far is printed if the time limit stops the enumeration (then nothing is concluded).
usage: nxcheck.py PATH DIGITS(e.g. 012) LIMIT_SECONDS"""
import sys, time, hashlib
import networkx as nx
path, digits, lim = sys.argv[1], sys.argv[2], float(sys.argv[3])
rows = [l.strip() for l in open(path) if l.strip()]; n = len(rows)
print('file', path.split('/')[-1], 'sha256', hashlib.sha256(open(path, 'rb').read()).hexdigest(), 'n', n, 'networkx', nx.__version__)
for d in digits:
    G = nx.Graph(); G.add_nodes_from(range(n))
    G.add_edges_from((i, j) for i in range(n) for j in range(i) if rows[i][j] == d)
    t = time.time(); best = 0; cnt = 0; done = True
    for c in nx.find_cliques(G):
        cnt += 1
        if len(c) > best: best = len(c)
        if cnt % 4096 == 0 and time.time() - t > lim: done = False; break
    print('digit', d, 'edges', G.number_of_edges(), 'maximal cliques enumerated', cnt,
          ('clique number %d' % best) if done else ('NOT COMPLETED in %d s (largest seen %d)' % (lim, best)), 'seconds %.1f' % (time.time() - t), flush=True)
