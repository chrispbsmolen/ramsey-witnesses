#!/usr/bin/env python3
"""edgesa_run.py - one restartable leg of edgesa.c (annealing on the whole edge colouring), logged to jsonl.
usage: edgesa_run.py N K1,K2,.. SECONDS T SEED PREFIX LOG [--start colormat] [--label L] [--pf 0.5]
A leg continues from PREFIX.colormat when it exists (restart), else from --start (padded with random new
vertices) or random."""
import sys, os, json, subprocess, time, argparse, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); BIN = os.path.join(HERE, '..', 'bin', 'edgesa')
sys.path.insert(0, HERE); import symlib as L
ap = argparse.ArgumentParser(); ap.add_argument('n', type=int); ap.add_argument('ks'); ap.add_argument('seconds', type=float)
ap.add_argument('T', type=float); ap.add_argument('seed', type=int); ap.add_argument('prefix'); ap.add_argument('log')
ap.add_argument('--start', default=None); ap.add_argument('--label', default=''); ap.add_argument('--pf', default='0.5')
a = ap.parse_args()
resumed = os.path.exists(a.prefix + '.colormat')
init = a.prefix + '.colormat' if resumed else a.start
if resumed:
    os.replace(a.prefix + '.colormat', a.prefix + '.prev.colormat'); init = a.prefix + '.prev.colormat'
cmd = [BIN, str(a.n), a.ks, str(a.seed), str(a.seconds), str(a.T), a.prefix, '-f', a.pf] + (['-i', init] if init else [])
t0 = time.time(); p = subprocess.run(cmd, capture_output=True, text=True)
res = json.loads(p.stdout.strip().splitlines()[-1])
rec = {'method': 'edgesa (annealing on the whole colouring, exact clique-count deltas)', 'label': a.label, 'n': a.n, 'ks': a.ks,
       'T': a.T, 'seed': a.seed, 'pf': float(a.pf), 'start': init, 'resumed_from_state': resumed, 'seconds_budget': a.seconds,
       'wall_seconds': round(time.time() - t0, 1), **res, 'result': 'FOUND' if res['best_score'] == 0 else 'NOT_FOUND'}
if res['best_score'] == 0:
    rec['file'] = a.prefix + '.colormat'; rec['sha256'] = L.sha256_file(rec['file'])
L.log_run(a.log, rec); print(json.dumps(rec)); sys.exit(0 if res['best_score'] == 0 else 3)
