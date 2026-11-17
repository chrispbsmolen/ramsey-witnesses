"""kuz_check.py: read the colourings that Kuznetsov's search wrote to a sym file and check the largest ones with
both checkers (clique.c and gen0).

A sym line is: ORDER <tab> six hexadecimal 64-bit words.  The words are a bit mask over the distances 1..ORDER-1
(bit d-1 = distance d).  The colouring of K_ORDER is: edge {i, j} has colour A if bit |i-j| - 1 is set, else colour B.
The search only writes masks with bit(d-1) = bit(ORDER-d-1), so the colouring is cyclic (circulant on Z_ORDER); this
script checks that on the mask and again, entry by entry, on the matrix.

Which colour is the K_KA-free one is not assumed: both assignments are tried and the result says which one holds.
For a circulant, x -> x + 1 is an automorphism (verified on the matrix), so a monochromatic K_s exists iff one
contains vertex 0 (Amendment 1).  Each checker is therefore asked for K_(s-1) in the graph induced on the
colour-neighbours of vertex 0; both checkers get byte-identical input.  With --full the whole graph is searched too
(no reduction; can be slow).  Controls: each checker must FIND a K_(s-2) in the same reduced graph when the row's
bound is tight there (reported, not required), and must FIND a clique in a corrupted copy (one K_(s-1) planted).

Usage: python3 kuz_check.py SYMFILE KA KB MINORDER OUTDIR [--full] [--max N]
  checks every distinct colouring of the largest order present that is >= MINORDER (at most N, default 3), writes
  each as OUTDIR/R<KA>_<KB>_n<ORDER>_cyclic_<j>.circ ("ORDER:d1,d2,..." = the distances of colour A) and appends one
  JSON line per colouring to OUTDIR/kuz_check.jsonl.  Prints "FIND CHECKED: PASS ..." or "... FAIL ...".
Solver binaries: environment W9_CLIQUE and W9_GEN0."""
import sys, os, json, time, hashlib, subprocess
import numpy as np


def read_sym(path):
    out = []
    if not os.path.exists(path): return out
    with open(path) as f:
        for line in f:
            tok = line.split()
            if len(tok) != 7: continue                       # a cut-off line is skipped
            try: n = int(tok[0]); w = [int(x, 16) for x in tok[1:]]
            except ValueError: continue
            if n < 2 or n > 384: continue
            mask = 0
            for i, x in enumerate(w): mask |= x << (64 * i)
            out.append((n, mask))
    return out


def graph_text(A):
    assert A.shape[0] == A.shape[1] and (A == A.T).all() and not A.diagonal().any()
    return b'%d\n' % len(A) + b'\n'.join((r.astype(np.uint8) + 48).tobytes() for r in A) + b'\n'


def solve(checker, k, buf, timeout=None):
    exe = os.environ['W9_' + checker.upper()]
    t = time.time()
    try: p = subprocess.run([exe, str(k)], input=buf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired: return 'TIMEOUT', 'timeout %s s' % timeout, round(time.time() - t, 1)
    o = p.stdout.decode(errors='replace').strip()
    res = 'NONE' if o.startswith('NONE') else ('FOUND' if o.startswith('FOUND') else 'ERROR')
    return res, o[:200], round(time.time() - t, 1)


def check(n, mask, ka, kb, full, timeout):
    bits = np.array([(mask >> (d - 1)) & 1 for d in range(1, n)], dtype=bool)      # bits[d-1] = distance d in colour A
    rec = dict(n=n, mask_hex='%x' % mask, extra_bits_above_order=bool(mask >> (n - 1)))
    rec['mask_symmetric'] = bool((bits == bits[::-1]).all())
    S = np.zeros(n, dtype=bool); S[1:] = bits
    idx = (np.arange(n)[None, :] - np.arange(n)[:, None]) % n
    A = S[np.abs(np.arange(n)[None, :] - np.arange(n)[:, None])]                   # the colouring as the search defines it
    np.fill_diagonal(A, False)
    Bm = ~A; np.fill_diagonal(Bm, False)
    rec['circulant_on_matrix'] = bool((A == A[0][idx]).all()) and bool((A == A.T).all())
    rec['distances_colour_A'] = [int(d) for d in range(1, n // 2 + 1) if S[d]]
    rec['degree_A'] = int(A[0].sum()); rec['degree_B'] = int(Bm[0].sum())
    results = {}
    def half(M, s, name):
        V = np.flatnonzero(M[0]); sub = M[np.ix_(V, V)]; buf = graph_text(sub)
        d = dict(asked='K_%d through vertex 0 (K_%d on its %d neighbours)' % (s, s - 1, len(V)), input_sha256=hashlib.sha256(buf).hexdigest())
        for c in ('clique', 'gen0'):
            r, o, sec = solve(c, s - 1, buf, timeout); d[c] = r; d[c + '_out'] = o; d[c + '_seconds'] = sec
            r2, o2, sec2 = solve(c, s - 2, buf, timeout); d[c + '_control_K_%d' % (s - 1)] = r2
        if full:
            fb = graph_text(M)
            for c in ('clique', 'gen0'):
                r, o, sec = solve(c, s, fb, timeout); d[c + '_full'] = r; d[c + '_full_seconds'] = sec
        d['ok'] = d['clique'] == 'NONE' and d['gen0'] == 'NONE' and (not full or (d['clique_full'] == 'NONE' and d['gen0_full'] == 'NONE'))
        results[name] = d
        return d['ok']
    verdict = None
    if rec['mask_symmetric'] and rec['circulant_on_matrix']:
        for (sa, sb, label) in ((ka, kb, 'A=%d,B=%d' % (ka, kb)), (kb, ka, 'A=%d,B=%d' % (kb, ka))):
            if ka == kb and label in results.get('tried', []): continue
            okA = half(A, sa, 'colour A no K_%d' % sa)
            okB = okA and half(Bm, sb, 'colour B no K_%d' % sb)
            if okA and okB: verdict = label; break
    rec['halves'] = results
    # corrupted copy: plant a clique of ka vertices in colour A on vertices 0..ka-1; both checkers must find it (full graph)
    C = A.copy(); C[np.ix_(range(ka), range(ka))] = True; np.fill_diagonal(C, False)
    cb = graph_text(C)
    rec['corrupted_copy_control'] = {c: solve(c, ka, cb, timeout)[0] for c in ('clique', 'gen0')}
    rec['controls_ok'] = all(v == 'FOUND' for v in rec['corrupted_copy_control'].values())
    rec['valid_as'] = verdict
    rec['verdict'] = 'PASS' if (verdict and rec['controls_ok']) else 'FAIL'
    return rec


def main():
    a = sys.argv[1:]
    full = '--full' in a; a = [x for x in a if x != '--full']
    mx = 3
    if '--max' in a: i = a.index('--max'); mx = int(a[i + 1]); del a[i:i + 2]
    path, ka, kb, minorder, out = a[0], int(a[1]), int(a[2]), int(a[3]), a[4]
    sym = read_sym(path)
    orders = [n for n, _ in sym]
    best = max(orders) if orders else 0
    print('sym file %s: %d colourings, largest order %d (asked for >= %d)' % (path, len(sym), best, minorder), flush=True)
    if best < minorder:
        print('NO FIND: no colouring of order >= %d in the file' % minorder); return 2
    os.makedirs(out, exist_ok=True)
    masks = sorted({m for n, m in sym if n == best})[:mx]
    allok = True
    for j, m in enumerate(masks):
        rec = check(best, m, ka, kb, full, None)
        rec.update(sym_file=os.path.basename(path), ka=ka, kb=kb, time=time.strftime('%Y-%m-%d %H:%M:%S'))
        name = 'R%d_%d_n%d_cyclic_%d.circ' % (ka, kb, best, j)
        fn = os.path.join(out, name)
        text = '%d:%s\n' % (best, ','.join(str(d) for d in rec['distances_colour_A']))
        if not os.path.exists(fn):
            with open(fn, 'w') as f: f.write(text)
        rec['circ_file'] = name; rec['circ_sha256'] = hashlib.sha256(text.encode()).hexdigest()
        with open(os.path.join(out, 'kuz_check.jsonl'), 'a') as f: f.write(json.dumps(rec) + '\n')
        print(json.dumps(rec), flush=True)
        print('FIND CHECKED: %s  cyclic (%d,%d;%d) colouring %d of %d, valid as %s, file %s' %
              (rec['verdict'], ka, kb, best, j + 1, len(masks), rec['valid_as'], name), flush=True)
        allok = allok and rec['verdict'] == 'PASS'
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main())
