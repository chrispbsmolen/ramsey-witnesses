"""Independent cross-check, same method as repo/crosscheck.py (networkx maximal-clique enumeration,
shares only the loader with verify_ramsey.py). Copy of its CHILD logic so that nothing is written into ./repo.
Usage: python3 xcheck.py FORMAT SRC K,L LIMIT_SECONDS [--sym]
--sym (circulant only, tested): the independence number is taken over cliques of the complement through vertex 0."""
import sys, json, subprocess, os
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools')
CHILD = r'''
import sys, json, networkx as nx, numpy as np
sys.path.insert(0, sys.argv[3]); import verify_ramsey as V
fmt, path, entry = sys.argv[1], sys.argv[2], sys.argv[4]
C = V.load(fmt, path, entry)
G = nx.from_numpy_array((C == 1).astype(int))
w = max(len(c) for c in nx.find_cliques(G)); print(json.dumps(dict(omega=w)), flush=True)
H = nx.complement(G)
if sys.argv[5] == 'sym':
    assert V.is_circulant(C)   # vertex-transitive: a maximum clique may be taken through vertex 0
    a = 1 + max(len(c) for c in nx.find_cliques(H.subgraph(list(H.neighbors(0)))))
else:
    a = max(len(c) for c in nx.find_cliques(H))
print(json.dumps(dict(alpha=a)), flush=True)
'''
fmt, src, kl, lim = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
entry = ''
sym = 'sym' if '--sym' in sys.argv else 'nosym'
k, l = [int(x) for x in kl.split(',')]
try:
    p = subprocess.run([sys.executable, '-c', CHILD, fmt, src, TOOLS, entry, sym], capture_output=True, text=True, timeout=lim); txt = p.stdout + p.stderr[-300:]
except subprocess.TimeoutExpired as e:
    txt = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or '')
got = {}
for line in txt.split('\n'):
    if line.strip().startswith('{'): got.update(json.loads(line))
w, a = got.get('omega'), got.get('alpha')
if w is not None and a is not None and not (w < k and a < l) and (w < l and a < k): k, l = l, k
ok = lambda v, lim_: 'not completed in %d s' % lim if v is None else ('%d (< %d, ok)' % (v, lim_) if v < lim_ else '%d (NOT < %d)' % (v, lim_))
print('%s %s: clique number %s, independence number %s' % (fmt, src[:40], ok(w, k), ok(a, l)))
