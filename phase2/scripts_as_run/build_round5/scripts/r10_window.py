"""Step 2: R(10,10,10) colour 1, the computed part that Rowley AJC 81(2) (2021) Theorem 3.2 (statement p.248, proof
pp.248-250) leaves.  W = built/R10^3_n23093.lengths (U = (10,3;30) from Rowley's sheet, m = 30, V = Q_797).  The theorem:
the clique number of W in a remaining colour of U is at most that colour's clique number in the subgraph of W induced
by the first Q(m-2) edge-lengths, Q = max(k_s - 1) = 9, so Q(m-2) = 252: vertices 0..252, 253 vertices.
Checks here: (a) file SHA-256 = the row's; (b) N = 23093 and the lengths 1..252 are read from the file; (c) no K_10 in
colour 1 of that 253-vertex graph, by clique.c and gen0 on the whole window (no reduction), and by linear0 on the
window as a linear colouring (N = 253; valid because any clique inside 0..252 shifts to one through vertex 0 that stays
inside 0..252); (d) control: the same three solvers are also asked for K_9 on
the window and the answers are recorded (a FOUND there shows that the solvers report cliques on this input).
Usage: python3 r10_window.py LENGTHS_FILE TIMEOUT    Appends to logs/r10_window.jsonl."""
import sys, os, subprocess, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L

path, to = sys.argv[1], int(sys.argv[2])
PINNED = '7c26d1205680411161a5f0ff010d738bd1d838509e396672fd1cafd1635462a2'
sha = L.sha256_file(path)
tok = open(path).read().split()
N = int(tok[0]); c = [None] + [int(x) for x in tok[1:N]]
assert len(c) == N
WIN = 9 * (30 - 2)            # Q(m-2) = 252 edge-lengths
n = WIN + 1                    # vertices 0..252
d = np.abs(np.arange(n)[:, None] - np.arange(n)[None, :])
cl = np.array([0] + c[1:WIN + 1])
rec = dict(object='R(10,10,10) W', file=os.path.basename(path), sha256=sha, sha_match=(sha == PINNED), N=N, N_ok=(N == 23093),
           window_lengths=WIN, window_vertices=n, colours_in_window=sorted(set(cl[1:].tolist())))
out = {}
for k in (10, 9):
    A = (cl[d] == 1) & (d > 0)
    r = {}
    for chk in ('clique', 'gen0'):
        f, o, s = L.solve(chk, A, k, to); r[chk] = dict(found=f, out=o, seconds=s)
    # linear0 on the window as a linear colouring of K_253
    with tempfile.NamedTemporaryFile('w', suffix='.lengths', delete=False) as t:
        t.write('%d\n%s\n' % (n, ' '.join(str(x) for x in cl[1:]))); tp = t.name
    t0 = time.time()
    p = subprocess.run([os.path.join(L.TOOLS, 'linear0'), tp, '1', str(k)], capture_output=True, text=True, timeout=to)
    os.unlink(tp)
    o = p.stdout.strip(); r['linear0'] = dict(found=o.startswith('FOUND') if o[:4] in ('FOUN', 'NONE') else None, out=o[:200], seconds=round(time.time() - t0, 1))
    out['K%d_in_colour1' % k] = r
rec['checks'] = out
ok10 = rec['sha_match'] and rec['N_ok'] and all(out['K10_in_colour1'][x]['found'] is False for x in ('clique', 'gen0', 'linear0'))
rec['claim'] = 'no K_10 in colour 1 of W restricted to vertices 0..252 (Rowley Thm 3.2 then gives no K_10 in colour 1 of W)'
rec['verdict'] = 'PASS (clique.c, gen0, linear0)' if ok10 else 'NOT CONFIRMED'
L.log('r10_window.jsonl', rec)
