"""Exact check of the large AlphaEvolve Ramsey witnesses, for a native run on a separate machine (a Mac).
For each witness G on n vertices claimed to show R(k,l) > n:
  (a) G has no clique of size k        (scripts: clique k)
  (b) G has no independent set of size l (clique l --complement)
Each half is a separate process; up to six run in parallel. No numpy needed.
Results append to hard_results.jsonl as each half finishes; rerunning skips finished halves.
Usage: copy this script, clique.c and the witness files (renamed Rk_l_geB.txt) into one folder, then run
        python3 run_hard.py   there (on macOS, under caffeinate -dims to keep the machine awake).
"""
import os, re, json, time, hashlib, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
if not os.path.exists('clique') or os.path.getmtime('clique') < os.path.getmtime('clique.c'):
    subprocess.run(['cc', '-O2', '-o', 'clique', 'clique.c'], check=True)
OUT = 'hard_results.jsonl'
done = set()
if os.path.exists(OUT):
    for l in open(OUT): r = json.loads(l); done.add((r['file'], r['half']))

def load(path):
    nums = re.findall(r'[01]', re.sub(r'[^\[\]01\s]', '', open(path).read()))
    n = int(round(len(nums) ** 0.5)); assert n * n == len(nums), 'not square'
    A = [nums[i * n:(i + 1) * n] for i in range(n)]
    for i in range(n):
        assert A[i][i] == '0'
        for j in range(i): assert A[i][j] == A[j][i], 'not symmetric'
    return n, A

jobs = []
for f in sorted(os.listdir('.')):
    m = re.match(r'R(\d+)_(\d+)_ge(\d+)\.txt$', f)
    if not m: continue
    k, l = int(m.group(1)), int(m.group(2))
    n, A = load(f)
    buf = '%d\n' % n + '\n'.join(''.join(r) for r in A) + '\n'
    sha = hashlib.sha256(open(f, 'rb').read()).hexdigest()
    for half, size, flag in (('no_clique', k, []), ('no_independent_set', l, ['--complement'])):
        if (f, half) not in done: jobs.append((f, n, k, l, half, size, flag, buf, sha))

def run(j):
    f, n, k, l, half, size, flag, buf, sha = j
    t0 = time.time()
    p = subprocess.run(['./clique', str(size)] + flag, input=buf, capture_output=True, text=True)
    rec = dict(file=f, sha256=sha, n=n, k=k, l=l, half=half, size=size, output=p.stdout.strip(), nodes=p.stderr.strip(),
               seconds=round(time.time() - t0, 1), result='OK' if p.stdout.startswith('NONE') else 'FOUND' if p.stdout.startswith('FOUND') else 'ERROR')
    with open(OUT, 'a') as o: o.write(json.dumps(rec) + '\n')
    print(time.strftime('%H:%M'), f, half, rec['result'], '%.0f s' % rec['seconds'], flush=True)

print('halves to run:', len(jobs), flush=True)
with ThreadPoolExecutor(6) as ex: list(ex.map(run, jobs))
print('all done; a witness is VERIFIED when both its halves say OK', flush=True)
