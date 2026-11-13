"""networkx (find_cliques) cross-check of an input witness used in a reduction.
  python3 nx_inputs.py NAME HALF TIMEOUT      NAME in kuz514 | mathon204 | mathon564
Circulant inputs (tested with verify_ramsey.is_circulant) are searched through vertex 0 only.
Appends to logs/nx_inputs.jsonl."""
import os, sys, json, time, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools')); sys.path.insert(0, HERE)
import verify_ramsey as V
import g3lib as L
from verify_built import NXCHILD
REPO = os.path.join(HERE, '..', 'repo')
SRC = {'kuz514': ('circcsv', '<cloud>/ramsey-witnesses/data/kuznetsov/table2_circulants.csv', '(5,14)', 5, 14),
       'mathon204': ('g6', os.path.join(REPO, 'constructions/witnesses/mathon101_R7_7.g6'), '0', 7, 7),
       'mathon564': ('g6', os.path.join(REPO, 'constructions/witnesses/mathon281_R9_9.g6'), '0', 9, 9)}
name, half, T = sys.argv[1], sys.argv[2], float(sys.argv[3])
fmt, path, entry, k, l = SRC[name]
C = V.load(fmt, path, entry); A = (C == 1).astype(np.uint8); np.fill_diagonal(A, 0)
sym = V.is_circulant(C)
X = A if half == 'clique' else L.complement(A); size = k if half == 'clique' else l
tmp = os.path.join(HERE, 'logs', 'tmp_in_%s_%s.npy' % (name, half)); np.save(tmp, X)
t0 = time.time()
try:
    p = subprocess.run([sys.executable, '-c', NXCHILD, tmp, str(size), '1' if sym else '0'], capture_output=True, text=True, timeout=T)
    r = json.loads(p.stdout.strip().split('\n')[-1]); res = 'FOUND' if r['found'] else 'NONE'
except subprocess.TimeoutExpired:
    r = None; res = 'TIMEOUT'
os.remove(tmp)
rec = dict(input=name, half=half, size=size, sym=bool(sym), result=res, nx=r, seconds=round(time.time() - t0, 1))
print(json.dumps(rec)); open(os.path.join(HERE, 'logs', 'nx_inputs.jsonl'), 'a').write(json.dumps(rec) + '\n')
