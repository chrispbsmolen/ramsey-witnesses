import random, networkx as nx, importlib.util, sys
spec = importlib.util.spec_from_file_location('cc', sys.argv[1]); src = open(sys.argv[1]).read().replace('\nmain()\n', '\n')
ns = {}; exec(compile(src, 'cc', 'exec'), ns)
rng = random.Random(3); bad = 0
for t in range(60):
    n = rng.randint(10, 70); p = rng.choice([0.2, 0.4, 0.6, 0.8])
    G = nx.gnp_random_graph(n, p, seed=t)
    A = [sum(1 << j for j in G[i]) for i in range(n)]
    w = max(len(c) for c in nx.find_cliques(G))
    if not (ns['has_clique'](A, (1 << n) - 1, w) and not ns['has_clique'](A, (1 << n) - 1, w + 1)): bad += 1
# circulant check: Paley(101) has clique number 5
N = 101; QR = {(x * x) % N for x in range(1, N)}
c = [None] + [1 if d in QR else 2 for d in range(1, N)]
A = ns['adj_bits'](N, c, 1)
print('random disagreements', bad, '| Paley101 K5 through 0:', ns['has_clique'](A, A[0], 4), 'K6 through 0:', ns['has_clique'](A, A[0], 5))
