"""Run the repository's checker (verify_ramsey.py with clique.c) on every phase-2 witness file.

For each row of phase2/witnesses/manifest.csv: check the file's SHA-256, load it, check the number of
vertices, and run verify_ramsey.verify with a time limit per clique search.  Results go to
phase2/results/repo_check.jsonl (one JSON record per file) and a readable summary to
phase2/results/repo_check.txt.  Run from the repository root:

    python3 phase2/check_phase2.py [--limit SECONDS] [--max-n N] [--only CELL ...]

Formats: g6 and colormat use the loaders of verify_ramsey.py (both read .gz).  'lengths' is a linear
colouring given by its length vector: first line N, second line the colours of the edge lengths
1..N-1, so that edge {i, j} has colour c[|i - j|].  It is turned into a colour matrix here and then
checked by the same verify() as every other file.  Files with more than --max-n vertices are not
loaded (the checker builds an n x n matrix); their checks are listed in phase2/CHECKS.md.

This is a light, uniform re-check.  A record "NOT_COMPLETED" means the time limit was reached, not
that anything failed.  The checks the status labels rest on are the ones in phase2/CHECKS.md.
"""
import os, sys, csv, json, gzip, time, hashlib, platform, argparse, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0, ROOT)
import numpy as np
import verify_ramsey as V


def load_lengths(path):
    with gzip.open(path, 'rt') if path.endswith('.gz') else open(path) as f:
        n = int(f.readline().split()[0])
        c = [int(x) for x in f.read().split()]
    if len(c) != n - 1: raise ValueError('length vector has %d entries, expected %d' % (len(c), n - 1))
    c = np.array([-1] + c, dtype=np.int64)
    idx = np.abs(np.arange(n)[None, :] - np.arange(n)[:, None])
    C = c[idx]; np.fill_diagonal(C, -1)
    return V._renumber(C)


def n_of(fmt, path):
    if fmt == 'lengths':
        with gzip.open(path, 'rt') as f: return int(f.readline().split()[0])
    if fmt == 'g6':
        line = V.g6_lines(path)[0]
        b = line[0] - 63
        return b if b < 63 else (line[1] - 63) * 4096 + (line[2] - 63) * 64 + (line[3] - 63)
    with gzip.open(path, 'rt') if path.endswith('.gz') else open(path) as f:
        return sum(1 for l in f if l.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=float, default=60.0, help='seconds per clique search')
    ap.add_argument('--max-n', type=int, default=6000)
    ap.add_argument('--only', nargs='*')
    a = ap.parse_args()
    V.ensure_solver()
    os.makedirs('phase2/results', exist_ok=True)
    rows = list(csv.DictReader(open('phase2/witnesses/manifest.csv')))
    if a.only: rows = [r for r in rows if r['cell'] in a.only]
    machine = '%s %s, %s, %d cores' % (platform.system(), platform.machine(), platform.python_implementation() + ' ' + platform.python_version(), os.cpu_count() or 0)
    out = []
    for r in rows:
        path, fmt, ks = r['file'], r['format'], [int(x) for x in r['cell'].split(',')]
        rec = dict(cell=r['cell'], file=path, format=fmt, label=r['label'], date=time.strftime('%Y-%m-%d %H:%M:%S'), machine=machine,
                   verify_ramsey=V.sha256_file('verify_ramsey.py')[:16], clique_c=V.sha256_file('clique.c')[:16], limit_s=a.limit)
        h = V.sha256_file(path); rec['sha256'] = h; rec['sha256_ok'] = (h == r['sha256'])
        if not rec['sha256_ok']:
            rec['verdict'] = 'HASH_MISMATCH'; out.append(rec); print(json.dumps(rec), flush=True); continue
        n = n_of(fmt, path); rec['n'] = n; rec['n_ok'] = (n == int(r['n']))
        if n > a.max_n:
            rec['verdict'] = 'NOT_RUN_SIZE'; rec['note'] = 'more than %d vertices: not loaded by the in-memory checker; see phase2/CHECKS.md' % a.max_n
            out.append(rec); print(json.dumps(rec), flush=True); continue
        t0 = time.time()
        try:
            C = load_lengths(path) if fmt == 'lengths' else V.load(fmt, path, '0' if fmt == 'g6' else '')
            res = V.verify(C, ks, timeout=a.limit)
            rec.update(verdict=res['verdict'], circulant=bool(res.get('circulant', False)), assignment=res.get('assignment'), seconds=res.get('seconds'))
            if res['verdict'] != 'PASS': rec['detail'] = res.get('note')
        except subprocess.TimeoutExpired:
            rec.update(verdict='NOT_COMPLETED', seconds=round(time.time() - t0, 1), note='a clique search reached the %g s limit' % a.limit)
        except MemoryError:
            rec.update(verdict='NOT_RUN_SIZE', note='out of memory')
        out.append(rec); print(json.dumps(rec), flush=True)
    with open('phase2/results/repo_check.jsonl', 'w') as f:
        for rec in out: f.write(json.dumps(rec) + '\n')
    cnt = {}
    for rec in out: cnt[rec['verdict']] = cnt.get(rec['verdict'], 0) + 1
    lines = ['Repository checker on the phase-2 witness files (%s, limit %g s per clique search, max n %d)' % (machine, a.limit, a.max_n),
             'verify_ramsey.py %s, clique.c %s' % (out[0]['verify_ramsey'], out[0]['clique_c']) if out else '', '']
    lines += ['%-22s %-34s %7s %-14s %8s  %s' % ('cell', 'file', 'n', 'verdict', 'seconds', 'label')]
    for rec in out:
        lines.append('%-22s %-34s %7s %-14s %8s  %s' % (rec['cell'], os.path.basename(rec['file']), rec.get('n', ''), rec['verdict'], rec.get('seconds', ''), rec['label']))
    lines += ['', 'totals: ' + ', '.join('%s %d' % kv for kv in sorted(cnt.items())), 'sha256 all match: %s' % all(r['sha256_ok'] for r in out)]
    open('phase2/results/repo_check.txt', 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[-2:]))


if __name__ == '__main__':
    main()
