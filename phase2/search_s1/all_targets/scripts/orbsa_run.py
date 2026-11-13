#!/usr/bin/env python3
"""orbsa_run.py - one restartable annealing leg of orbsa.c on a group ansatz, logged to jsonl.
usage: orbsa_run.py GROUP K1,K2,... SECONDS T SEED STATEPREFIX LOG [--label L] [--pf 0.3] [--reload 60]
If STATEPREFIX.state exists, the leg continues from it (restart). On cost 0 the colouring is expanded to
STATEPREFIX.colormat (one colour digit per entry, '0' on the diagonal (ignored))."""
import sys, os, json, subprocess, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import symlib as L
HERE = os.path.dirname(os.path.abspath(__file__)); BIN = os.path.join(HERE, '..', 'bin', 'orbsa')

ap = argparse.ArgumentParser()
for x in ('group', 'ks'): ap.add_argument(x)
ap.add_argument('seconds', type=float); ap.add_argument('T', type=float); ap.add_argument('seed', type=int)
ap.add_argument('prefix'); ap.add_argument('log')
ap.add_argument('--label', default=''); ap.add_argument('--pf', default='0.3'); ap.add_argument('--reload', default='60')
a = ap.parse_args()
ks = [int(x) for x in a.ks.split(',')]
n, gens, desc = L.group_perms(a.group)
orb, O = L.edge_orbits(n, gens); reps = L.vertex_orbit_reps(n, gens)
inp = a.prefix + '.in'
if not os.path.exists(inp):
    with open(inp, 'w') as f:
        f.write(f'{n} {len(ks)} {len(O)} {len(reps)}\n' + ' '.join(map(str, ks)) + '\n' + ' '.join(map(str, reps)) + '\n')
        f.write(' '.join(str(orb[(x, y)]) for x in range(n) for y in range(x + 1, n)) + '\n')
cmd = [BIN, inp, str(a.seed), str(a.seconds), str(a.T), a.prefix, '-f', a.pf, '-r', a.reload]
resumed = os.path.exists(a.prefix + '.state')
if resumed: cmd += ['-i', a.prefix + '.state']
t0 = time.time()
p = subprocess.run(cmd, capture_output=True, text=True)
res = json.loads(p.stdout.strip().splitlines()[-1])
rec = {'method': 'orbsa (orbit annealing, exact clique count through orbit representatives)', 'label': a.label,
       'group': a.group, 'group_desc': desc, 'ks': a.ks, 'n': n, 'edge_orbits': len(O), 'T': a.T, 'seed': a.seed,
       'pf': float(a.pf), 'reload': float(a.reload), 'resumed_from_state': resumed, 'seconds_budget': a.seconds,
       'wall_seconds': round(time.time() - t0, 1), **res, 'result': 'FOUND' if res['best_score'] == 0 else 'NOT_FOUND'}
if res['best_score'] == 0:
    col = [int(x) for x in open(a.prefix + '.found').read().split()]
    C = L.expand(n, orb, col); L.write_colormat(C, a.prefix + '.colormat')
    rec['file'] = a.prefix + '.colormat'; rec['sha256'] = L.sha256_file(a.prefix + '.colormat')
L.log_run(a.log, rec); print(json.dumps(rec))
