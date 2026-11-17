"""exoo_check.py: check the colourings Geoffrey Exoo sent on 16 November 2026 with both checkers.

For each file (colormat: n lines of n digits, digit = colour of edge ij, diagonal ignored) and each matching of
colours to the k_i given, every colour class is searched on the whole graph, with no symmetry reduction, by
clique.c and by gen0 for a K_k (both must answer NONE).  Controls for every colour: both checkers must FIND a
K_(k-1) in the same graph, and both must FIND a K_k in a copy with one K_k planted (a few edges recoloured).

Usage: python3 exoo_check.py FILE K1,K2,... OUT.jsonl   (environment: CLIQUE and GEN0 = paths to the binaries)
"""
import sys, os, json, time, hashlib, subprocess, itertools
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
from verify_ramsey import load_colormat

def text(A):
    A = A.astype(np.uint8)
    assert (A == A.T).all() and not A.diagonal().any()
    return b'%d\n' % len(A) + b'\n'.join((r + 48).tobytes() for r in A) + b'\n'

def run(exe, k, buf):
    t = time.time(); p = subprocess.run([exe, str(k)], input=buf, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.decode().strip().splitlines()
    return (out[-1] if out else 'ERROR ' + p.stderr.decode()[:200]), round(time.time() - t, 2)

path, ks, outp = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], sys.argv[3]
C = load_colormat(path)
n = len(C); cols = sorted(set(C[np.triu_indices(n, 1)].tolist()))
assert len(cols) == len(ks), (cols, ks)
raw = open(path, 'rb').read()
# which colour is which: the matching that gives every colour clique number < k (tried from networkx-free omegas)
def classes(c): A = (C == c); np.fill_diagonal(A, False); return A
omega_ok = {}
rec = dict(file=os.path.basename(path), n=n, sha256_file=hashlib.sha256(raw).hexdigest(), ks=ks, colours=cols, checks=[])
match = None
for perm in itertools.permutations(ks):
    good = True
    for c, k in zip(cols, perm):
        key = (c, k)
        if key not in omega_ok:
            buf = text(classes(c)); omega_ok[key] = run(os.environ['CLIQUE'], k, buf)[0].startswith('NONE')
        good &= omega_ok[key]
    if good: match = dict(zip(cols, perm)); break
rec['matching'] = {str(c): k for c, k in (match or {}).items()}
ok = match is not None
for c, k in (match or {}).items():
    A = classes(c); buf = text(A)
    r = dict(colour=c, k=k, edges=int(A.sum() // 2), input_sha256=hashlib.sha256(buf).hexdigest())
    for name in ('clique', 'gen0'):
        exe = os.environ[name.upper()]
        r[name], r[name + '_s'] = run(exe, k, buf)
        r[name + '_control_K%d' % (k - 1)] = run(exe, k - 1, buf)[0]
    # corrupted copy: plant K_k on the vertices of a found K_(k-1) plus one more vertex
    found = [int(v) for v in run(os.environ['CLIQUE'], k - 1, buf)[0].split()[2:2 + k - 1]]
    extra = next(v for v in range(n) if v not in found)
    B = A.copy()
    for u, v in itertools.combinations(found + [extra], 2): B[u, v] = B[v, u] = True
    bb = text(B); r['corrupted_copy'] = {nm: run(os.environ[nm.upper()], k, bb)[0].split()[0] for nm in ('clique', 'gen0')}
    r['ok'] = (r['clique'].startswith('NONE') and r['gen0'].startswith('NONE')
               and r['clique_control_K%d' % (k - 1)].startswith('FOUND') and r['gen0_control_K%d' % (k - 1)].startswith('FOUND')
               and r['corrupted_copy'] == {'clique': 'FOUND', 'gen0': 'FOUND'})
    ok &= r['ok']; rec['checks'].append(r)
rec['verdict'] = 'PASS' if ok else 'FAIL'
rec['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
open(outp, 'a').write(json.dumps(rec) + '\n')
print(rec['file'], rec['verdict'], rec['matching'], [(r['colour'], r['clique'], r['gen0']) for r in rec['checks']])
