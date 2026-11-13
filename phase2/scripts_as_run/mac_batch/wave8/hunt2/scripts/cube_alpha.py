"""Exact test: does Cay(Z_p, H0) (H0 = nonzero cubes mod p, p = 1 mod 6) have an independent set
of size L?  Reduction (not used by repo/verify_ramsey.py, which only uses translations):
x -> a*x + b with a in H0 is an automorphism, transitive on Z_p, and the stabiliser of 0
(multiplication by H0) is transitive on each coset g*H0 and g^2*H0.  So an independent set of
size >= 2 can be moved to contain 0 and w in {g, g^2}; the rest is a clique of size L-2 in the
complement restricted to the common non-neighbours of 0 and w.  Runs clique.c (repo copy) on
both subproblems.  Usage: python3 cube_alpha.py P L TIMEOUT_EACH"""
import sys, subprocess, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
CL = os.path.join(HERE, '..', 'tools', 'clique')
if not os.path.exists(CL): subprocess.run(['cc', '-O2', '-o', CL, CL + '.c'], check=True)
p, L, to = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
def order(a):
    x, k = a, 1
    while x != 1: x = x * a % p; k += 1
    return k
g = next(a for a in range(2, p) if order(a) == p - 1)
H = {pow(x, 3, p) for x in range(1, p)}
nonadj = lambda x, y: x != y and ((x - y) % p) not in H
for w in (g, g * g % p):
    V = [v for v in range(p) if nonadj(v, 0) and nonadj(v, w)]
    inp = '%d\n' % len(V) + '\n'.join(''.join('1' if nonadj(a, b) else '0' for b in V) for a in V) + '\n'
    t = time.time()
    try:
        r = subprocess.run([CL, str(L - 2)], input=inp, capture_output=True, text=True, timeout=to)
        print('p=%d L=%d w=%d |V|=%d: %s  nodes:%s  %.1fs' % (p, L, w, len(V), r.stdout.strip()[:60], r.stderr.strip()[-40:], time.time() - t), flush=True)
    except subprocess.TimeoutExpired:
        print('p=%d L=%d w=%d |V|=%d: not completed in %ds' % (p, L, w, len(V), to), flush=True)
