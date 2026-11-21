#!/usr/bin/env python3
"""whole_class.py - one checker, one colour class, whole graph, no reduction, as its own process: writes the 0/1
matrix of the class of the given digit and asks the checker for a K_k.  Appends one JSON line to the log (file and
class-text SHA-256, answer, checker stderr, seconds).
usage: whole_class.py COLORMAT DIGIT K CHECKER(clique|gen0) LOG --bin DIR [--timeout S]"""
import sys, os, json, time, subprocess, hashlib, argparse
ap = argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('digit'); ap.add_argument('k'); ap.add_argument('checker')
ap.add_argument('log'); ap.add_argument('--bin', required=True); ap.add_argument('--timeout', type=float, default=570)
a = ap.parse_args()
rows = [l.strip() for l in open(a.path) if l.strip()]; n = len(rows)
txt = '%d\n' % n + ''.join(''.join('1' if (i != j and rows[i][j] == a.digit) else '0' for j in range(n)) + '\n' for i in range(n))
t = time.time()
try:
    p = subprocess.run([os.path.join(a.bin, a.checker), a.k], input=txt, capture_output=True, text=True, timeout=a.timeout)
    ans, err = p.stdout.strip(), p.stderr.strip()
except subprocess.TimeoutExpired:
    ans, err = 'TIMEOUT after %d s' % a.timeout, ''
rec = {'file': os.path.basename(a.path), 'file_sha256': hashlib.sha256(open(a.path, 'rb').read()).hexdigest(), 'n': n,
       'colour_digit': a.digit, 'k': int(a.k), 'checker': a.checker, 'reduction': 'none (whole colour class, no symmetry)',
       'class_text_sha256': hashlib.sha256(txt.encode()).hexdigest(), 'answer': ans, 'stderr': err,
       'seconds': round(time.time() - t, 1), 'logged_at': time.strftime('%Y-%m-%dT%H:%M:%S%z')}
open(a.log, 'a').write(json.dumps(rec, sort_keys=True) + '\n'); print(json.dumps(rec, sort_keys=True))
