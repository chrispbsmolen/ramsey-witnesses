"""The computed part that Rowley AJC 81(2) (2021) Theorem 3.2 (statement p.248, proof pp.248-250) leaves for a row:
for each remaining colour s of U (s != template colour q), the clique number of W in colour s is at most that of the
subgraph of W induced by the first Q(m-2) edge-lengths.  The proof (p.249) bounds the largest length of a K_k in
colour s by (k_s - 1)(m-2); here the window is taken as M = (k-1)(m-2), which is at least Q(m-2) under either reading
of Q (max clique number of U, or max k_s - 1; the U colours are checked to have clique number <= k-1 in inputs.jsonl).
Window = vertices 0..M of W (all edge-lengths 1..M), read from the row's own file (SHA-256 pinned).
Modes (one solver process per call of solve(); each call of this script is run under a 600 s cap):
  full        : the window graph of colour s, clique of k vertices, no reduction (small windows only);
  whole       : the neighbourhood S of vertex 0 in colour s inside the window, clique of k-1 vertices.  Valid by the
                translation lemma used in the proof (p.248, after Giraud): a clique {a_0<...<a_t} in a linear colouring
                shifts to {0, a_1-a_0, ...}, which stays inside 0..M;
  split:A:B   : exact partition of 'whole' by the smallest vertex v = S[i] (A <= i < B) of the (k-1)-clique: for each v,
                the set T_v = {u in S : u > v, c(u - v) = s}, clique of k-2 vertices.  A call covers the indices it
                records in 'range' (it stops when its time budget runs out); the union of the recorded ranges must
                cover 0..|S|-1 exactly (summarise.py checks this);
  linear0     : linear0.c on the window as a linear colouring of K_(M+1) (it uses the same translation lemma);
  control     : 'whole' asked for a clique of k-2 vertices (a K_(k-1) in colour s); FOUND is expected.
Usage: python3 window_check.py BUILT_DIR CELL COLOUR CHECKER MODE TIMEOUT    Appends to logs/windows.jsonl."""
import sys, os, subprocess, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L
import r6common as C

built, cell, s, chk, mode, to = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6])
fname, pin, col, m, k = C.ROW[cell]
path = os.path.join(built, fname)
sha = L.sha256_file(path)
N, c = C.read_lengths(path)
M = (k - 1) * (m - 2)
rec = dict(cell=cell, file=fname, sha256=sha, sha_match=(sha == pin), N=int(N), m=m, k=k, colour=s,
           window_lengths=M, window_vertices=M + 1, checker=chk, mode=mode)
cw = c[:M + 1].astype(np.int16)
S = np.flatnonzero(cw == s); S = S[S > 0]
rec['S_size'] = int(len(S))
rec['window_text_sha256'] = L.sha256_bytes(('%d\n' % (M + 1)).encode() + b' '.join(b'%d' % x for x in cw[1:].tolist()) + b'\n')


def sub(idx):
    idx = idx.astype(np.int32); D = np.abs(idx[:, None] - idx[None, :])
    return (cw[D] == s) & (D > 0)


if mode == 'full':
    A = sub(np.arange(M + 1)); f, o, sec = L.solve(chk, A, k, to)
    rec.update(target=k, found=f, out=o[:160], seconds=sec)
elif mode in ('whole', 'control'):
    A = sub(S); kk = k - 1 if mode == 'whole' else k - 2
    rec['graph_sha256'] = L.sha256_bytes(L.graph_text(A))
    f, o, sec = L.solve(chk, A, kk, to); rec.update(target=kk, found=f, out=o[:160], seconds=sec)
elif mode.startswith('split:'):
    # TIMEOUT is the budget of this call: subproblems are started while time remains, each with the remaining time as
    # its own limit; the range actually completed, [A, end), is recorded, and the next call starts at end.
    a, b = (int(x) for x in mode.split(':')[1:]); b = min(b, len(S))
    rec.update(requested_range=[a, b], target=k - 2)
    t0 = time.time(); n_sub = 0; found = False; undecided = []; end = a; mx = 0.0
    for i in range(a, b):
        left = to - (time.time() - t0)
        if left < 5: break
        v = S[i]; T = S[(S > v) & (cw[np.abs(S - v)] == s)]
        if len(T) >= k - 2:
            f, o, sec = L.solve(chk, sub(T), k - 2, int(left)); mx = max(mx, sec)
            if f is True: found = True; rec['witness'] = dict(v=int(v), out=o[:200]); end = i + 1; break
            if f is None:
                if i == a: undecided.append(dict(v=int(v), T=int(len(T)), out=o[:60]))
                break
        n_sub += 1; end = i + 1
    rec.update(range=[a, end], subproblems_completed=n_sub, undecided=undecided, seconds=round(time.time() - t0, 1),
               max_sub_seconds=mx, out='range %d..%d done' % (a, end))
    rec['found'] = True if found else (None if (undecided or end == a) else False)
elif mode == 'linear0':
    with tempfile.NamedTemporaryFile('w', suffix='.lengths', delete=False, dir=os.environ.get('TMPDIR')) as t:
        t.write('%d\n%s\n' % (M + 1, ' '.join(str(int(x)) for x in cw[1:]))); tp = t.name
    t0 = time.time()
    try:
        p = subprocess.run([os.path.join(L.TOOLS, 'linear0'), tp, str(s), str(k)], capture_output=True, text=True, timeout=to)
        o = p.stdout.strip()
        f = True if o.startswith('FOUND') else (False if o.startswith('NONE') else None)
    except subprocess.TimeoutExpired:
        o, f = 'TIMEOUT %d s' % to, None
    os.unlink(tp)
    rec.update(target=k, found=f, out=o[:200], seconds=round(time.time() - t0, 1))
L.log('windows.jsonl', rec)
