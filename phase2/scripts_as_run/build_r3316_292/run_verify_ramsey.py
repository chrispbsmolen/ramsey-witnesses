#!/usr/bin/env python3
"""run_verify_ramsey.py - call the repository's verify_ramsey.verify (unchanged copy in ../tools) on a file, with the
clique binary taken from --bin (compiled from ../tools/clique.c).  No symmetry (the colouring is not circulant;
verify() tests that itself).  usage: run_verify_ramsey.py FORMAT PATH K1,K2,.. --bin DIR [--timeout S]"""
import sys, os, json, argparse, hashlib
sys.dont_write_bytecode = True
ap = argparse.ArgumentParser(); ap.add_argument('fmt'); ap.add_argument('path'); ap.add_argument('ks')
ap.add_argument('--bin', required=True); ap.add_argument('--timeout', type=float, default=560)
a = ap.parse_args()
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import verify_ramsey as V
V.CLIQUE = os.path.join(a.bin, 'clique')
V.ensure_solver = lambda: None
C = V.load(a.fmt, a.path, '')
try:
    res = V.verify(C, [int(x) for x in a.ks.split(',')], timeout=a.timeout)
except Exception as e:
    res = {'verdict': 'NOT COMPLETED', 'error': type(e).__name__, 'timeout_s': a.timeout}
res['file_sha256'] = hashlib.sha256(open(a.path, 'rb').read()).hexdigest()
res['verify_ramsey_py_sha256'] = hashlib.sha256(open(V.__file__, 'rb').read()).hexdigest()
print(json.dumps(res, sort_keys=True))
