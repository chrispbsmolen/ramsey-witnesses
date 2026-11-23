"""Check a two-color witness in graph6 for R(k,l) as registration/REGISTRATION_intake.md requires.

usage: python3 intake/check_two_color.py FILE K L OUTDIR
"""
import os, sys, gzip, json, time, random, hashlib, subprocess
import networkx as nx
import pynauty

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, k, l, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
os.makedirs(out, exist_ok=True)
log = open(os.path.join(out, 'checks.jsonl'), 'a')


def record(**kw):
    kw['logged_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    log.write(json.dumps(kw, sort_keys=True) + '\n')
    log.flush()
    print(json.dumps(kw, sort_keys=True), flush=True)


def raw(path):
    b = open(path, 'rb').read()
    return gzip.decompress(b) if path.endswith('.gz') else b


def decode_networkx(data):
    g = nx.from_graph6_bytes(data.strip())
    n = g.number_of_nodes()
    return [[1 if i != j and g.has_edge(i, j) else 0 for j in range(n)] for i in range(n)]


def decode_own(data):
    s = data.strip()
    if s.startswith(b'>>graph6<<'):
        s = s[10:]
    v = [c - 63 for c in s]
    if v[0] < 63:
        n, p = v[0], 1
    elif v[1] < 63:
        n, p = (v[1] << 12) | (v[2] << 6) | v[3], 4
    else:
        raise SystemExit('graph6 with more than 258047 vertices is not handled')
    bits = []
    for x in v[p:]:
        bits.extend((x >> (5 - t)) & 1 for t in range(6))
    a = [[0] * n for _ in range(n)]
    q = 0
    for j in range(1, n):
        for i in range(j):
            a[i][j] = a[j][i] = bits[q]
            q += 1
    return a


def text(a, digit):
    n = len(a)
    return '%d\n' % n + ''.join(''.join('1' if i != j and a[i][j] == digit else '0' for j in range(n)) + '\n'
                                for i in range(n))


def ask(checker, a, digit, size, what):
    t = time.time()
    body = text(a, digit)
    try:
        p = subprocess.run([os.path.join(out, 'bin', checker), str(size)], input=body, capture_output=True, text=True,
                           timeout=3600)
        ans = p.stdout.strip()
    except subprocess.TimeoutExpired:
        ans = 'TIMEOUT after 3600 s'
    record(step=what, checker=checker, color='edges' if digit == 1 else 'non-edges', clique_size=size,
           input_sha256=hashlib.sha256(body.encode()).hexdigest(), answer=ans, seconds=round(time.time() - t, 1))
    return ans


def plant(a, digit, size, seed):
    b = [row[:] for row in a]
    vs = random.Random(seed).sample(range(len(a)), size)
    for x in vs:
        for y in vs:
            if x != y:
                b[x][y] = digit
    return b


os.makedirs(os.path.join(out, 'bin'), exist_ok=True)
for name, path in (('clique', os.path.join(ROOT, 'clique.c')),
                   ('gen0', os.path.join(ROOT, 'phase2/scripts_as_run/build_round2/checker/gen0.c'))):
    subprocess.run(['cc', '-O2', '-o', os.path.join(out, 'bin', name), path], check=True)
    record(step='compile', checker=name, source=os.path.relpath(path, ROOT),
           source_sha256=hashlib.sha256(open(path, 'rb').read()).hexdigest())

data = raw(src)
A, B = decode_networkx(data), decode_own(data)
n = len(A)
record(step='read', file=os.path.basename(src), file_sha256=hashlib.sha256(open(src, 'rb').read()).hexdigest(),
       content_sha256=hashlib.sha256(data).hexdigest(), n=n, edges=sum(map(sum, A)) // 2,
       readers_agree=A == B, reader_for_clique='networkx.from_graph6_bytes', reader_for_gen0='own graph6 decoder')
if A != B:
    raise SystemExit('the two readers disagree')

adj = {i: [j for j in range(n) if A[i][j]] for i in range(n)}
cert = pynauty.certificate(pynauty.Graph(n, adjacency_dict=adj))
record(step='canonical form', tool='pynauty %s certificate' % pynauty.__version__,
       canonical_hash=hashlib.sha256(cert).hexdigest())

ok = True
for checker, M in (('clique', A), ('gen0', B)):
    ok &= ask(checker, M, 1, k, 'witness').startswith('NONE')
    ok &= ask(checker, M, 0, l, 'witness').startswith('NONE')
    ok &= ask(checker, M, 1, k - 1, 'control: smaller clique').startswith('FOUND')
    ok &= ask(checker, M, 0, l - 1, 'control: smaller clique').startswith('FOUND')
    ok &= ask(checker, plant(M, 1, k, 1), 1, k, 'control: planted clique').startswith('FOUND')
    ok &= ask(checker, plant(M, 0, l, 1), 0, l, 'control: planted clique').startswith('FOUND')

tmp = os.path.join(out, 'bin', 'input.g6')
open(tmp, 'wb').write(data)
t = time.time()
p = subprocess.run([sys.executable, os.path.join(ROOT, 'verify_ramsey.py'), 'g6', tmp, '%d,%d' % (k, l)],
                   capture_output=True, text=True)
os.remove(tmp)
record(step='verify_ramsey', answer=p.stdout.strip().split('\n')[-1] if p.stdout.strip() else p.stderr.strip(),
       seconds=round(time.time() - t, 1))
ok &= 'PASS' in p.stdout
record(step='result', all_passed=bool(ok))
print('ALL PASSED' if ok else 'NOT PASSED', flush=True)
