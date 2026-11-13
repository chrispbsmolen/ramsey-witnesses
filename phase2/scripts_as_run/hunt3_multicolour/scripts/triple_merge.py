"""Optional extension for R(3,3,3,5) >= 162: a 6-colour sum-free colouring of [1,160] gives a linear
colouring of K_161 (colour of uv = colour of |u-v|) with 6 triangle-free colours. Merging three colours
gives a (3,3,3,5;161)-colouring iff the union of the three is K5-free. Tests all 20 triples.
Usage: python3 -I triple_merge.py mined6.tsv out.txt [max_lines] [time_limit_s]"""
import sys, itertools, time

N = 161

def find_k5(adj):
    # adj: list of int bitmasks. returns a K5 or None
    def rec(cand, k, chosen):
        if k == 0:
            return chosen
        while cand:
            if bin(cand).count('1') < k:
                return None
            v = cand.bit_length() - 1
            cand &= ~(1 << v)
            r = rec(cand & adj[v], k - 1, chosen + [v])
            if r:
                return r
        return None
    return rec((1 << N) - 1, 5, [])

lim = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
tl = float(sys.argv[4]) if len(sys.argv) > 4 else 540
t0 = time.time()
done = hits = 0
with open(sys.argv[2], 'w') as out:
    for line in open(sys.argv[1]):
        if done >= lim or time.time() - t0 > tl:
            break
        w = [int(x) for x in line.split('\t')[0].split()]
        for tri in itertools.combinations(range(6), 3):
            D = {d for d in range(1, N) if w[d - 1] in tri}
            adj = [sum(1 << j for j in range(N) if j != i and abs(i - j) in D) for i in range(N)]
            K = find_k5(adj)
            if K is None:
                hits += 1
                out.write('K5-FREE\t%s\t%s\n' % (tri, line.split('\t')[2].strip()))
        done += 1
    out.write('# lines tested %d, triples %d, K5-free hits %d, seconds %.1f\n' % (done, 20 * done, hits, time.time() - t0))
print(done, hits, round(time.time() - t0, 1))
