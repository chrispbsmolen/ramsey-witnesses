"""Check one built colouring with both checkers, each in its own process with a time and memory cap.

 1. verify_ramsey.py (byte-identical copy in ../checker): exact clique.c decision for every colour
    class, all colour-to-k matchings tried, circulant shortcut only if circulancy is detected.
 2. crosscheck: the method of repo/crosscheck.py (networkx maximal-clique enumeration, no code shared
    with clique.c), extended from two colours to every colour class: the clique number of each
    colour class is computed and a matching colour -> k with clique number < k is required.

Usage: python3 check.py FORMAT PATH K1,K2,... [--limit SECONDS] [--only verify|cross]
Appends one JSON line to ../logs/checks.jsonl and prints it.
"""
import os, sys, json, subprocess, time, itertools, resource
HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, '..', 'checker')
LOG = os.path.join(HERE, '..', 'logs', 'checks.jsonl')
MEM = 1500 * 1024 * 1024

def limit_mem():
    resource.setrlimit(resource.RLIMIT_AS, (MEM, MEM))

VERIFY = r'''
import sys, json; sys.path.insert(0, sys.argv[1]); import verify_ramsey as V
fmt, path, ks = sys.argv[2], sys.argv[3], [int(x) for x in sys.argv[4].split(',')]
C = V.load(fmt, path, '0' if fmt == 'g6' else '')
print(json.dumps(V.verify(C, ks)), flush=True)
'''
CROSS = r'''
import sys, json, networkx as nx, numpy as np
sys.path.insert(0, sys.argv[1]); import verify_ramsey as V
fmt, path = sys.argv[2], sys.argv[3]
C = V.load(fmt, path, '0' if fmt == 'g6' else '')
for c in sorted(set(C[C >= 0].tolist())):
    G = nx.from_numpy_array((C == c).astype(int))
    w = max(len(q) for q in nx.find_cliques(G))
    print(json.dumps({'colour': int(c), 'omega': w}), flush=True)
'''

def run(code, args, limit):
    t0 = time.time()
    # own process group, so that on timeout the clique.c grandchild is killed too (not left orphaned)
    import signal
    p = subprocess.Popen([sys.executable, '-c', code, CHECKER] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, preexec_fn=lambda: (limit_mem(), os.setsid()))
    try:
        out, err = p.communicate(timeout=limit); err, status = err[-500:], 'done'
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); out, _ = p.communicate()
        err, status = '', 'timeout after %d s' % limit
    return out, err, status, round(time.time() - t0, 1)

def main():
    a = sys.argv[1:]
    limit = 590; only = None
    if '--limit' in a: i = a.index('--limit'); limit = int(a[i + 1]); del a[i:i + 2]
    if '--only' in a: i = a.index('--only'); only = a[i + 1]; del a[i:i + 2]
    fmt, path, ks = a[0], a[1], a[2]
    K = [int(x) for x in ks.split(',')]
    rec = dict(time=time.strftime('%Y-%m-%d %H:%M:%S'), file=os.path.relpath(path, os.path.join(HERE, '..')), ks=K)
    if only in (None, 'verify'):
        out, err, st, sec = run(VERIFY, [fmt, path, ks], limit)
        v = json.loads(out.strip().split('\n')[-1]) if out.strip() and st == 'done' else None
        rec['verify_ramsey'] = dict(status=st, seconds=sec, result=v, stderr=err if v is None else '')
    if only in (None, 'cross'):
        out, err, st, sec = run(CROSS, [fmt, path], limit)
        om = {}
        for line in out.split('\n'):
            if line.strip(): d = json.loads(line); om[d['colour']] = d['omega']
        cols = sorted(om)
        verdict = None
        if st == 'done' and cols:
            ok = any(all(om[cols[i]] < K[perm[i]] for i in range(len(cols)))
                     for perm in itertools.permutations(range(len(K)), len(cols)))
            verdict = 'PASS' if ok else 'FAIL'
        rec['crosscheck'] = dict(status=st, seconds=sec, omega_per_colour=om, verdict=verdict,
                                 stderr=err if verdict is None else '')
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    open(LOG, 'a').write(json.dumps(rec) + '\n')
    print(json.dumps(rec))

if __name__ == '__main__':
    main()
