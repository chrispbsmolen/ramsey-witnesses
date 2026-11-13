"""Independence half of the input (6,20;877) graph (R(6,20) > 877), symmetry-reduced, with both checkers.

Object: inputs/R6_20_n877_SLLLcubic.g6 (SHA-256 ef50e6ab...), loaded as a matrix.  Everything below is
checked on that matrix, nothing is assumed from the formula:
  1. t: x -> x+1 and c: x -> g^3 x (g the least primitive root mod 877) are automorphisms of the matrix;
     <t> is transitive, so a maximum independent set may be taken through 0.
  2. c fixes 0; the orbits of <c> on the non-neighbours of 0 (vertices != 0) are computed: the reduction
     needs exactly two orbits, with representatives w1, w2.  An independent set of size >= 2 through 0
     contains some non-neighbour x of 0, and an element of <c> maps x to w1 or w2 while fixing 0.
  3. For w in {w1, w2}: S = common non-neighbours of 0 and w; the question "independent L-set in G" reduces
     to "independent (L-2)-set in G[S]", i.e. a K_(L-2) in the complement of G[S].  With L = 20 (target
     alpha(G) <= 19) each subproblem is run with
        repo : tools/clique (clique.c, unchanged repo copy), no --sym
        gen0 : tools/gen0 (gen0.c, build_round2), independent of clique.c
     and a negative control (K_(L-3), i.e. an independent 19-set through 0 and w, must be FOUND by clique.c
     in at least one subproblem since alpha(G) = 19).
Usage: python3 src/alpha_877.py CHECKER W_INDEX TIMEOUT [neg]       appends to logs/alpha_877.jsonl
"""
import os, sys, json, time, subprocess
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import verify_ramsey as V

checker, wi, T = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
neg = len(sys.argv) > 4 and sys.argv[4] == 'neg'
L = 20
path = os.path.join(HERE, 'inputs', 'R6_20_n877_SLLLcubic.g6')
h = V.sha256_file(path); assert h == 'ef50e6ab42e3814f4abd9118d26724df25c3a4ccd819774d7add6964a8ed20be'
C = V.load_g6(path); p = len(C)
A = (C == 1).astype(np.uint8); np.fill_diagonal(A, 0)
def order(a):
    x, k = a, 1
    while x != 1: x = x * a % p; k += 1
    return k
g = next(a for a in range(2, p) if order(a) == p - 1)
c = pow(g, 3, p)
perm_t = (np.arange(p) + 1) % p
perm_c = (np.arange(p) * c) % p
is_aut = lambda P: bool((A[np.ix_(P, P)] == A).all())
rec = dict(object='R6_20_n877_SLLLcubic.g6', sha256=h, n=p, checker=checker, primitive_root=g, multiplier=c,
           aut_translation=is_aut(perm_t), aut_multiplier=is_aut(perm_c))
seen = {0}; st = [0]
while st:
    x = st.pop(); y = int(perm_t[x])
    if y not in seen: seen.add(y); st.append(y)
rec['transitive'] = len(seen) == p
non = [x for x in range(1, p) if not A[0][x]]
orbits = []; left = set(non)
while left:
    x0 = min(left); orb = set(); x = x0
    while x not in orb: orb.add(x); x = x * c % p
    orbits.append(sorted(orb)); left -= orb
rec['nonneighbours_of_0'] = len(non); rec['orbits_on_nonneighbours'] = [len(o) for o in orbits]
reps = [o[0] for o in orbits]; rec['representatives'] = reps
assert rec['aut_translation'] and rec['aut_multiplier'] and rec['transitive'] and all(int(perm_c[0]) == 0 for _ in [0])
assert sorted(sum(orbits, [])) == non
w = reps[wi]
S = [v for v in range(p) if v not in (0, w) and not A[0][v] and not A[w][v]]
Y = (1 - A[np.ix_(S, S)]).astype(np.uint8); np.fill_diagonal(Y, 0)   # complement of G[S]
size = L - 2 - (1 if neg else 0)
rec.update(w=w, subproblem_order=len(S), searched_clique_size=size, claim=('no independent %d-set through 0 and %d' % (size + 2, w)),
           negative_control=neg)
inp = ('%d\n' % len(S)).encode() + b'\n'.join(bytes((r + 48).astype(np.uint8)) for r in Y) + b'\n'
exe = {'repo': os.path.join(HERE, 'tools', 'clique'), 'gen0': os.path.join(HERE, 'tools', 'gen0')}[checker]
t0 = time.time()
try:
    r = subprocess.run(['bash', '-c', 'ulimit -s unlimited 2>/dev/null; exec "$@"', 'x', exe, str(size)], input=inp, capture_output=True, timeout=T)
    out = r.stdout.decode().strip(); rec['solver'] = out[:200]; rec['result'] = out.split()[0] if out else 'ERROR ' + r.stderr.decode()[-200:]
except subprocess.TimeoutExpired:
    rec['result'] = 'TIMEOUT'
rec['seconds'] = round(time.time() - t0, 1)
print(json.dumps(rec), flush=True)
open(os.path.join(HERE, 'logs', 'alpha_877.jsonl'), 'a').write(json.dumps(rec) + '\n')
