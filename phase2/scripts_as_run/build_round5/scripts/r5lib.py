"""build_round5 helpers: run the two exact clique checkers on an explicit 0/1 graph and log the result.

  checker 1 = clique.c (repo copy, sha256 137a1002...), called without --sym on the graph it is given;
  checker 2 = gen0.c (build_round2 copy, sha256 d82e1855..., independent of clique.c).
Any symmetry reduction is done by the caller, after the automorphisms are verified on the object's own matrix;
both checkers then receive exactly the same reduced graph.  Solver binaries are taken from R5_TOOLS (default:
../tools next to this folder).  Every record goes to logs/<name>.jsonl with the input SHA-256."""
import os, sys, json, time, hashlib, subprocess, gzip
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = os.environ.get('R5_TOOLS', os.path.join(ROOT, 'tools'))
LOGS = os.environ.get('R5_LOGS', os.path.join(ROOT, 'logs'))
BIN = {'clique': os.path.join(TOOLS, os.environ.get('R5_CLIQUE', 'clique')),
       'gen0': os.path.join(TOOLS, os.environ.get('R5_GEN0', 'gen0'))}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def log(name, rec):
    os.makedirs(LOGS, exist_ok=True)
    rec = dict(rec); rec['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(os.path.join(LOGS, name), 'a') as f: f.write(json.dumps(rec) + '\n')
    print(json.dumps(rec), flush=True)
    return rec


def graph_text(A):
    A = np.asarray(A, dtype=bool)
    assert A.shape[0] == A.shape[1] and (A == A.T).all() and not A.diagonal().any()
    return b'%d\n' % len(A) + b'\n'.join((r.astype(np.uint8) + 48).tobytes() for r in A) + b'\n'


def solve(checker, A, k, timeout=None):
    """Does graph A contain a clique of k vertices?  Returns (found: bool or None, output line, seconds).
    None = no verdict (timeout or error)."""
    if k <= 1: return (len(A) >= k), 'trivial', 0.0
    buf = graph_text(A)
    t = time.time()
    try:
        p = subprocess.run([BIN[checker], str(k)], input=buf, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, 'TIMEOUT %s s' % timeout, round(time.time() - t, 1)
    out = p.stdout.decode().strip()
    sec = round(time.time() - t, 1)
    if out.startswith('FOUND'): return True, out[:200], sec
    if out.startswith('NONE'): return False, out[:200], sec
    return None, ('ERROR %s %s' % (out, p.stderr.decode()[-200:]))[:300], sec


# ---------------------------------------------------------------- graph6 (own reader/writer, no networkx)
def g6_decode(line):
    s = line.strip()
    if isinstance(s, bytes): s = s.decode()
    if s.startswith('>>graph6<<'): s = s[10:]
    d = [ord(c) - 63 for c in s]
    if d[0] < 63: n, i = d[0], 1
    elif d[1] < 63: n, i = (d[1] << 12) | (d[2] << 6) | d[3], 4
    else: n, i = sum(d[2 + j] << (6 * (5 - j)) for j in range(6)), 8
    bits = np.unpackbits(np.array(d[i:], dtype=np.uint8)[:, None], axis=1)[:, 2:].ravel()
    A = np.zeros((n, n), dtype=bool)
    iu = np.triu_indices(n, 1)
    # graph6 order: for j = 1..n-1, for i = 0..j-1 (column-wise upper triangle)
    jj, ii = np.meshgrid(np.arange(n), np.arange(n))
    mask = ii < jj
    order_i = ii.T[mask.T]; order_j = jj.T[mask.T]
    m = n * (n - 1) // 2
    b = bits[:m].astype(bool)
    A[order_i, order_j] = b; A[order_j, order_i] = b
    return A


def g6_encode(A):
    A = np.asarray(A, dtype=bool); n = len(A)
    if n < 63: head = bytes([n + 63])
    elif n < 258048: head = bytes([126, 63 + (n >> 12 & 63), 63 + (n >> 6 & 63), 63 + (n & 63)])
    else: head = bytes([126, 126] + [63 + (n >> (6 * (5 - j)) & 63) for j in range(6)])
    jj, ii = np.meshgrid(np.arange(n), np.arange(n))
    mask = ii < jj
    bits = A[ii.T[mask.T], jj.T[mask.T]].astype(np.uint8)
    pad = (-len(bits)) % 6
    bits = np.concatenate([bits, np.zeros(pad, dtype=np.uint8)]).reshape(-1, 6)
    vals = (bits * np.array([32, 16, 8, 4, 2, 1], dtype=np.uint8)).sum(axis=1) + 63
    return head + vals.astype(np.uint8).tobytes() + b'\n'


def load_g6(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rb') as f: line = f.readline()
    return g6_decode(line)


def circulant_adj(n, D):
    S = np.zeros(n, dtype=bool)
    for d in D: S[d % n] = True; S[(-d) % n] = True
    S[0] = False
    idx = (np.arange(n)[None, :] - np.arange(n)[:, None]) % n
    return S[idx]


def is_circulant(A):
    n = len(A); idx = (np.arange(n)[None, :] - np.arange(n)[:, None]) % n
    return bool((A == A[0][idx]).all())
