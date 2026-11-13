"""Timed small tests for the Mac job specs: how long does clique.c take to show 'no independent
l-set' on random induced subgraphs of growing order of the search graph?

  python3 estimate.py CELL [MAXSEC]

Search graph: for a graph with proved vertex transitivity (see verify_built.py) the complement of
the closed neighbourhood structure is used exactly as clique.c --sym does (independent (l-1)-sets
among the non-neighbours of vertex 0); otherwise the whole graph with target l.  For each order
n' (increasing by 5% steps of the search graph's order, 3 random subsets each) the median time of
clique.c --complement is recorded, until a run exceeds MAXSEC/3 or the full order is reached.
A log-linear fit of time against n' is extrapolated to the full order.  This is an
order-of-magnitude estimate only (branch-and-bound time is erratic).
Appends to logs/estimate.jsonl.
"""
import os, sys, json, time, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools')); sys.path.insert(0, HERE)
import verify_ramsey as V
import g3lib as L
from verify_built import load_built

V.ensure_solver()


def run(A, t, timeout):
    n = len(A)
    buf = '%d\n' % n + '\n'.join(''.join('1' if x else '0' for x in row) for row in A) + '\n'
    t0 = time.time()
    p = subprocess.run([V.CLIQUE, str(t), '--complement'], input=buf, capture_output=True, text=True, timeout=timeout)
    return time.time() - t0, p.stdout.strip(), p.stderr.strip()


def main():
    cell = sys.argv[1]; MAXSEC = float(sys.argv[2]) if len(sys.argv) > 2 else 150
    C, m = load_built(cell)
    k, l = [int(x) for x in cell.replace('aux_', '').split(',')]
    A = (C == 1).astype(np.uint8); np.fill_diagonal(A, 0); n = len(A)
    sym = False
    if 'vt_generators' in m:
        gens = [np.array(g) for g in m['vt_generators']]
        sym = all(L.is_automorphism(A, g) for g in gens) and L.orbit_of_0(n, gens) == n
    if sym:
        X = [v for v in range(1, n) if not A[0][v]]; t = l - 1
    else:
        X = list(range(n)); t = l
    N = len(X); rng = np.random.default_rng(12345)
    pts = []; spent = 0.0
    for frac in np.arange(0.10, 1.0001, 0.05):
        size = int(round(frac * N)); times = []; outs = []
        for rep in range(3):
            S = sorted(rng.choice(X, size=size, replace=False)) if size < N else X
            try:
                dt, out, err = run(A[np.ix_(S, S)], t, MAXSEC / 3)
            except subprocess.TimeoutExpired:
                dt, out, err = MAXSEC / 3, 'TIMEOUT', ''
            times.append(dt); outs.append(out.split()[0] + ' ' + err); spent += dt
            if out.startswith('FOUND'): print('FOUND in a subgraph?!', cell, size, out); return
            if size == N: break
        med = float(np.median(times)); pts.append((size, med, outs))
        print('%s n\'=%d/%d target %d: median %.2f s %s' % (cell, size, N, t, med, outs), flush=True)
        if med >= MAXSEC / 3 * 0.99 or 'TIMEOUT' in ' '.join(outs) or spent > MAXSEC * 2: break
    good = [(s, tm) for s, tm, _ in pts if tm > 0.05 and tm < MAXSEC / 3 * 0.99]
    est = None
    if len(good) >= 3:
        xs = np.array([s for s, _ in good], dtype=float); ys = np.log(np.array([tm for _, tm in good]))
        a, b = np.polyfit(xs[-4:], ys[-4:], 1)
        est = float(np.exp(a * N + b))
    rec = dict(cell=cell, n=n, sym=sym, search_order=N, target=t, points=[(s, round(tm, 3)) for s, tm, _ in pts],
               extrapolated_seconds_full=est, completed_full=bool(pts and pts[-1][0] == N and pts[-1][1] < MAXSEC / 3 * 0.99))
    print(json.dumps(rec))
    open(os.path.join(HERE, 'logs', 'estimate.jsonl'), 'a').write(json.dumps(rec) + '\n')


if __name__ == '__main__':
    main()
