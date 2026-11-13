"""Merge tests for R(3,3,3,5) >= 162 (XXER, EJC 11 (2004) #R35 pp.2-3: merge colours 2 and 3 of Exoo's
(3,3,3,3,3;161)-colouring).  Independent small checker (pure Python bitsets, own code).
A Schur partition P_1..P_5 of [1,160] gives the colouring of K_161 on [0,160] with colour(u,v) = index of
the part containing |u-v|.  For each pair {a,b}: is the union graph (|u-v| in P_a u P_b) K5-free?
Also checks that the remaining three colours are K3-free (sum-free), i.e. the merged colouring is a
(3,3,3,5;161) colouring iff the union is K5-free.
Input: a text file with 5 lines, each the full list of elements of one part (all of [1,160] covered), or
--half: lines list only 1..80 and the partition is symmetric (x and 161-x in the same part)."""
import sys, itertools, json


def load(path, half):
    parts = [[int(x) for x in l.replace(',', ' ').split()] for l in open(path) if l.strip() and not l.startswith('#')]
    assert len(parts) == 5, len(parts)
    if half: parts = [sorted(set(p) | {161 - x for x in p}) for p in parts]
    allx = sorted(x for p in parts for x in p)
    assert allx == list(range(1, 161)), 'not a partition of [1,160]'
    return parts


def sumfree(p):
    s = set(p)
    return not any(a + b in s for a in p for b in p if a <= b)


def has_clique(adj, cand, k):
    if k == 0: return True
    if bin(cand).count('1') < k: return False
    while cand:
        v = cand.bit_length() - 1
        cand &= ~(1 << v)
        if has_clique(adj, cand & adj[v], k - 1): return True
        if bin(cand).count('1') < k: return False
    return False


def find_clique(adj, cand, k, chosen=()):
    if k == 0: return list(chosen)
    while cand:
        if bin(cand).count('1') < k: return None
        v = cand.bit_length() - 1
        cand &= ~(1 << v)
        r = find_clique(adj, cand & adj[v], k - 1, chosen + (v,))
        if r: return r
    return None


def union_graph(D, N=161):
    return [sum(1 << j for j in range(N) if j != i and abs(i - j) in D) for i in range(N)]


def test(parts, N=161):
    res = {'sumfree': [sumfree(p) for p in parts], 'sizes': [len(p) for p in parts], 'merges': {}}
    for a, b in itertools.combinations(range(5), 2):
        D = set(parts[a]) | set(parts[b])
        adj = union_graph(D, N)
        circ = all((d in D) == ((N - d) in D) for d in range(1, N))
        if circ:
            K = find_clique(adj, adj[0], 4, (0,))
        else:
            K = find_clique(adj, (1 << N) - 1, 5)
        res['merges']['%d+%d' % (a + 1, b + 1)] = {'K5_free': K is None, 'K5': K, 'circulant': circ}
    return res


if __name__ == '__main__':
    half = '--half' in sys.argv
    path = [a for a in sys.argv[1:] if not a.startswith('--')][0]
    print(json.dumps(test(load(path, half))))
