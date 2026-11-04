"""Independent cross-check of selected two-colour witnesses with networkx (maximal-clique enumeration),
which shares no solver code with clique.c (only the file loaders of verify_ramsey.py are shared).  Each witness gets its own process and a time limit; results go to
results/crosscheck_output.txt.  Run from the repository root after fetch_data.py:  python3 crosscheck.py
"""
import os, sys, csv, json, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
IDS = ['constructions/cubic127_R4_12.g6', 'fritzcremer/R6_8/n134-gpt-6.1-sol.g6', 'alphaevolve/R(3, 13) >= 61.txt', 'alphaevolve/R(4, 15) >= 163.txt']
LIMIT = 120
CHILD = r'''
import sys, json, networkx as nx, numpy as np
sys.path.insert(0, '.'); import verify_ramsey as V
fmt, path = sys.argv[1], sys.argv[2]
C = V.load(fmt, path, '0' if fmt == 'g6' else '')
G = nx.from_numpy_array((C == 1).astype(int))
w = max(len(c) for c in nx.find_cliques(G)); print(json.dumps(dict(omega=w)), flush=True)
a = max(len(c) for c in nx.find_cliques(nx.complement(G))); print(json.dumps(dict(alpha=a)), flush=True)
'''
man = {r['id']: r for r in csv.DictReader(open('sources/manifest.csv'))}
out = []
for i in IDS:
    r = man[i]; k, l = [int(x) for x in r['parameters'].split(',')]
    if not os.path.exists(r['path']): out.append('%s: file missing (run fetch_data.py)' % i); continue
    got = {}
    try:
        p = subprocess.run([sys.executable, '-c', CHILD, r['format'], r['path']], capture_output=True, text=True, timeout=LIMIT)
        txt = p.stdout
    except subprocess.TimeoutExpired as e:
        txt = (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or '')
    for line in txt.split('\n'):
        if line.strip(): got.update(json.loads(line))
    w, a = got.get('omega'), got.get('alpha')
    ok = lambda v, lim: 'not completed in %d s' % LIMIT if v is None else ('%d (< %d, ok)' % (v, lim) if v < lim else '%d (NOT < %d)' % (v, lim))
    # the colour class called 1 is the edge set; a witness may avoid K_k in either class, so test both orders
    if w is not None and a is not None and not (w < k and a < l) and (w < l and a < k): k, l = l, k
    out.append('%s: n = %s, clique number %s, independence number %s' % (i, r['n'], ok(w, k), ok(a, l)))
    print(out[-1], flush=True)
open('results/crosscheck_output.txt', 'w').write('\n'.join(out) + '\n')
