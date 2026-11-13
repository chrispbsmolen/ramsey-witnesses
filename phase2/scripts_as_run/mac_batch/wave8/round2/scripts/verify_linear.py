"""Check one built linear colouring (built/*.lengths) with one checker.

  python3 verify_linear.py FILE K CHECKER [COLOUR] [TIMEOUT_S]
    FILE     built/....lengths(.gz)   K  forbidden clique size (same for every colour: diagonal cells)
    CHECKER  repo     : repo/verify_ramsey.py (byte-identical copy in checker/), verify() on the full colour
                        matrix; it tests circulance itself and then searches cliques through vertex 0.  N <= 4200.
             repo_stream : the same solver (checker/clique_r2 = repo clique.c compiled under a new name) fed
                        one colour class by checker/stream_adj.py (round-1 hunt_multicolour script); --sym only
                        when the colouring is cyclic (tested here on the length vector: c[d] == c[N-d]).
             repo_stream_full : as repo_stream but never --sym (all vertices searched, no symmetry used).
             gen0_full : checker/gen0_r2 (independent of clique.c) on the whole colour class, no symmetry used.
             repo_nbhd : clique.c without --sym on the subgraph induced by N(0) in COLOUR, searching K_{K-1};
                        only for cyclic colourings (rotation is an automorphism, tested) -- the reduction that
                        --sym performs, done outside clique.c so the n x n matrix need not be held (N > 40000).
             mc       : checker/crosscheck_mc.py (round-1 pure-Python checker, shares no code with clique.c).
             linear0  : checker/linear0_r2 (round-1 linear0.c compiled under a new name; translation reduction
                        for linear colourings, independent of clique.c).
             sumfree  : K must be 3.  Exact check that no a, b with a+b <= N-1 have c[a] = c[b] = c[a+b]
                        (a monochromatic triangle {i<j<k} exists iff such a, b exist: a=j-i, b=k-j).  numpy.
Appends one JSON line to logs/verify_linear.jsonl.
"""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lib2 as L

CH = L.CHECKER
# binary names can be overridden (Mac runs compile the same sources under new names)
CLQ = os.environ.get('CLIQUE_BIN', os.path.join(CH, 'clique_r2'))
LIN = os.environ.get('LINEAR0_BIN', os.path.join(CH, 'linear0_r2'))
GEN = os.environ.get('GEN0_BIN', os.path.join(CH, 'gen0_r2'))


def main():
    path, k, checker = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    colour = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != 'all' else None
    T = float(sys.argv[5]) if len(sys.argv) > 5 else 560
    full = os.path.join(L.OUT, path)
    N, c = L.read_lengths(full)
    cyc = L.is_cyclic(N, c)
    cols = L.colours(c)
    todo = [colour] if colour else cols
    rec = dict(file=path, sha256=L.sha256_file(full), N=N, k=k, checker=checker, colours=todo, cyclic=cyc, timeout=T)
    t0 = time.time()
    res = {}
    try:
        if checker == 'repo':
            assert N <= 4200
            import verify_ramsey as V
            idx = np.abs(np.arange(N)[:, None] - np.arange(N)[None, :])
            C = np.array([-1] + [x - 1 for x in c[1:]], dtype=np.int64)[idx]
            out = V.verify(C, [k] * len(cols), timeout=T)
            res = out
        elif checker in ('repo_stream', 'repo_nbhd', 'repo_stream_full', 'gen0_full'):
            for col in todo:
                t1 = time.time()
                if checker in ('repo_stream', 'repo_stream_full', 'gen0_full'):
                    args = ([GEN, str(k)] if checker == 'gen0_full' else [CLQ, str(k)] + (['--sym'] if cyc and checker == 'repo_stream' else []))
                    feed = subprocess.Popen([sys.executable, '-I', os.path.join(CH, 'stream_adj.py'), full if not full.endswith('.gz') else unz(full), str(col)], stdout=subprocess.PIPE)
                    p = subprocess.run(['bash', '-c', 'ulimit -s unlimited; exec "$@"', 'x'] + args, stdin=feed.stdout, capture_output=True, text=True, timeout=T)
                    feed.wait()
                else:
                    assert cyc, 'repo_nbhd needs a cyclic colouring'
                    S = [d for d in range(1, N) if c[d] == col]     # N(0) in colour col
                    cc = np.array([0] + c[1:], dtype=np.int16)
                    Sa = np.array(S)
                    import tempfile
                    outf = tempfile.TemporaryFile(); errf = tempfile.TemporaryFile()
                    pr = subprocess.Popen(['bash', '-c', 'ulimit -s unlimited; exec "$@"', 'x', CLQ, str(k - 1)],
                                          stdin=subprocess.PIPE, stdout=outf, stderr=errf)
                    pr.stdin.write(b'%d\n' % len(S))
                    for i, a in enumerate(S):
                        row = (cc[np.abs(Sa - a)] == col); row[i] = False
                        pr.stdin.write((row.astype(np.uint8) + 48).tobytes() + b'\n')
                    pr.stdin.close(); pr.wait(timeout=T)
                    outf.seek(0); errf.seek(0)
                    p = subprocess.CompletedProcess(pr.args, pr.returncode, outf.read(), errf.read())
                    p = subprocess.CompletedProcess(p.args, p.returncode, p.stdout.decode(), p.stderr.decode())
                res[str(col)] = dict(out=p.stdout.strip(), err=p.stderr.strip()[-200:], seconds=round(time.time() - t1, 1))
        elif checker == 'mc':
            assign = ['%d:%d' % (col, k) for col in cols]
            p = subprocess.run([sys.executable, os.path.join(CH, 'crosscheck_mc.py'), full, ','.join([str(k)] * len(cols))] + assign,
                               capture_output=True, text=True, timeout=T)
            res = json.loads(p.stdout.strip().split('\n')[-1])
        elif checker == 'linear0':
            for col in todo:
                t1 = time.time()
                p = subprocess.run([LIN, full if not full.endswith('.gz') else unz(full), str(col), str(k)],
                                   capture_output=True, text=True, timeout=T)
                res[str(col)] = dict(out=p.stdout.strip(), seconds=round(time.time() - t1, 1))
        elif checker == 'sumfree':
            assert k == 3
            cc = np.array([0] + c[1:], dtype=np.int16)
            bad = 0
            for col in todo:
                S = np.nonzero(cc == col)[0]; S = S[S > 0]
                ind = (cc == col)
                cnt = 0
                for a in S:
                    b = S[(S >= a) & (S + a <= N - 1)]
                    cnt += int(ind[a + b].sum())
                res[str(col)] = dict(monochromatic_sums=cnt, size=int(len(S)))
                bad += cnt
            res['verdict'] = 'PASS' if bad == 0 else 'FAIL'
        else:
            raise ValueError(checker)
        rec['result'] = res
    except subprocess.TimeoutExpired:
        rec['result'] = 'TIMEOUT'; rec['partial'] = res
    rec['seconds'] = round(time.time() - t0, 1)
    L.log('verify_linear.jsonl', rec)


def unz(path):
    import gzip
    out = os.path.join('<scratch>', os.path.basename(path)[:-3])
    if not os.path.exists(out): open(out, 'wb').write(gzip.open(path).read())
    return out


if __name__ == '__main__':
    main()
