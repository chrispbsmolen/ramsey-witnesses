"""One colour, one forbidden clique size, through the unchanged verify_ramsey.has_clique (clique.c).
Same call as the python3 -c one-liners of build_G1_G2/macjobs/MAC_JOBS.md (J2, J3), with two differences:
the solver is CHECKER_DIR/clique_mac (the Linux `clique` next to it cannot run on macOS), and the timeout
is a stated cap (TIMEOUT_S) that prints a TIMEOUT record instead of a traceback.

  python3 onecolour.py CHECKER_DIR FORMAT PATH ENTRY COLOUR K TIMEOUT_S
  e.g. python3 onecolour.py checker g6 built/mathon797_R11_11.g6.gz 0 1 11 86400

Prints one JSON line, e.g. {"colour": 1, "K11": [false, "NONE 10"], "seconds": ...}; PASS = [false, "NONE K-1"].
"""
import os, sys, json, time, subprocess, hashlib

checker, fmt, path, entry, colour, k, T = sys.argv[1:8]
colour, k, T = int(colour), int(k), float(T)
checker = os.path.abspath(checker)
sys.path.insert(0, checker)
import verify_ramsey as V
V.CLIQUE = os.path.join(checker, 'clique_mac')
if not os.path.exists(V.CLIQUE):
    sys.exit('missing %s (wave0.sh builds it)' % V.CLIQUE)
t0 = time.time()
C = V.load(fmt, path, entry)
rec = dict(colour=colour, file=path, sha256_file=hashlib.sha256(open(path, 'rb').read()).hexdigest(), n=len(C))
try:
    rec['K%d' % k] = list(V.has_clique(C, colour, k, timeout=T))
except subprocess.TimeoutExpired:
    rec['K%d' % k] = 'TIMEOUT after %d s' % T
rec['seconds'] = round(time.time() - t0, 1)
print(json.dumps(rec), flush=True)
