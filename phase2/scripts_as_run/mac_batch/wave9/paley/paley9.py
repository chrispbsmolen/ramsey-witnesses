"""paley9.py: the clique number of the Paley graph G_p (p prime, p = 1 mod 4), in restartable pieces, both checkers.

Same automorphisms and same checkers as build_round5/scripts/paley_check.py (rows R(13,13)..R(18,18)).  New here:
every (subproblem, checker) pair is its own restartable piece, and there are two modes for the subproblems:
  plain    T_a = B & N(a): exactly the subproblems of paley_check.py;
  ordered  T_a = the vertices of B & N(a) whose sigma-orbit is not earlier than a's (see below): the same
           automorphisms, about 8 times less work.

The reduction (Amendments 1 and 5), every step verified on the object by `verify` before anything is searched:
  G_p is the circulant on Z_p with connection set QR = nonzero squares mod p, A[x][y] = QR[(y - x) mod p].
  (a) QR = -QR and |QR| = (p-1)/2;
  (b) x -> x + 1 is an automorphism (the matrix is circulant: every entry compared, row block by row block);
  (c) x -> g^2 x (g the least primitive root) maps QR to QR and its powers are transitive on QR, so the group
      {x -> a x + b, a in QR} is transitive on ordered edges: every edge can be moved to (0,1);
  (d) sigma: x -> 1 - x is an automorphism (-1 in QR) that fixes the edge {0,1} and maps B = N(0) & N(1) to itself.
  Hence a K_(k+1) exists iff, for some representative a of a sigma-orbit {a, 1-a} on B, the set T_a = B & N(a)
  holds a K_(k-2).  The representatives are reps[0..R-1] (the least element of each orbit, in increasing order).
  Ordered mode.  Write idx(x) for the index of the orbit {x, 1-x} of x in B; idx(x) = idx(sigma(x)).  Let K be a
  K_(k+1) through 0 and 1.  Its other vertices lie in B.  Take one, x, with idx(x) = i least.  If x is not the
  representative a = reps[i], replace K by sigma(K) (also a clique through 0 and 1, with the same idx values, and
  it contains a).  Then K - {0, 1, a} is a K_(k-2) inside {y in B & N(a) : idx(y) >= i}.  So a K_(k+1) exists iff
  for some i the set T'_i = {y in B & N(reps[i]) : idx(y) >= i} holds a K_(k-2).  This uses only sigma, which
  (d) verifies, and the fact that idx is constant on sigma-orbits, which `verify` also checks.  The conclusion
  needs every i (as in plain mode); `collect` enforces that.

A piece is (i, checker): the graph induced on T_a (plain) or T'_i (ordered), a = reps[i], given as text to one checker (clique.c or gen0),
which is asked for K_(k-2).  Both checkers get byte-identical input; its SHA-256 is in the record.

Coverage rule (checked by `collect`): for every i in 0..R-1 and both checkers there is exactly one record; it says
NONE; its a, vertex count and input SHA-256 equal the values `collect` recomputes from p alone; and a K_k witness
is checked edge by edge.  Only then is the verdict PASS.  A piece that is present twice, missing, FOUND or ERROR
makes the verdict INCOMPLETE or FAIL.

Subcommands (OUT is the run folder; records are only ever appended, nothing is deleted or overwritten):
  verify  P K OUT                 checks (a)-(d), appends OUT/header.jsonl
  lane    P K OUT LANE NLANES     runs the pieces with i % NLANES == LANE that have no record yet in any
                                  OUT/lane*.jsonl; appends to OUT/lane<LANE>.jsonl.  Options (environment):
                                  W9_MAXPIECES=n stop after n pieces; W9_ONLY="i1,i2,.." only these rep indices.
  witness P K OUT LANE NLANES     looks for a K_k: asks clique.c for K_(k-3) in T_a, reps of this lane in turn,
                                  until some lane has found one (checked edge by edge); appends OUT/witness<LANE>.jsonl
  collect P K OUT [WITNESSFILE]   applies the coverage rule, prints and appends the verdict to OUT/verdict.jsonl
  time    P K i1,i2,..            timing test: both checkers on those pieces, nothing recorded
Solver binaries: environment W9_CLIQUE and W9_GEN0 (full paths).  Mode: environment W9_MODE = ordered (default)
or plain; it is written into every record, and `collect` refuses a run folder that mixes modes."""
import sys, os, json, time, hashlib, subprocess, glob
import numpy as np

CHECKERS = ('gen0', 'clique')
MODE = os.environ.get('W9_MODE', 'ordered')
assert MODE in ('ordered', 'plain'), 'W9_MODE must be ordered or plain'


def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def append(path, rec):
    """Append one JSON line.  If an earlier write was cut off (file does not end in a newline), start a new line."""
    rec = dict(rec); rec['time'] = now()
    line = json.dumps(rec) + '\n'
    lead = ''
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, 'rb') as f:
            f.seek(-1, 2)
            if f.read(1) != b'\n': lead = '\n'
    with open(path, 'a') as f:
        f.write(lead + line); f.flush(); os.fsync(f.fileno())
    return rec


def read_records(path):
    """Complete JSON lines only; a cut-off line is counted and skipped."""
    recs, bad = [], 0
    if not os.path.exists(path): return recs, bad
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: recs.append(json.loads(line))
            except ValueError: bad += 1
    return recs, bad


class Paley:
    def __init__(self, p):
        assert p > 5 and p % 4 == 1 and all(p % d for d in range(2, int(p ** .5) + 1)), 'p must be a prime = 1 mod 4'
        self.p = p
        QR = np.zeros(p, dtype=bool); QR[[x * x % p for x in range(1, p)]] = True
        self.QR = QR
        B = [x for x in range(2, p) if QR[x] and QR[(x - 1) % p]]
        self.B = B; self.Bn = np.array(B)
        self.reps = sorted({min(a, (1 - a) % p) for a in B})
        pos = {a: i for i, a in enumerate(self.reps)}
        self.idx = np.array([pos[min(x, (1 - x) % p)] for x in B])      # orbit index of every vertex of B

    def sub(self, a, i=None):
        """Vertices and matrix of the subproblem of rep a = reps[i] (i given: ordered mode, else plain)."""
        keep = self.QR[(self.Bn - a) % self.p]
        if i is not None:
            assert self.reps[i] == a
            keep = keep & (self.idx >= i)
        T = self.Bn[keep]
        M = self.QR[(T[:, None] - T[None, :]) % self.p]; np.fill_diagonal(M, False)
        return T, M


def graph_text(A):
    assert A.shape[0] == A.shape[1] and (A == A.T).all() and not A.diagonal().any()
    return b'%d\n' % len(A) + b'\n'.join((r.astype(np.uint8) + 48).tobytes() for r in A) + b'\n'


def run_solver(checker, k, buf):
    exe = os.environ['W9_' + checker.upper()]
    t = time.time()
    p = subprocess.run([exe, str(k)], input=buf, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.decode(errors='replace').strip()
    sec = round(time.time() - t, 1)
    if p.returncode == 0 and out.startswith('NONE'): res = 'NONE'
    elif p.returncode == 0 and out.startswith('FOUND'): res = 'FOUND'
    else: res = 'ERROR'; out = ('rc=%d %s %s' % (p.returncode, out, p.stderr.decode(errors='replace')[-200:]))
    return res, out[:300], sec


def cmd_verify(p, k, out):
    G = Paley(p); QR = G.QR
    def order(a):
        x, e = a, 1
        while x != 1: x = x * a % p; e += 1
        return e
    g = next(a for a in range(2, p) if order(a) == p - 1)
    S = np.flatnonzero(QR)
    chk = {}
    chk['a_symmetric'] = bool(all(QR[(-s) % p] for s in S)) and len(S) == (p - 1) // 2
    ok = True; cols = np.arange(p)
    for r0 in range(0, p, 256):                      # every entry of the p x p matrix, 256 rows at a time
        rows = np.arange(r0, min(p, r0 + 256))
        A = QR[(cols[None, :] - rows[:, None]) % p]              # the matrix rows as defined
        shifted = QR[(cols[None, :] + 1 - (rows[:, None] + 1)) % p]  # A[x+1][y+1]
        row0 = np.stack([np.roll(QR, int(r)) for r in rows])     # row 0 rotated by r
        ok = ok and bool((A == shifted).all()) and bool((A == row0).all())
    chk['b_translation'] = ok
    g2 = g * g % p
    chk['c_mult_g2_preserves_QR'] = bool(all(QR[g2 * s % p] for s in S))
    orb, x = set(), 1
    while True:
        orb.add(x); x = x * g2 % p
        if x == 1: break
    chk['c_transitive_on_QR'] = orb == set(S.tolist())
    Bs = set(G.B)
    chk['d_sigma_preserves_B'] = all(((1 - a) % p) in Bs for a in G.B) and bool(QR[p - 1])
    chk['d_reps_cover_B'] = set(G.reps) | {(1 - a) % p for a in G.reps} == Bs
    ix = dict(zip(G.B, G.idx.tolist()))
    chk['d_idx_constant_on_sigma_orbits'] = all(ix[a] == ix[(1 - a) % p] and G.reps[ix[a]] in (a, (1 - a) % p) for a in G.B)
    rec = dict(type='header', mode=MODE, p=p, k=k, primitive_root=g, automorphism_checks=chk, B=len(G.B), orbit_reps=len(G.reps),
               asked='K_%d in each T_a' % (k - 2), claim='no K_%d in G_%d' % (k + 1, p), ok=all(chk.values()))
    append(os.path.join(out, 'header.jsonl'), rec)
    print(json.dumps(rec), flush=True)
    return 0 if rec['ok'] else 1


def done_keys(out, pattern, p, k):
    keys = set()
    for f in sorted(glob.glob(os.path.join(out, pattern))):
        for r in read_records(f)[0]:
            if r.get('p') == p and r.get('k') == k and 'i' in r:
                if r.get('type') == 'piece' and r.get('mode') != MODE:
                    sys.exit('STOP: %s holds records of mode %s, this run is mode %s; use one mode per run folder' % (f, r.get('mode'), MODE))
                keys.add((r['i'], r.get('checker')))
    return keys


def fmt(sec):
    return '%.1f h' % (sec / 3600.0) if sec >= 5400 else '%.0f min' % (sec / 60.0)


def cmd_lane(p, k, out, lane, nl):
    G = Paley(p); R = len(G.reps)
    only = os.environ.get('W9_ONLY'); only = {int(x) for x in only.split(',')} if only else None
    maxp = int(os.environ.get('W9_MAXPIECES', '0'))
    mine = [i for i in range(R) if i % nl == lane and (only is None or i in only)]
    done = done_keys(out, 'lane*.jsonl', p, k)
    todo = [(i, c) for i in mine for c in CHECKERS if (i, c) not in done]
    total = 2 * len(mine)
    print('%s lane %d of %d, p=%d, mode %s: %d pieces in this lane, %d already recorded, %d to run' %
          (now(), lane, nl, p, MODE, total, total - len(todo), len(todo)), flush=True)
    path = os.path.join(out, 'lane%d.jsonl' % lane)
    t0 = time.time(); n = 0; cache = (None, None)
    # time left: measured here, search time grows about as (vertex count)^8, so weigh each piece by that
    def size(i):
        keep = G.QR[(G.Bn - G.reps[i]) % p]
        return int((keep & (G.idx >= i)).sum()) if MODE == 'ordered' else int(keep.sum())
    wt = {i: float(max(size(i), 1)) ** 8 for i in sorted({i for i, _ in todo})}
    w_left = sum(wt[i] for i, _ in todo); w_done = 0.0
    for (i, c) in todo:
        if maxp and n >= maxp: break
        a = G.reps[i]
        if cache[0] != i:
            T, M = G.sub(a, i if MODE == 'ordered' else None); buf = graph_text(M); cache = (i, (len(T), buf, hashlib.sha256(buf).hexdigest()))
        nv, buf, sha = cache[1]
        res, o, sec = run_solver(c, k - 2, buf)
        append(path, dict(type='piece', mode=MODE, p=p, k=k, i=i, a=a, n=nv, sha256=sha, checker=c, asked='K_%d' % (k - 2),
                          result=res, out=o, seconds=sec, lane=lane, nlanes=nl))
        n += 1; w_done += wt[i]; w_left -= wt[i]
        left = len(todo) - n
        print('%s lane %d: piece %d of %d done (rep %d, a=%d, %d vertices, %s): %s in %.1f s; %d left in this lane, about %s' %
              (now(), lane, total - left, total, i, a, nv, c, res, sec, left, fmt((time.time() - t0) * w_left / w_done)), flush=True)
        if res != 'NONE':
            print('%s lane %d: ATTENTION rep %d %s gave %s: %s' % (now(), lane, i, c, res, o), flush=True)
    print('%s lane %d: stopped after %d pieces this run (%s); %d pieces of this lane still to run' %
          (now(), lane, n, fmt(time.time() - t0), len(todo) - n), flush=True)
    return 0


def cmd_time(p, k, idxs):
    """Timing test only: runs both checkers on the pieces of the given rep indices, records nothing."""
    G = Paley(p); out = []
    for i in idxs:
        a = G.reps[i]; T, M = G.sub(a, i if MODE == 'ordered' else None); buf = graph_text(M)
        d = dict(p=p, k=k, mode=MODE, i=i, n=len(T))
        for c in CHECKERS:
            res, o, sec = run_solver(c, k - 2, buf); d[c] = res; d[c + '_seconds'] = sec
        out.append(d); print(json.dumps(d), flush=True)
    return out


def check_witness(G, k, vs):
    vs = [int(v) % G.p for v in vs]
    return bool(len(vs) == k and len(set(vs)) == k and all(G.QR[(u - v) % G.p] for u in vs for v in vs if u != v))


def found_witness(out, G, k):
    for f in sorted(glob.glob(os.path.join(out, 'witness*.jsonl'))):
        for r in read_records(f)[0]:
            if r.get('p') == G.p and r.get('k') == k and r.get('result') == 'FOUND' and check_witness(G, k, r.get('vertices', [])):
                return r['vertices']
    return None


def cmd_witness(p, k, out, lane, nl):
    G = Paley(p); R = len(G.reps)
    done = done_keys(out, 'witness*.jsonl', p, k)
    path = os.path.join(out, 'witness%d.jsonl' % lane)
    for i in range(R):
        if i % nl != lane or (i, 'clique') in done: continue
        if found_witness(out, G, k):
            print('%s witness lane %d: a K_%d is on file, stopping' % (now(), lane, k), flush=True); return 0
        a = G.reps[i]; T, M = G.sub(a)
        res, o, sec = run_solver('clique', k - 3, graph_text(M))
        rec = dict(type='witness', p=p, k=k, i=i, a=a, n=len(T), checker='clique', asked='K_%d' % (k - 3), result=res, out=o, seconds=sec, lane=lane)
        if res == 'FOUND':
            vs = [0, 1, a] + [int(T[int(v)]) for v in o.split()[2:2 + k - 3]]
            rec['vertices'] = vs; rec['all_edges_checked'] = check_witness(G, k, vs)
        append(path, rec)
        print('%s witness lane %d: rep %d (a=%d): %s in %.1f s' % (now(), lane, i, a, res, sec), flush=True)
    return 0


def cmd_collect(p, k, out, wfile=None):
    G = Paley(p); R = len(G.reps)
    hdr = [r for r in read_records(os.path.join(out, 'header.jsonl'))[0] if r.get('p') == p and r.get('k') == k and r.get('mode') == MODE]
    header_ok = bool(hdr) and all(r.get('ok') and all(r['automorphism_checks'].values()) for r in hdr) and hdr[-1]['orbit_reps'] == R
    count = {}; recs = {}; cut = 0; modes_bad = 0; files = sorted(glob.glob(os.path.join(out, 'lane*.jsonl')))
    for f in files:
        rs, bad = read_records(f); cut += bad
        for r in rs:
            if r.get('type') != 'piece' or r.get('p') != p or r.get('k') != k: continue
            if r.get('mode') != MODE: modes_bad += 1
            key = (r['i'], r['checker']); count[key] = count.get(key, 0) + 1; recs[key] = r
    missing = [(i, c) for i in range(R) for c in CHECKERS if (i, c) not in count]
    twice = sorted(key for key, n in count.items() if n > 1)
    stray = sorted(key for key in count if not (0 <= key[0] < R and key[1] in CHECKERS))
    notnone = sorted(key for key, r in recs.items() if r['result'] != 'NONE')
    found = sorted(key for key, r in recs.items() if r['result'] == 'FOUND')
    mismatch = []; secs = {c: 0.0 for c in CHECKERS}; nmax = 0
    for i in range(R):                                   # recompute every subproblem from p alone and compare
        got = [recs[(i, c)] for c in CHECKERS if (i, c) in recs]
        if not got: continue
        a = G.reps[i]; T, M = G.sub(a, i if MODE == 'ordered' else None); sha = hashlib.sha256(graph_text(M)).hexdigest(); nmax = max(nmax, len(T))
        for r in got:
            secs[r['checker']] += r.get('seconds', 0)
            if r['a'] != a or r['n'] != len(T) or r['sha256'] != sha or r['asked'] != 'K_%d' % (k - 2): mismatch.append((i, r['checker']))
    wit = None; wsrc = None
    if wfile and os.path.exists(wfile):
        with open(wfile) as f: vs = [int(x) for x in f.read().replace(',', ' ').split()]
        if check_witness(G, k, vs): wit, wsrc = vs, os.path.basename(wfile)
    if wit is None:
        wit = found_witness(out, G, k); wsrc = 'witness*.jsonl' if wit else None
    complete = not missing and not twice and not stray and not mismatch and cut == 0 and modes_bad == 0
    if found: verdict = 'FAIL: a checker reports a K_%d in G_%d (pieces %s): the published value is not reproduced' % (k + 1, p, found[:5])
    elif complete and not notnone and header_ok and wit:
        verdict = 'PASS: c(G_%d) = %d (both checkers, all %d reps, every piece exactly once, mode %s)' % (p, k, R, MODE)
    else:
        verdict = 'INCOMPLETE: %d of %d pieces recorded' % (2 * R - len(missing), 2 * R)
    rec = dict(type='verdict', mode=MODE, records_of_other_mode=modes_bad, p=p, k=k, claim='c(G_%d) = %d, so R(%d,%d) > %d by Shearer 1986 Lemma 1 and Theorem 1' % (p, k, k + 2, k + 2, 2 * p + 2),
               orbit_reps=R, pieces_expected=2 * R, pieces_recorded=2 * R - len(missing), missing=len(missing), missing_first=missing[:6],
               recorded_twice=twice[:10], stray=stray[:10], cut_off_lines=cut, not_NONE=notnone[:10], input_mismatch=mismatch[:10],
               header_ok=header_ok, subproblem_max=nmax, checker_seconds={c: round(v, 1) for c, v in secs.items()},
               K_k_witness=dict(vertices=wit, source=wsrc, all_edges_checked=True) if wit else None,
               lane_files=[os.path.basename(f) for f in files], verdict=verdict)
    append(os.path.join(out, 'verdict.jsonl'), rec)
    print(json.dumps(rec), flush=True)
    print('VERDICT p=%d: %s' % (p, verdict), flush=True)
    return 0 if verdict.startswith('PASS') else 1


if __name__ == '__main__':
    mode, p, k, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    if mode == 'time': cmd_time(p, k, [int(x) for x in out.split(',')]); sys.exit(0)
    os.makedirs(out, exist_ok=True)
    if mode == 'verify': sys.exit(cmd_verify(p, k, out))
    if mode == 'lane': sys.exit(cmd_lane(p, k, out, int(sys.argv[5]), int(sys.argv[6])))
    if mode == 'witness': sys.exit(cmd_witness(p, k, out, int(sys.argv[5]), int(sys.argv[6])))
    if mode == 'collect': sys.exit(cmd_collect(p, k, out, sys.argv[5] if len(sys.argv) > 5 else None))
    sys.exit('unknown mode ' + mode)
