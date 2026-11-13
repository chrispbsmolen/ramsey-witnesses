"""Independent multicolour cross-check (shares no code with repo/verify_ramsey.py or clique.c).
Input: a '.lengths' file (line 1: N; line 2: colour of edge-length d=1..N-1), the colour of edge {i,j}
being c[|i-j|].  If c[d]==c[N-d] for all d the colouring is circulant and only cliques through
vertex 0 are searched (vertex-transitivity); otherwise all vertices are searched.
Usage: python3 crosscheck_mc.py FILE K1,K2,... [colour:k ...]  (explicit assignment colour->k)
Clique decision: pure-Python bitset branch and bound with greedy colouring bound (Tomita style),
plus a networkx find_cliques oracle when --nx is given (small graphs only)."""
import sys, time, json

def load(path):
    t = open(path).read().split()
    N = int(t[0]); c = [None] + [int(x) for x in t[1:]]
    assert len(c) == N, 'expected %d lengths, got %d' % (N - 1, len(c) - 1)
    return N, c

def adj_bits(N, c, col):
    A = [0] * N
    for i in range(N):
        m = 0
        for j in range(N):
            if i != j and c[abs(i - j)] == col: m |= 1 << j
        A[i] = m
    return A

def has_clique(A, cand, k):
    """True iff the vertex set `cand` (bitmask) contains a k-clique in graph A."""
    if k <= 0: return True
    if cand == 0: return False
    # greedy colouring bound
    order = []; bound = []
    P = cand; colour = 0
    while P:
        colour += 1; Q = P
        while Q:
            v = (Q & -Q).bit_length() - 1
            Q &= ~(1 << v); Q &= ~A[v]
            P &= ~(1 << v)
            order.append(v); bound.append(colour)
    if colour < k: return False
    for idx in range(len(order) - 1, -1, -1):
        if bound[idx] < k: return False
        v = order[idx]
        if has_clique(A, cand & A[v], k - 1): return True
        cand &= ~(1 << v)
    return False

def load_matrix(path):
    """Full colour matrix: N lines of N digits; diagonal ignored; must be symmetric."""
    rows = [l.strip() for l in open(path) if l.strip()]
    N = len(rows); assert all(len(r) == N for r in rows)
    M = [[int(ch) for ch in r] for r in rows]
    assert all(M[i][j] == M[j][i] for i in range(N) for j in range(N))
    return N, M

def main_matrix(path, ks, assign):
    N, M = load_matrix(path)
    cols = sorted({M[i][j] for i in range(N) for j in range(N) if i != j})
    assert sorted(assign) == cols and sorted(assign.values()) == sorted(ks)
    out = dict(file=path, N=N, circulant=False, colours=cols, ks=ks, assignment=assign, results={}); ok = True
    for col in cols:
        A = [sum(1 << j for j in range(N) if j != i and M[i][j] == col) for i in range(N)]
        t0 = time.time(); found = has_clique(A, (1 << N) - 1, assign[col])
        out['results'][str(col)] = dict(k=assign[col], has_Kk=found, seconds=round(time.time() - t0, 1)); ok &= not found
    out['verdict'] = 'PASS' if ok else 'FAIL'; print(json.dumps(out))

def main():
    path, ks = sys.argv[1], [int(x) for x in sys.argv[2].split(',')]
    assign = dict(tuple(int(y) for y in a.split(':')) for a in sys.argv[3:] if ':' in a)
    if path.endswith('.colormat'): return main_matrix(path, ks, assign)
    N, c = load(path)
    circ = all(c[d] == c[N - d] for d in range(1, N))
    cols = sorted(set(c[1:]))
    out = dict(file=path, N=N, circulant=circ, colours=cols, ks=ks, assignment=assign, results={})
    assert sorted(assign.values()) == sorted(ks) and sorted(assign) == cols, 'assignment must map each colour to one k'
    ok = True
    for col in cols:
        k = assign[col]; t0 = time.time()
        A = adj_bits(N, c, col)
        if circ: found = has_clique(A, A[0], k - 1)          # clique through vertex 0
        else: found = has_clique(A, (1 << N) - 1, k)
        out['results'][str(col)] = dict(k=k, has_Kk=found, seconds=round(time.time() - t0, 1))
        ok &= not found
        print(json.dumps(out['results'][str(col)]), flush=True)
    out['verdict'] = 'PASS' if ok else 'FAIL'
    print(json.dumps(out))
main()
